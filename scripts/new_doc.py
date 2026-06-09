#!/usr/bin/env python3
"""Erzeugt ein neues Dokument aus einem Template.

Usage: python scripts/new_doc.py <typ> "<titel>"
"""
import sys
import datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent


def slugify(text: str) -> str:
    keep = "".join(c if c.isalnum() or c in " -" else "" for c in text.lower())
    return "-".join(keep.split())


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    doc_type, title = sys.argv[1], sys.argv[2]
    config = yaml.safe_load((ROOT / "config.yaml").read_text())

    if doc_type not in config["types"]:
        known = ", ".join(config["types"])
        print(f"Unbekannter Typ '{doc_type}'. Bekannt: {known}")
        return 1

    spec = config["types"][doc_type]
    template_path = Path(spec["template"])

    env = Environment(
        loader=FileSystemLoader(str(ROOT / template_path.parent)),
        keep_trailing_newline=True,
    )
    template = env.get_template(template_path.name)
    rendered = template.render(
        title=title,
        created=datetime.date.today().isoformat(),
    )

    out_dir = ROOT / config["output_dir"] / doc_type
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{slugify(title)}.{spec['extension']}"
    out_file.write_text(rendered)

    print(f"Erstellt: {out_file}")
    print(f"Regeln dazu: {spec['rules']} (+ {config['global_rules']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
