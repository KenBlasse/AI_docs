# AI_docs

Ein leichtgewichtiges Framework, mit dem jeder **zusammen mit einer AI** sinnvolle, konsistente Rulesets und Templates erstellen kann — beschränkt auf drei Bausteine: **Markdown, Python, HTML**.

Repo: https://github.com/KenBlasse/AI_docs

> **Status:** Lauffähiger Prototyp. Starter-Bibliothek (5 Sets), AI-Prompts und beide Skripte sind da und getestet.

## Schnellstart

```bash
python -m venv .venv && source .venv/bin/activate   # oder: uv venv .venv
pip install -r requirements.txt

python scripts/new_doc.py session-log "Mein erster Eintrag"   # Dokument erzeugen
python scripts/validate.py out/session-log/mein-erster-eintrag.md   # prüfen
```

---

## Das Problem

Wer Notizen, Doku, Specs oder Newsletter schreibt, landet schnell bei einem von zwei Extremen:

1. **Alles in einer Datei** — eine riesige "So-schreibst-du-Docs"-MD, in der Regeln, Beispiele und Vorlagen vermischt sind. Niemand liest sie ganz, sie driftet, eine AI überfliegt sie.
2. **Gar keine Konvention** — jedes Dokument sieht anders aus, Frontmatter fehlt mal, die Struktur ist beliebig, Links sterben.

Und selbst wer es besser machen will, steht vor der Henne-Ei-Frage: *Wie baue ich überhaupt ein gutes Ruleset und gute Templates?*

**Genau da setzt AI_docs an.** Es ist kein fertiges Korsett, sondern ein Gerüst plus AI-Anleitung, mit dem du dein **eigenes** Set aus Regeln und Vorlagen aufbaust — und mitgelieferte Beispiele, an denen du (und die AI) siehst, wie gute Sets aussehen.

---

## Zwei Dinge in einem

AI_docs ist **Werkzeug und Bibliothek** zugleich:

| | Was | Wozu |
|---|-----|------|
| **Werkzeug** | Struktur + AI-Prompt-Vorlagen + Validierung | Du erstellst damit dein eigenes Ruleset/Template-Set |
| **Bibliothek** | Mitgelieferte Starter-Sets (Notiz, README, Newsletter) | Sofort nutzbar als Startpunkt — und Lern-Muster für die AI |

Die Bibliothek ist nicht nur "Beispiel" — sie ist der Boden, auf dem das Werkzeug steht. Die AI bekommt die Starter-Sets als Referenz, um daraus passende Sets für deinen Kontext zu generieren.

---

## Drei Bausteine — bewusst nur diese

AI_docs kennt absichtlich nur drei Dateitypen. Diese Beschränkung ist ein Feature, kein Mangel: Sie hält das Framework klein, verständlich und für AI gut handhabbar.

| Baustein | Rolle | Beispiel |
|----------|-------|----------|
| **Markdown** | Regeln, Doku, Templates für Text, **AI-Prompt-Vorlagen** | `rules/note.md`, `templates/note.md` |
| **Python** | Logik: Templates rendern, Dokumente validieren | `scripts/new_doc.py`, `scripts/validate.py` |
| **HTML** | Nur als **Zielformat**, wenn das Endprodukt HTML ist | `templates/newsletter.html.j2` |

---

## Die drei Schichten

Jedes Set — ob mitgeliefert oder selbst erstellt — besteht aus denselben drei Schichten:

| Schicht | Frage | Format |
|---------|-------|--------|
| **Regeln** | *Was gilt?* (Dos & Donts) | Markdown |
| **Templates** | *Wie sieht es aus?* (Struktur) | Markdown, oder HTML wenn Zielformat HTML |
| **Logik** | *Wie entsteht & stimmt es?* | Python (Jinja2) |

Kerngedanke: **Jeder Dokumenttyp bringt sein eigenes Template im nativen Format mit, plus zugehörige Regeln, plus optional Logik — nichts wird in eine Sammel-Datei gepresst.**

---

