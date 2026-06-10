#!/usr/bin/env python3
"""Hält die Frontmatter-Felder in den Rule-Files mit dem Schema in Sync.

`schemas/frontmatter.yaml` ist die einzige Quelle der Wahrheit. Dieses Script
erzeugt daraus pro Typ eine Feld-Tabelle und schreibt sie in das jeweilige
Rule-File zwischen die Marker:

    <!-- FIELDS:start -->
    ... generiert, nicht von Hand bearbeiten ...
    <!-- FIELDS:end -->

Zusätzlich prüft es, dass das Frontmatter der Templates (templates/<typ>.md) zum
Schema passt — gleiche Feld-Menge, gleicher type-Wert. Das fängt den Drift, der
sich nicht generieren lässt (Templates enthalten Jinja2-Platzhalter + Defaults).

Usage:
  python scripts/sync_fields.py            # schreibt die Marker-Blöcke
  python scripts/sync_fields.py --check    # prüft nur, schreibt nicht (CI)
Exit: 0 = in Sync, 1 = Drift gefunden (nur --check), 2 = Aufruffehler
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "frontmatter.yaml"
CONFIG_PATH = ROOT / "config.yaml"
RULES_DIR = ROOT / "rules"
TEMPLATES_DIR = ROOT / "templates"

START = "<!-- FIELDS:start -->"
END = "<!-- FIELDS:end -->"


def load_schemas() -> dict:
    data = yaml.safe_load(SCHEMA_PATH.read_text()) or {}
    return data.get("types", {})


def template_path_for(doc_type: str) -> Path | None:
    """Liefert den in config.yaml hinterlegten Template-Pfad eines Typs (absolut).

    None, wenn der Typ nicht in der Config steht oder die Config nicht lesbar ist —
    dann fällt der Drift-Check auf die alte Konvention templates/<typ>.md zurück.
    """
    try:
        config = yaml.safe_load(CONFIG_PATH.read_text()) or {}
    except (OSError, yaml.YAMLError):
        return None
    spec = config.get("types", {}).get(doc_type, {})
    rel = spec.get("template")
    return ROOT / rel if rel else None


def field_table(schema: dict) -> str:
    """Erzeugt eine Markdown-Tabelle der Felder aus einem JSON-Schema-Objekt."""
    required = set(schema.get("required", []))
    rows = ["| Feld | Pflicht | Typ / Werte |", "| --- | --- | --- |"]
    for name, spec in schema.get("properties", {}).items():
        pflicht = "ja" if name in required else "nein"
        rows.append(f"| `{name}` | {pflicht} | {describe(spec)} |")
    return "\n".join(rows)


def describe(spec: dict) -> str:
    """Knappe, menschenlesbare Beschreibung einer Property aus ihrem JSON Schema."""
    if "const" in spec:
        return f"`{spec['const']}` (fest)"
    if "enum" in spec:
        return " / ".join(f"`{v}`" for v in spec["enum"])
    if spec.get("format") == "date":
        return "Datum (`YYYY-MM-DD`)"
    if spec.get("type") == "string":
        return "Text" + (" (nicht leer)" if spec.get("minLength") else "")
    return spec.get("type", "—")


def render_block(doc_type: str, schema: dict) -> str:
    return (
        f"{START}\n"
        f"<!-- generiert aus schemas/frontmatter.yaml via scripts/sync_fields.py — nicht von Hand bearbeiten -->\n\n"
        f"{field_table(schema)}\n\n"
        f"{END}"
    )


def replace_block(text: str, block: str) -> str | None:
    """Ersetzt den Inhalt zwischen den Markern. None, wenn keine Marker da sind."""
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        return None
    return pattern.sub(lambda _: block, text)


def parse_template_frontmatter(text: str) -> dict[str, str]:
    """Liest die `key: wert`-Paare aus dem führenden ----Block eines Templates.

    Bewusst kein YAML-Parser: Template-Werte enthalten Jinja2 (`{{ created }}`),
    was YAML als Flow-Mapping missdeutet. Wir brauchen ohnehin nur die Keys (und
    den rohen type-Wert), also splitten wir die Zeilen selbst am ersten `:`.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    out = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip().strip('"')
    return out


def template_drift(doc_type: str, schema: dict) -> list[str]:
    """Prüft, ob das Markdown-Template eines Typs zum Schema passt (Feld-Menge + type-Wert).

    Der Template-Pfad kommt aus config.yaml (nicht hartkodiert), mit Fallback auf
    die Konvention templates/<typ>.md. Nur Markdown-Templates haben YAML-Frontmatter;
    HTML-Templates (Newsletter) werden übersprungen — kein Drift-Check.
    """
    tpl = template_path_for(doc_type) or TEMPLATES_DIR / f"{doc_type}.md"
    if tpl.suffix != ".md" or not tpl.is_file():
        return []
    meta = parse_template_frontmatter(tpl.read_text())
    schema_keys = set(schema.get("properties", {}))
    tpl_keys = set(meta)
    problems = []
    if tpl_keys != schema_keys:
        missing = schema_keys - tpl_keys
        extra = tpl_keys - schema_keys
        if missing:
            problems.append(f"Template fehlt: {', '.join(sorted(missing))}")
        if extra:
            problems.append(f"Template hat extra: {', '.join(sorted(extra))}")
    const = schema.get("properties", {}).get("type", {}).get("const")
    if const and meta.get("type") != const:
        problems.append(f"type ist {meta.get('type')!r}, Schema verlangt {const!r}")
    return problems


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    check_only = "--check" in argv

    schemas = load_schemas()
    drift = []
    written = []

    for doc_type, schema in schemas.items():
        # 1. Template-Frontmatter gegen Schema
        for problem in template_drift(doc_type, schema):
            drift.append(f"templates/{doc_type}.md: {problem}")

        # 2. Feld-Block in der Rule
        rule = RULES_DIR / f"{doc_type}.md"
        if not rule.is_file():
            continue
        text = rule.read_text()
        new_text = replace_block(text, render_block(doc_type, schema))
        if new_text is None:
            drift.append(f"rules/{doc_type}.md: keine FIELDS-Marker gefunden")
            continue
        if new_text != text:
            if check_only:
                drift.append(f"rules/{doc_type}.md: Feld-Block veraltet (sync nötig)")
            else:
                rule.write_text(new_text)
                written.append(f"rules/{doc_type}.md")

    if check_only:
        if drift:
            print("DRIFT gefunden:")
            for d in drift:
                print(f"  - {d}")
            return 1
        print("OK: Felder, Templates und Schema sind in Sync.")
        return 0

    for d in drift:
        print(f"WARNUNG: {d}")
    for w in written:
        print(f"aktualisiert: {w}")
    if not written:
        print("Nichts zu tun — alles aktuell.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
