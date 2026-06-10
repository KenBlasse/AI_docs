# Backlog — offene Verbesserungen aus der Code-Review

Stand: 2026-06-10. Umgesetzt sind **#1 (echtes Frontmatter-Parsing + JSON Schema)**,
**#3 (Datumsformat wird erzwungen)** — siehe `scripts/validate.py`,
`schemas/frontmatter.yaml`, `tests/` —, **#6 (Callout-Anspruch tool-neutral)**
, **#2 (eine Quelle der Wahrheit für Felder)**,
**#5 (new_doc.py: Kontextfelder & Robustheit)** und
**#4 (Newsletter-HTML-Validierung)**.

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
