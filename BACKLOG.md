# Backlog — offene Verbesserungen aus der Code-Review

Stand: 2026-06-10. Umgesetzt sind **#1 (echtes Frontmatter-Parsing + JSON Schema)**,
**#3 (Datumsformat wird erzwungen)** — siehe `scripts/validate.py`,
`schemas/frontmatter.yaml`, `tests/` —, **#6 (Callout-Anspruch tool-neutral)**
und **#2 (eine Quelle der Wahrheit für Felder)**.

Die folgenden Punkte sind bewusst zurückgestellt, nach Wirkung sortiert.

---

## ✅ #2 — Eine einzige Quelle der Wahrheit für Felder (erledigt)

**War:** Pflichtfelder standen doppelt — maschinenlesbar in
`schemas/frontmatter.yaml` und als Prosa in den Rule-Files. Drift garantiert.

**Umgesetzt:** `scripts/sync_fields.py` generiert die „Frontmatter-Felder"-Tabelle
jeder Rule aus dem Schema (Marker `<!-- FIELDS:start/end -->`). Das Schema ist
alleinige Quelle; `_global.md`/`spec.md`-Prosa verweist nur noch darauf.
`--check`-Modus meldet Drift zwischen Schema, Rule-Tabellen und
Template-Frontmatter (pre-commit-/CI-tauglich), abgesichert durch `tests/test_sync_fields.py`.

---

## #4 — Newsletter (HTML) ist ein blinder Fleck

**Problem:** Der HTML-Typ ist komplett von der Validierung ausgenommen — also
genau der Typ, der am ehesten kaputtgeht (Jinja2→HTML, Mail-Client-Quirks).

**Nächster Schritt:**
- Template rendern und mit `html.parser`/`lxml` auf Wohlgeformtheit prüfen.
- Optional: Pflicht-Kontextvariablen (Betreff, Preheader) deklarieren und prüfen,
  dass sie gesetzt sind.

---

## #5 — new_doc.py: Kontextfelder & Robustheit

**Problem A:** Das Template hat `{{ context }}`, `{{ cause }}`, `{{ lesson }}`
(bzw. `purpose`, `architecture` …) mit Defaults, aber `render()` übergibt nur
`title` und `created`. Alle optionalen Felder bleiben Platzhaltertext.
→ Entweder CLI-Flags (`--field cause="..."`) durchreichen, **oder** ehrlich
dokumentieren, dass das Template bewusst nur ein Gerüst mit Prompts ist (dann
sind die `default()`-Werte überflüssig).

**Problem B (Robustheit):**
- `slugify("###")` → leerer String → Datei heißt `.md`. Fallback auf z.B.
  `untitled` + Kollisionsschutz (existierende Datei wird sonst kommentarlos
  überschrieben).
- Kein Abfangen von Config-/Template-Fehlern (KeyError bei kaputter Config).

---

## ✅ #6 — Callout-Anspruch ehrlich machen (erledigt)

**War:** `rules/_global.md` verkaufte `> [!danger]` als format-übergreifend —
Obsidian/Docusaurus-Syntax, die in reinem GitHub/Pandoc/MkDocs (default) nur als
simples Blockquote ohne Label rendert.

**Umgesetzt:** Tool-neutraler Default (Blockquote + Bold-Label,
`> **PFLICHT:** / **WARNUNG:** / **INFO:**`) in der Rule empfohlen, mit
`**Warum so neutral:**`-Begründung. Alle aktiven Callout-Blöcke in `rules/`,
`prompts/`, `templates/` und `README.md` entsprechend umgestellt. Wer in einer
Callout-fähigen Umgebung arbeitet, kann das typ-spezifische Ruleset überschreiben.

---

## #7 — Tooling-Hygiene (Framework für andere)

- **Tests:** Grundstein gelegt (`tests/`, je valide + invalide Fixtures pro Typ).
  Noch offen: Fixtures für `agent-instructions`, Newsletter-Tests (hängt an #4).
- **CI:** GitHub Action, die `validate.py` über alle `out/`-Dokumente + Fixtures
  laufen lässt.
- **Pre-commit-Hook** mit `validate.py` — der eigentliche Killer-Use-Case: ein
  Doc, der gegen sein eigenes Ruleset verstößt, wird beim Commit blockiert.
  (`validate.py` nimmt jetzt mehrere Pfade als Argumente — pre-commit-tauglich.)
- **Meta-Schema:** `config.yaml` und `schemas/frontmatter.yaml` selbst gegen ein
  Meta-Schema validieren, damit ein Tippfehler in der Config nicht erst zur
  Laufzeit auffällt.
