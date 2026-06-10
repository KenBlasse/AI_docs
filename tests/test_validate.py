"""Tests für scripts/validate.py — echtes Frontmatter-Parsing + JSON Schema (#1, #3)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate  # noqa: E402

FIX = ROOT / "tests" / "fixtures"


@pytest.mark.parametrize("path", sorted((FIX / "valid").glob("*.md")), ids=lambda p: p.name)
def test_valid_fixtures_pass(path):
    assert validate.validate_file(path) == [], f"{path.name} sollte gültig sein"


@pytest.mark.parametrize("path", sorted((FIX / "invalid").glob("*.md")), ids=lambda p: p.name)
def test_invalid_fixtures_fail(path):
    assert validate.validate_file(path), f"{path.name} sollte mindestens einen Fehler liefern"


def test_bad_date_is_rejected():
    """#3: created muss ein echtes ISO-Datum sein, nicht nur 'vorhanden'."""
    errors = validate.validate_file(FIX / "invalid" / "spec-bad-date.md")
    assert any("created" in e for e in errors), errors


def test_typo_field_is_rejected():
    """additionalProperties:false fängt Tippfehler in Feldnamen."""
    errors = validate.validate_file(FIX / "invalid" / "spec-typo-field.md")
    assert any("titel" in e for e in errors), errors


def test_hr_in_body_does_not_break_parsing():
    """#1: --- im Body / Code-Fence darf das Frontmatter nicht zerstören."""
    assert validate.validate_file(FIX / "valid" / "spec-with-hr-in-body.md") == []


def test_no_frontmatter_reports_error():
    errors = validate.validate_file(FIX / "invalid" / "no-frontmatter.md")
    assert errors


def test_unknown_type_reports_error():
    errors = validate.validate_file(FIX / "invalid" / "unknown-type.md")
    assert any("type" in e.lower() for e in errors), errors


def test_out_documents_validate():
    """Die ausgelieferten Beispiel-Dokumente in out/ müssen gültig bleiben."""
    for path in (ROOT / "out").rglob("*.md"):
        assert validate.validate_file(path) == [], f"{path} ist ungültig"
