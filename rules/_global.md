# Globale Regeln

Format-übergreifende Grundregeln. Gelten für **jeden** Dokumenttyp, sofern ein typ-spezifisches Ruleset nichts anderes sagt.

## Markdown ist Primärformat

- Alles, was gelesen, verlinkt oder durchsucht wird, ist Markdown.
- HTML **nur** dort, wo das *Endprodukt* HTML sein muss (z. B. ein Email-Newsletter, der in einem Mail-Client rendert).
- **Warum:** Reines HTML kostet deutlich mehr Tokens als dieselbe Information in Markdown (relevant, weil AIs die Dateien lesen). Viele MD-Tools rendern eigenständige `.html`-Dateien nicht als Teil des Doc-Graphen — keine Backlinks, kein Frontmatter, keine Suche. HTML *innerhalb* von MD ist fragil.

## Kritische Regeln sichtbar machen

Für PFLICHT-Regeln, Warnungen und wichtigen Kontext **Callout-Blöcke** statt HTML-Tags verwenden:

> [!danger] für Pflicht-Regeln und Sicherheits-Checks — kein Skip
> [!warning] für Abweichungs- und Recovery-Hinweise
> [!info] für Kontext und Begründungen

Callouts wirken beim Lesen mindestens so stark wie HTML-Tags, kosten kaum Tokens und sind sofort als kritisch erkennbar.

## Jedes Dokument hat Frontmatter

- YAML-Frontmatter am Dateianfang, mindestens: `title`, `type`, `created`.
- Welche Felder ein Typ darüber hinaus verlangt, steht im typ-spezifischen Ruleset und in `schemas/frontmatter.yaml`.

## Ein gutes Ruleset ist kurz und entscheidbar

> [!info] Leitprinzip
> Die wertvollste Sektion jedes Rulesets ist eine klare **"Was gehört rein / Was gehört NICHT rein"**-Abgrenzung. Eine Regel, bei der man im Zweifelsfall *entscheiden* kann, schlägt drei Absätze Prosa.

- Regeln sind Bullet-Points, keine Aufsätze.
- Jede Regel ist durchsetzbar oder prüfbar — sonst ist sie ein Wunsch, keine Regel.
- Begründung (`Warum:`) nur dort, wo sie nicht offensichtlich ist.

## Verlinken statt duplizieren

- Eine Information lebt an *einem* Ort. Andere Dokumente verweisen darauf.
- Interne Verweise als relative Links oder als das Verlinkungs-Format deines Tools.
