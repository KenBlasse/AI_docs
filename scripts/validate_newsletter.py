#!/usr/bin/env python3
"""Prüft fertiges Newsletter-HTML auf Wohlgeformtheit und Mail-Client-Härtung.

Der Newsletter ist der einzige Typ mit HTML-Zielformat und hatte bisher keine
Validierung — der fragilste Typ war ungeprüft. Dieses Script schließt die Lücke:
es parst das HTML (stdlib html.parser, keine Extra-Dependency), prüft auf
balancierte Tags und setzt die Härtungsregeln aus rules/newsletter.md durch.

Eingabe ist fertiges HTML — entweder eine gerenderte Datei (out/newsletter/*.html)
oder via --template wird das Jinja2-Template vorher gerendert.

Usage:
  python scripts/validate_newsletter.py out/newsletter/mail.html
  python scripts/validate_newsletter.py --template            # Standard-Template rendern + prüfen
Exit: 0 = ok, 1 = Fehler gefunden, 2 = Aufruffehler
"""
import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# void elements brauchen kein schließendes Tag (HTML5)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class NewsletterParser(HTMLParser):
    """Sammelt die Fakten, die wir für die Härtungs-Checks brauchen, in einem Durchlauf."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.balance_errors: list[str] = []
        self.tags_seen: set[str] = set()
        self.imgs_without_alt = 0
        self.has_script = False
        self.has_max_width = False
        self.title_text = ""
        self.in_title = False
        self.style_in_head = False
        self.in_head = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        self.tags_seen.add(tag)
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "head":
            self.in_head = True
        if tag == "style" and self.in_head:
            self.style_in_head = True
        if tag == "title":
            self.in_title = True
        if tag == "script":
            self.has_script = True
        # alt="" ist für dekorative Bilder der a11y-korrekte Weg (WCAG) — nur ein
        # komplett fehlendes alt-Attribut ist ein Fehler.
        if tag == "img" and "alt" not in attrs_d:
            self.imgs_without_alt += 1
        style = attrs_d.get("style", "")
        if "max-width" in style:
            self.has_max_width = True

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "head":
            self.in_head = False
        if tag == "title":
            self.in_title = False
        if not self.stack:
            self.balance_errors.append(f"</{tag}> ohne offenes Tag")
            return
        if self.stack[-1] != tag:
            self.balance_errors.append(
                f"</{tag}> erwartet </{self.stack[-1]}> (verschachtelte/unbalancierte Tags)")
            # tolerant: zurückspulen, falls das Tag weiter unten offen ist
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
            return
        self.stack.pop()

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data


def validate_html(html: str) -> list[str]:
    """Gibt eine Liste von Fehlern zurück (leer = ok)."""
    parser = NewsletterParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as exc:
        return [f"HTML nicht parsebar: {exc}"]

    errors: list[str] = []

    # 1. Wohlgeformtheit
    errors.extend(parser.balance_errors)
    if parser.stack:
        errors.append(f"Nicht geschlossene Tags: {', '.join(parser.stack)}")

    # 2. Pflicht-Kontext: ein nicht-leerer Titel
    if not parser.title_text.strip():
        errors.append("Kein <title>-Text (Pflicht-Kontextvariable 'title' fehlt/leer)")

    # 3. Härtungsregeln aus rules/newsletter.md
    if parser.has_script:
        errors.append("<script> gefunden — Mail-Clients entfernen/blockieren JS")
    if parser.imgs_without_alt:
        errors.append(f"{parser.imgs_without_alt} <img> ohne alt-Text")
    if not parser.has_max_width:
        errors.append("Kein max-width-Container gefunden (Inhalt sollte ~600px begrenzt sein)")
    if parser.style_in_head:
        errors.append("<style> im <head> — viele Clients strippen es; Inline-CSS verwenden")

    return errors


def render_template() -> str:
    """Rendert das Standard-Newsletter-Template mit autoescape (für den --template-Modus)."""
    import yaml
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    tpl_rel = Path(config["types"]["newsletter"]["template"])
    env = Environment(  # nosemgrep: direct-use-of-jinja2 — autoescape via select_autoescape gesetzt
        loader=FileSystemLoader(str(ROOT / tpl_rel.parent)),
        autoescape=select_autoescape(enabled_extensions=("html", "htm", "j2")),
    )
    return env.get_template(tpl_rel.name).render(title="Beispiel-Newsletter")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Newsletter-HTML validieren.")
    parser.add_argument("paths", nargs="*", help="HTML-Datei(en)")
    parser.add_argument("--template", action="store_true",
                        help="Standard-Template rendern und prüfen statt einer Datei")
    args = parser.parse_args(argv)

    if not args.paths and not args.template:
        parser.print_help()
        return 2

    jobs: list[tuple[str, str]] = []
    if args.template:
        jobs.append(("<template:newsletter>", render_template()))
    for p in args.paths:
        path = Path(p)
        if not path.is_file():
            print(f"Datei nicht gefunden: {path}")
            return 2
        jobs.append((str(path), path.read_text()))

    exit_code = 0
    for name, html in jobs:
        errors = validate_html(html)
        if errors:
            print(f"UNGÜLTIG: {name}")
            for e in errors:
                print(f"  - {e}")
            exit_code = 1
        else:
            print(f"OK: {name}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
