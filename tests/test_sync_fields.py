"""Tests für scripts/sync_fields.py — Single Source of Truth für Felder (#2).

Schema ist die alleinige Quelle; Rule-Tabellen und Template-Frontmatter müssen
dazu passen. Der Kern-Test ruft den --check-Modus auf — schlägt er fehl, ist
irgendwo Drift entstanden (Schema geändert, Rule/Template nicht nachgezogen).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sync_fields  # noqa: E402


def test_repo_is_in_sync():
    """Rules + Templates sind mit dem Schema in Sync (sonst: sync_fields.py laufen lassen)."""
    assert sync_fields.main(["--check"]) == 0


def test_check_detects_template_drift(tmp_path, monkeypatch):
    """Ein Template, dem ein Schema-Pflichtfeld fehlt, wird als Drift gemeldet."""
    schema = {"type": "object", "required": ["title", "type"],
              "properties": {"title": {"type": "string"}, "type": {"const": "demo"}}}
    tpl = tmp_path / "demo.md"
    tpl.write_text("---\ntype: demo\n---\n")  # title fehlt
    monkeypatch.setattr(sync_fields, "TEMPLATES_DIR", tmp_path)
    problems = sync_fields.template_drift("demo", schema)
    assert any("title" in p for p in problems)


def test_check_detects_type_mismatch(tmp_path, monkeypatch):
    """Ein falscher type-Wert im Template wird gemeldet."""
    schema = {"type": "object", "required": ["type"],
              "properties": {"type": {"const": "demo"}}}
    tpl = tmp_path / "demo.md"
    tpl.write_text("---\ntype: falsch\n---\n")
    monkeypatch.setattr(sync_fields, "TEMPLATES_DIR", tmp_path)
    problems = sync_fields.template_drift("demo", schema)
    assert any("type" in p for p in problems)


def test_parse_template_frontmatter_handles_jinja():
    """Jinja2-Werte (`{{ created }}`) dürfen das Key-Parsing nicht sprengen."""
    text = '---\ntitle: "{{ title }}"\ntype: spec\ncreated: {{ created }}\nstatus: draft\n---\nBody\n'
    meta = sync_fields.parse_template_frontmatter(text)
    assert set(meta) == {"title", "type", "created", "status"}
    assert meta["type"] == "spec"


def test_describe_enum_and_const():
    assert sync_fields.describe({"const": "spec"}) == "`spec` (fest)"
    assert sync_fields.describe({"enum": ["a", "b"]}) == "`a` / `b`"
    assert sync_fields.describe({"type": "string", "format": "date"}) == "Datum (`YYYY-MM-DD`)"
