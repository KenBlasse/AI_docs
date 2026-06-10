# Backlog — Verbesserungen aus der Code-Review

Stand: 2026-06-10. **Alle Punkte umgesetzt** (#1–#7):

- **#1** echtes Frontmatter-Parsing + JSON Schema, **#3** Datumsformat erzwungen
- **#2** eine Quelle der Wahrheit für Felder (`sync_fields.py`)
- **#4** Newsletter-HTML-Validierung (`validate_newsletter.py`)
- **#5** `new_doc.py`: Kontextfelder (`--field`) & Robustheit
- **#6** Callout-Anspruch tool-neutral
- **#7** Tooling-Hygiene (Fixtures, CI, Pre-commit, Meta-Schema)

Details je Punkt unten.

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

## ✅ #4 — Newsletter (HTML) ist ein blinder Fleck (erledigt)

**War:** Der HTML-Typ war komplett von der Validierung ausgenommen — genau der
Typ, der am ehesten kaputtgeht (Jinja2→HTML, Mail-Client-Quirks).

**Umgesetzt:** `scripts/validate_newsletter.py` prüft fertiges HTML (stdlib
`html.parser`, keine Extra-Dependency): Wohlgeformtheit (balancierte Tags),
Pflicht-Kontext (`title` gesetzt) und die Härtungsregeln aus `rules/newsletter.md`
(kein `<script>`, `alt`-Texte, `max-width`-Container, kein `<style>` im `<head>`).
`--template` rendert + prüft das Standard-Template. Abgesichert durch
`tests/test_validate_newsletter.py`; Rule + Schema-Kommentar verweisen darauf.

---

## ✅ #5 — new_doc.py: Kontextfelder & Robustheit (erledigt)

**A (Kontextfelder):** `--field KEY=WERT` (mehrfach) reicht optionale Felder ins
Template-Render durch; Defaults bleiben als Fallback. `templates/spec.md`
nutzt jetzt `status: {{ status | default("draft") }}`, damit der Status
überschreibbar ist.

**B (Robustheit):**
- `slugify("###")` → `untitled` statt `.md`.
- Kollisionsschutz: gleicher Slug wird nummeriert (`-2`, `-3`); `--force`
  erzwingt Überschreiben.
- Config-/Template-Fehler werden abgefangen (`KeyError`/`YAMLError`/`TemplateError`)
  → klare Meldung + Exit-Code statt Traceback.

**Sicherheit:** Jinja2-`autoescape` via `select_autoescape` für HTML-Templates
(Newsletter) — `--field`-Werte werden im HTML escaped (kein XSS). Markdown bleibt
unescaped. Abgesichert durch `tests/test_new_doc.py`.

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

## ✅ #7 — Tooling-Hygiene (erledigt)

- **Tests/Fixtures:** valide + invalide Fixtures jetzt auch für `agent-instructions`;
  Newsletter über `test_validate_newsletter.py` (aus #4). Insgesamt 48 Tests.
- **CI:** `.github/workflows/ci.yml` — bei Push/PR: pytest + alle Validatoren
  (`validate_config`, `sync_fields --check`, `validate_newsletter --template`,
  `validate.py` über Fixtures/`out`).
- **Pre-commit-Hook:** `.pre-commit-config.yaml` (lokale Hooks) blockiert beim
  Commit Docs, die gegen Schema/Härtung/Sync verstoßen.
- **Meta-Schema:** `scripts/validate_config.py` prüft `config.yaml` und
  `schemas/frontmatter.yaml` strukturell + Kreuz-Konsistenz (jeder Typ hat Schema,
  referenzierte Dateien existieren) — Tippfehler fällt vor der Laufzeit auf.
