#!/usr/bin/env python3
"""Erzeugt ein neues Dokument aus einem Template.

Usage:
  python scripts/new_doc.py <typ> "<titel>" [--field KEY=WERT ...] [--force]

Mit --field lassen sich optionale Template-Felder direkt setzen (z. B.
--field status=approved). Ohne Angabe greifen die im Template hinterlegten
Default-Prompts, die du danach im Editor ausfüllst.
"""
import argparse
import datetime
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateError, select_autoescape

ROOT = Path(__file__).resolve().parent.parent


def slugify(text: str) -> str:
    keep = "".join(c if c.isalnum() or c in " -" else "" for c in text.lower())
    slug = "-".join(keep.split())
    return slug or "untitled"


def parse_fields(pairs: list[str]) -> dict[str, str]:
    """Wandelt ['k=v', ...] in ein Dict. Bricht bei fehlendem '=' kontrolliert ab."""
    fields = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"--field erwartet KEY=WERT, bekam: {pair!r}")
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"--field mit leerem Schlüssel: {pair!r}")
        fields[key] = value
    return fields


def unique_path(out_dir: Path, slug: str, ext: str) -> Path:
    """Gibt einen noch nicht existierenden Pfad zurück (slug, slug-2, slug-3, …)."""
    candidate = out_dir / f"{slug}.{ext}"
    n = 2
    while candidate.exists():
        candidate = out_dir / f"{slug}-{n}.{ext}"
        n += 1
    return candidate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Neues Dokument aus Template erzeugen.")
    parser.add_argument("type", help="Dokumenttyp (siehe config.yaml)")
    parser.add_argument("title", help="Titel des Dokuments")
    parser.add_argument("--field", action="append", default=[], metavar="KEY=WERT",
                        help="Optionales Template-Feld setzen (mehrfach möglich)")
    parser.add_argument("--force", action="store_true",
                        help="Vorhandene Datei überschreiben statt zu nummerieren")
    args = parser.parse_args(argv)

    try:
        fields = parse_fields(args.field)
    except ValueError as exc:
        print(f"Fehler: {exc}")
        return 2

    try:
        config = yaml.safe_load((ROOT / "config.yaml").read_text())
    except (OSError, yaml.YAMLError) as exc:
        print(f"config.yaml nicht lesbar: {exc}")
        return 1

    try:
        types = config["types"]
        output_dir = config["output_dir"]
        global_rules = config["global_rules"]
    except (KeyError, TypeError) as exc:
        print(f"config.yaml unvollständig — fehlender Schlüssel: {exc}")
        return 1

    if args.type not in types:
        known = ", ".join(types) or "(keine)"
        print(f"Unbekannter Typ {args.type!r}. Bekannt: {known}")
        return 1

    spec = types[args.type]
    try:
        template_path = Path(spec["template"])
        extension = spec["extension"]
    except (KeyError, TypeError) as exc:
        print(f"config.yaml: Typ {args.type!r} fehlt ein Schlüssel: {exc}")
        return 1

    # autoescape für HTML-Templates (Newsletter): --field-Werte kommen von außen,
    # ungeschütztes HTML darin wäre eine XSS-Lücke im gerenderten Newsletter.
    # Markdown-Templates bleiben unescaped, damit z. B. & nicht zu &amp; wird.
    env = Environment(  # nosemgrep: direct-use-of-jinja2 — autoescape via select_autoescape gesetzt
        loader=FileSystemLoader(str(ROOT / template_path.parent)),
        keep_trailing_newline=True,
        autoescape=select_autoescape(
            enabled_extensions=("html", "htm", "j2"),
            default_for_string=False,
        ),
    )
    try:
        template = env.get_template(template_path.name)
        rendered = template.render(  # nosemgrep: direct-use-of-jinja2 — Environment hat autoescape
            title=args.title,
            created=datetime.date.today().isoformat(),
            **fields,
        )
    except TemplateError as exc:
        print(f"Template {template_path} konnte nicht gerendert werden: {exc}")
        return 1

    out_dir = ROOT / output_dir / args.type
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.title)
    if args.force:
        out_file = out_dir / f"{slug}.{extension}"
    else:
        out_file = unique_path(out_dir, slug, extension)
    out_file.write_text(rendered)

    print(f"Erstellt: {out_file}")
    print(f"Regeln dazu: {spec.get('rules', '—')} (+ {global_rules})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
