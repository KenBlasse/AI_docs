#!/usr/bin/env python3
"""Prüft ein Dokument gegen sein Frontmatter-Schema.

Usage: python scripts/validate.py <pfad-zur-datei>
Exit:  0 = ok, 1 = Fehler gefunden, 2 = Aufruffehler
"""
import sys
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1)) or {}


def check_field(name: str, rule: dict, fm: dict) -> list[str]:
    errors = []
    present = name in fm and fm[name] not in (None, "")
    if rule.get("required") and not present:
        errors.append(f"Pflichtfeld '{name}' fehlt oder ist leer.")
        return errors
    if present and rule.get("type") == "enum":
        if fm[name] not in rule.get("values", []):
            allowed = ", ".join(rule["values"])
            errors.append(f"Feld '{name}': '{fm[name]}' nicht erlaubt (erlaubt: {allowed}).")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"Datei nicht gefunden: {path}")
        return 2

    text = path.read_text()
    fm = parse_frontmatter(text)
    if fm is None:
        print("FEHLER: Kein YAML-Frontmatter gefunden.")
        return 1

    doc_type = fm.get("type")
    schema = yaml.safe_load((ROOT / "schemas" / "frontmatter.yaml").read_text())
    type_schema = schema.get("types", {}).get(doc_type)

    if type_schema is None:
        print(f"FEHLER: Typ '{doc_type}' nicht im Schema definiert.")
        return 1

    errors = []
    for field_name, rule in type_schema.items():
        if field_name.startswith("_") or not isinstance(rule, dict):
            continue
        errors.extend(check_field(field_name, rule, fm))

    if errors:
        print(f"UNGÜLTIG: {path}")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {path} ({doc_type})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
