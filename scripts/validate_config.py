#!/usr/bin/env python3
"""Validiert config.yaml und schemas/frontmatter.yaml gegen ein Meta-Schema.

Beide Dateien steuern die übrigen Tools. Ein Tippfehler darin (falscher Key,
fehlende extension, kaputtes Teil-Schema) fiel bisher erst zur Laufzeit auf —
oft als unklarer KeyError tief im Aufruf. Dieses Script prüft die Struktur
vorab und meldet die Stelle klar.

Geprüft wird zusätzlich die Kreuz-Konsistenz: jeder Typ in config.yaml hat ein
Schema in frontmatter.yaml (und referenzierte rules-/template-Dateien existieren).

Usage: python scripts/validate_config.py
Exit:  0 = ok, 1 = Fehler gefunden
"""
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.yaml"
SCHEMA_PATH = ROOT / "schemas" / "frontmatter.yaml"

# Meta-Schema für config.yaml
CONFIG_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["output_dir", "types", "global_rules", "schema"],
    "properties": {
        "output_dir": {"type": "string", "minLength": 1},
        "global_rules": {"type": "string", "minLength": 1},
        "schema": {"type": "string", "minLength": 1},
        "types": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {
                "type": "object",
                "additionalProperties": False,
                "required": ["rules", "template", "extension"],
                "properties": {
                    "rules": {"type": "string", "minLength": 1},
                    "template": {"type": "string", "minLength": 1},
                    "extension": {"type": "string", "minLength": 1},
                },
            },
        },
    },
}

# Meta-Schema für schemas/frontmatter.yaml: types.<name> ist je ein JSON-Schema-Objekt.
FRONTMATTER_META = {
    "type": "object",
    "required": ["types"],
    "properties": {
        "types": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {
                "type": "object",
                "required": ["type", "properties"],
                "properties": {
                    "type": {"const": "object"},
                    "required": {"type": "array", "items": {"type": "string"}},
                    "properties": {"type": "object", "minProperties": 1},
                },
            },
        }
    },
}


def _load(path: Path) -> tuple[dict | None, str | None]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}, None
    except (OSError, yaml.YAMLError) as exc:
        return None, f"{path.name} nicht lesbar: {exc}"


def _schema_errors(data: dict, schema: dict, label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.json_path))
    return [f"{label} — {e.json_path}: {e.message}" for e in errors]


def validate() -> list[str]:
    problems: list[str] = []

    config, err = _load(CONFIG_PATH)
    if err:
        return [err]
    fm, err = _load(SCHEMA_PATH)
    if err:
        return [err]

    problems += _schema_errors(config, CONFIG_SCHEMA, "config.yaml")
    problems += _schema_errors(fm, FRONTMATTER_META, "frontmatter.yaml")

    # Struktur ok? Dann Kreuz-Konsistenz prüfen.
    if problems:
        return problems

    config_types = set(config["types"])
    schema_types = set(fm["types"])

    # Jeder Markdown-Typ braucht ein Frontmatter-Schema. HTML-Typen (extension html)
    # sind bewusst ausgenommen (kein YAML-Frontmatter, siehe Newsletter).
    for name, spec in config["types"].items():
        if spec["extension"] != "html" and name not in schema_types:
            problems.append(f"Typ {name!r}: in config.yaml, aber kein Schema in frontmatter.yaml")
        for key in ("rules", "template"):
            ref = ROOT / spec[key]
            if not ref.is_file():
                problems.append(f"Typ {name!r}: {key}-Datei fehlt: {spec[key]}")

    # Schema-Typen ohne config-Eintrag → verwaistes Schema
    for name in schema_types - config_types:
        problems.append(f"Schema-Typ {name!r} in frontmatter.yaml hat keinen config.yaml-Eintrag")

    # Referenzierte globale Dateien existieren
    for key in ("global_rules", "schema"):
        if not (ROOT / config[key]).is_file():
            problems.append(f"config.yaml: {key}-Datei fehlt: {config[key]}")

    return problems


def main(argv: list[str] | None = None) -> int:
    problems = validate()
    if problems:
        print("UNGÜLTIGE Konfiguration:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("OK: config.yaml und schemas/frontmatter.yaml sind konsistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