## Die AI-gestützte Erstellung (das Herzstück)

Damit du nicht bei null anfängst, liefert AI_docs **tool-agnostische Prompt-Vorlagen** (reines Markdown) unter `prompts/`. Du gibst sie einer beliebigen AI — Claude, ChatGPT, ein lokales Modell — kein Tool-Lock-in.

Ablauf:

1. **Beschreiben** — Du füllst eine kurze Vorlage aus: Welchen Dokumenttyp willst du? Wer liest ihn? Welches Format soll raus?
2. **Generieren** — Die Prompt-Vorlage instruiert die AI, ein passendes **Ruleset** (`rules/<typ>.md`) und **Template** (`templates/<typ>.*`) zu erzeugen — mit den mitgelieferten Starter-Sets als Qualitäts-Referenz.
3. **Validieren** — `scripts/validate.py` prüft das Ergebnis gegen das Schema (Frontmatter, Pflicht-Sections, tote Links). Qualitäts-Gate für das selbst Erstellte.
4. **Eintragen** — Der neue Typ kommt in `config.yaml`, ab da kennt ihn das Werkzeug.

> **INFO — Warum Prompt-Vorlagen statt fester AI-Integration:**
> Reine Markdown-Prompts funktionieren mit **jeder** AI und bleiben lesbar/editierbar — konsistent mit der Drei-Bausteine-Regel. Keine Bindung an ein bestimmtes Tool.

---

## Wichtigste Designentscheidung: HTML nur als *Zielformat*

> **INFO — HTML-Regel:**
> HTML wird **nur** verwendet, wenn das **Endprodukt** HTML ist (z. B. ein Email-Newsletter, der im Postfach gerendert wird).
> Für Regeln, Templates, Doku und Prompts bleibt **Markdown das Primärformat**.

Begründung (allgemeingültig):

- Reines HTML kostet deutlich mehr Tokens als dieselbe Information in Markdown — relevant, weil AIs die Dateien lesen.
- Viele Markdown-Tools rendern eigenständige `.html`-Dateien nicht als Teil des Doc-Graphen — keine Backlinks, kein Frontmatter, keine Suche.
- HTML *innerhalb* von Markdown ist fragil und uneinheitlich unterstützt.

→ **Markdown für alles, was gelesen/verlinkt/durchsucht wird. HTML nur, wo ein externer Renderer (Email-Client) es verlangt.**

---

## Verzeichnisstruktur

```
AI_docs/
├── README.md              # dieses Dokument — Einstieg & Konzept
├── config.yaml            # zentrale Anpassung: Doc-Typen, Frontmatter-Felder, Pfade
│
├── prompts/               # AI-Prompt-Vorlagen (Markdown, tool-agnostisch)
│   ├── make-ruleset.md    #   "Erstelle mir ein Ruleset für Typ X"
│   ├── make-template.md   #   "Erstelle mir ein Template für Typ X"
│   └── describe-type.md   #   Kurz-Fragebogen, den der Nutzer ausfüllt
│
├── rules/                 # Rulesets (Markdown) — mitgeliefert + selbst erstellt
│   ├── _global.md         #   format-übergreifende Grundregeln
│   ├── session-log.md     #   Starter: Arbeitsjournal / Changelog
│   ├── agent-instructions.md  # Starter: AI-Instruktionen pro Projekt
│   ├── spec.md            #   Starter: Design-/Konzept-Dokument
│   └── newsletter.md      #   Starter: Email-HTML (Inline-CSS, Tabellen, Alt-Text)
│
├── templates/             # Templates im jeweiligen Zielformat
│   ├── session-log.md     #   Markdown-Gerüst + Frontmatter
│   ├── agent-instructions.md
│   ├── spec.md
│   └── newsletter.html.j2 #   echtes HTML mit Jinja2-Platzhaltern & Schleifen
│
├── schemas/               # maschinenlesbare Feld-Definitionen (JSON Schema pro Typ)
│   └── frontmatter.yaml   #   Pflichtfelder, Typen, enum, Datumsformat, additionalProperties
│
└── scripts/               # Logik (Python + Jinja2) — nur die drei Bausteine
    ├── new_doc.py         #   Typ wählen → Template rendern → Zieldatei
    └── validate.py        #   Doc gegen Schema/Regeln prüfen
```

