# Ruleset: newsletter

Ein Email-Newsletter. **Das einzige Set, dessen Zielformat HTML ist** — weil das Endprodukt in einem Mail-Client rendern muss.

## Warum hier HTML statt Markdown

Mail-Clients (Gmail, Outlook, Apple Mail) rendern kein Markdown und sind beim HTML eigenwillig. Das Template ist deshalb echtes, gehärtetes HTML. Das ist die *eine* dokumentierte Ausnahme von der Markdown-Regel.

## Was gehört rein

- **Eine** Kernbotschaft pro Newsletter — nicht fünf.
- Klare Abschnitte mit Überschriften; jeder Abschnitt eine in sich geschlossene Einheit.
- Ein klarer Call-to-Action.
- Pre-Header-Text (die Vorschau-Zeile im Postfach).

## Email-HTML-Regeln (PFLICHT)

> **PFLICHT — Mail-Client-Härtung, sonst bricht das Layout:**
> - **Inline-CSS** verwenden — viele Clients strippen `<style>`-Blöcke und `<head>`.
> - **Tabellen-Layout** (`<table>`) statt Flexbox/Grid — alte Clients (Outlook) können kein modernes CSS.
> - Feste **max-width ~600px** für den Inhalts-Container.
> - **Alt-Text** für jedes Bild — viele Clients laden Bilder erst nach Klick.
> - Keine externen Web-Fonts verlassen — System-Font-Stack mit Fallback.

## Was gehört NICHT rein

- JavaScript (wird von Mail-Clients entfernt/blockiert).
- `<style>` im `<head>` als einzige Stilquelle (siehe Inline-CSS-Regel).
- Mehrere konkurrierende CTAs.

## Validierung

`scripts/validate_newsletter.py` prüft das fertige HTML automatisch:

- **Wohlgeformtheit** — balancierte Tags, parsebares HTML.
- **Pflicht-Kontext** — `title` muss gesetzt sein (sonst leerer `<title>`/Postfach-Betreff).
- **Härtung** — kein `<script>`, jedes `<img>` hat `alt`, ein `max-width`-Container
  ist vorhanden, kein `<style>` im `<head>`.
