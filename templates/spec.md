---
title: "{{ title }}"
type: spec
created: {{ created }}
status: {{ status | default("draft") }}
---

# Spec — {{ title }}

> Design-Dokument. Stand: {{ created }}.
> {{ origin | default("Woraus abgeleitet / Kontext.") }}

## 1. Zweck & Kontext

{{ purpose | default("Wozu das Ganze, für wen, woraus abgeleitet.") }}

## 2. Architektur

{{ architecture | default("Die Bausteine und wie sie zusammenhängen. Bei Code: Verzeichnis-/Komponenten-Baum.") }}

## 3. Bewusste Entscheidungen

| Option | Gewählt | Grund |
|--------|---------|-------|
| {{ decision_option | default("Alternative A vs. B") }} | {{ decision_choice | default("…") }} | {{ decision_reason | default("Warum.") }} |

## 4. Ablauf

{{ flow | default("Die Schritte, falls es ein Prozess ist.") }}

## 5. Nicht-Ziele

- {{ non_goal | default("Was bewusst NICHT gebaut wird.") }}

## 6. Offene Punkte

- [ ] {{ open_point | default("Erster offener Implementierungs-Punkt.") }}