**Anpassung:** Zwei Ebenen, bewusst kombiniert.
- `config.yaml` für Häufiges (eigene Typen, Frontmatter-Felder, Zielpfade) — ohne Code anzufassen.
- `rules/`, `templates/`, `prompts/` sind **direkt editierbare** Markdown-Dateien — kein verstecktes Verhalten.

---

## Nutzungsfluss

### A) Sofort loslegen mit der Bibliothek
```bash
python scripts/new_doc.py session-log "Mein erster Eintrag"
```
Nutzt ein mitgeliefertes Starter-Set, erzeugt ein korrekt strukturiertes Dokument. Kein Setup nötig.

### B) Eigenen Typ mit AI erstellen
1. `prompts/describe-type.md` ausfüllen (Was, für wen, welches Format).
2. Ausgefüllte Vorlage + `prompts/make-ruleset.md` einer AI geben → `rules/<typ>.md` entsteht.
3. Dasselbe mit `prompts/make-template.md` → `templates/<typ>.*`.
4. `python scripts/validate.py` prüft das Ergebnis.
5. Typ in `config.yaml` eintragen — fertig, ab jetzt via `new_doc.py` nutzbar.

### C) Bestehendes Dokument prüfen
```bash
python scripts/validate.py pfad/zur/datei.md
```
Frontmatter gegen das JSON Schema des Typs geprüft (Pflichtfelder, Typen, enum, Datumsformat, unbekannte Felder) → klare Fehlerliste. Nimmt mehrere Pfade auf einmal, taugt damit als Pre-Commit-Hook. (Pflicht-Sections- und Tote-Links-Checks sind noch offen, siehe unten.)

---

## Engine: Jinja2 durchgängig

Auch für Markdown-Templates. Ein einziger Renderer für alle Formate, reine Platzhalter (`{{ titel }}`) kosten nichts, und sobald ein Typ Logik braucht (z. B. Artikel-Liste im Newsletter mit `{% for %}`) ist sie schon da. Python-Standard, leicht nachvollziehbar.

---

## Bewusste Nicht-Ziele

- **Keine anderen Dateitypen** als MD, PY, HTML. Die Beschränkung ist Absicht.
- **Keine Kopplung an ein bestimmtes Tool, Vault oder AI-Anbieter.** Prompts sind tool-agnostisch, Defaults über `config.yaml` ersetzbar.
- **Kein Editor / kein UI.** Geschrieben wird im gewohnten Editor; AI_docs liefert Struktur, AI-Anleitung und Validierung.
- **Keine schwere Infrastruktur.** Ein paar Ordner, eine Config, zwei Skripte, ein Satz Prompts. "Framework" meint *Konvention + Werkzeug*, nicht ein großes System.

---

## Was schon da ist

- [x] `config.yaml` + `schemas/frontmatter.yaml`
- [x] Prompt-Vorlagen: `describe-type`, `make-ruleset`, `make-template`
- [x] Starter-Bibliothek (5 Sets): `_global`, `session-log`, `agent-instructions`, `spec`, `newsletter`
- [x] `new_doc.py` (Jinja2-Rendering) + `validate.py` (JSON-Schema-Validierung des Frontmatter) — mit pytest-Fixtures getestet

## Mögliche nächste Schritte

- [ ] `validate.py` um Section-Check (Pflicht-Überschriften vorhanden?) und Tote-Links-Check erweitern
- [ ] Mehr Starter-Sets (z. B. `meeting-notes`, `adr`)
- [ ] Optionaler Lint speziell für Newsletter-HTML (Inline-CSS / Alt-Text durchsetzen)
- [ ] Pre-Commit-Hook-Beispiel, das `validate.py` über geänderte Docs laufen lässt
```
