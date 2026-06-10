#!/usr/bin/env python3
"""Prüft ein Dokument gegen sein Frontmatter-Schema (echtes JSON Schema).

Frontmatter wird mit python-frontmatter geparst (robust gegen --- im Body,
mehrzeilige Werte, Code-Fences) und mit jsonschema/Draft 2020-12 validiert.
Daraus ergeben sich Typprüfung, Pattern, Datumsformat und additionalProperties
gratis — ohne eigenen Feld-für-Feld-Validierungscode.

Usage: python scripts/validate.py <pfad-zur-datei> [<weitere> ...]
Exit:  0 = alle ok, 1 = Fehler gefunden, 2 = Aufruffehler
"""
import datetime
import sys
from functools import lru_cache
from pathlib import Path

import frontmatter
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "frontmatter.yaml"


@lru_cache(maxsize=1)
def load_schemas() -> dict:
    """Lädt die JSON-Schema-Definitionen pro Typ aus schemas/frontmatter.yaml."""
    data = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8")) or {}
    return data.get("types", {})


def _normalize(metadata: dict) -> dict:
    """YAML lädt ISO-Daten als date/datetime — JSON Schema 'format: date' prüft
    aber nur Strings. Wir spiegeln solche Werte als ISO-String zurück, damit ein
    echter Datums-Check stattfindet (statt ihn stillschweigend zu überspringen)."""
    out = {}
    for key, value in metadata.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            out[key] = value.isoformat()
        else:
            out[key] = value
    return out


def validate_file(path) -> list[str]:
    """Validiert eine Datei. Gibt eine Liste von Fehlermeldungen zurück (leer = ok)."""
    path = Path(path)
    try:
        post = frontmatter.load(str(path))
    except Exception as exc:  # kaputtes YAML, Encoding etc.
        return [f"Frontmatter nicht lesbar: {exc}"]

    if not post.metadata:
        return ["Kein YAML-Frontmatter gefunden."]

    metadata = _normalize(post.metadata)
    doc_type = metadata.get("type")
    schemas = load_schemas()

    if doc_type not in schemas:
        known = ", ".join(sorted(schemas)) or "(keine)"
        return [f"Unbekannter type: {doc_type!r} (bekannt: {known})."]

    validator = Draft202012Validator(schemas[doc_type], format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(metadata), key=lambda e: list(e.json_path))
    return [f"{e.json_path}: {e.message}" for e in errors]


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__)
        return 2

    exit_code = 0
    for arg in argv:
        path = Path(arg)
        if not path.is_file():
            print(f"Datei nicht gefunden: {path}")
            exit_code = 2
            continue

        errors = validate_file(path)
        if errors:
            print(f"UNGÜLTIG: {path}")
            for e in errors:
                print(f"  - {e}")
            exit_code = exit_code or 1
        else:
            print(f"OK: {path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
