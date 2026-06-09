---
title: "{{ title }}"
type: agent-instructions
created: {{ created }}
---

> [!danger] Pflicht-Regeln — kein Skip
> - {{ rule_1 | default("Die wichtigste nicht-verhandelbare Regel.") }}
> - Beim Debuggen: Logs vollständig lesen → Hypothese → eine gezielte Änderung — kein blindes Iterieren.
> - Bei Änderungen an > 2 Dateien oder breaking Changes: Plan zeigen und genehmigen lassen.
> - Secrets niemals committen.

# Projekt: {{ project_name | default("{{ PROJECT_NAME }}") }}

{{ project_description | default("2–3 Sätze: Was, wofür, wer nutzt es.") }}

## Tech-Stack

- **Runtime:** {{ runtime | default("{{ z. B. Node 22 / Python 3.12 }}") }}
- **Framework:** {{ framework | default("{{ z. B. Next.js / FastAPI }}") }}
- **Tests:** {{ tests | default("{{ z. B. Vitest / pytest }}") }}
- **Linting:** {{ linting | default("{{ z. B. ESLint / Ruff }}") }}

## Konventionen

- **Branches:** {{ branches | default("{{ z. B. feature/<slug>, kein Direkt-Push auf main }}") }}
- **Commits:** {{ commits | default("{{ z. B. <type>(<scope>): <was> }}") }}

## Aktueller Fokus

<!-- Vor jeder Session aktualisieren -->
{{ current_focus | default("{{ Was steht gerade an }}") }}
