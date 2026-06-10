"""Tests für scripts/new_doc.py — Kontextfelder & Robustheit (#5)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import new_doc  # noqa: E402


# --- slugify (Problem B: leerer Slug) ---

def test_slugify_empty_falls_back_to_untitled():
    assert new_doc.slugify("###") == "untitled"
    assert new_doc.slugify("   ") == "untitled"


def test_slugify_normal():
    assert new_doc.slugify("  Ä Test! ") == "ä-test"
    assert new_doc.slugify("Mein Erster Eintrag") == "mein-erster-eintrag"


# --- parse_fields (Problem A: CLI-Flags) ---

def test_parse_fields_ok():
    assert new_doc.parse_fields(["status=approved", "x=a=b"]) == {"status": "approved", "x": "a=b"}


def test_parse_fields_missing_equals():
    with pytest.raises(ValueError):
        new_doc.parse_fields(["kaputt"])


def test_parse_fields_empty_key():
    with pytest.raises(ValueError):
        new_doc.parse_fields(["=wert"])


# --- unique_path (Problem B: Kollisionsschutz) ---

def test_unique_path_numbers_collisions(tmp_path):
    assert new_doc.unique_path(tmp_path, "doc", "md").name == "doc.md"
    (tmp_path / "doc.md").write_text("x")
    assert new_doc.unique_path(tmp_path, "doc", "md").name == "doc-2.md"
    (tmp_path / "doc-2.md").write_text("x")
    assert new_doc.unique_path(tmp_path, "doc", "md").name == "doc-3.md"


# --- main() Ende-zu-Ende über echte Templates/Config ---

def _out(monkeypatch, tmp_path):
    """Lenkt output_dir auf tmp_path, sonst echte config/templates.

    Patcht gezielt new_doc.load_config (nicht yaml.safe_load global) — sonst würde
    der bei --validate nachgelagerte Validator dieselbe gepatchte safe_load sehen
    und das Schema nicht mehr laden können.
    """
    import yaml
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    cfg["output_dir"] = str(tmp_path)
    monkeypatch.setattr(new_doc, "load_config", lambda: cfg)
    return tmp_path


def test_main_field_overrides_default(monkeypatch, tmp_path):
    out = _out(monkeypatch, tmp_path)
    assert new_doc.main(["spec", "Titel", "--field", "status=approved"]) == 0
    text = (out / "spec" / "titel.md").read_text()
    assert "status: approved" in text


def test_main_unknown_type(monkeypatch, tmp_path):
    _out(monkeypatch, tmp_path)
    assert new_doc.main(["gibtsnicht", "Titel"]) == 1


def test_main_bad_field_returns_2(monkeypatch, tmp_path):
    _out(monkeypatch, tmp_path)
    assert new_doc.main(["spec", "Titel", "--field", "kaputt"]) == 2


def test_main_no_force_does_not_overwrite(monkeypatch, tmp_path):
    out = _out(monkeypatch, tmp_path)
    new_doc.main(["session-log", "Doppelt"])
    new_doc.main(["session-log", "Doppelt"])
    files = sorted(p.name for p in (out / "session-log").glob("*.md"))
    assert files == ["doppelt-2.md", "doppelt.md"]


# --- --validate (Prüfung direkt beim Erzeugen) ---

def test_main_validate_markdown_ok(monkeypatch, tmp_path):
    """Ein erzeugtes Markdown-Doc validiert sauber → Exit 0."""
    _out(monkeypatch, tmp_path)
    assert new_doc.main(["session-log", "Geprüft", "--validate"]) == 0


def test_main_validate_newsletter_ok(monkeypatch, tmp_path):
    """Das gehärtete Newsletter-Template validiert sauber → Exit 0."""
    _out(monkeypatch, tmp_path)
    assert new_doc.main(["newsletter", "Mail", "--validate"]) == 0


def test_main_validate_catches_invalid(monkeypatch, tmp_path):
    """Ein ungültiges Feld (Schema verbietet unbekannte Keys) → Exit 1 mit --validate."""
    _out(monkeypatch, tmp_path)
    assert new_doc.main(["spec", "Kaputt", "--field", "status=gibtsnicht", "--validate"]) == 1
