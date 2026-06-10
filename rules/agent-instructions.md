# Ruleset: agent-instructions

Eine Instruktions-Datei für einen AI-Assistenten in einem Projekt (z. B. eine `CLAUDE.md`, `AGENTS.md` oder vergleichbar). Sagt der AI, *wie* sie in diesem Projekt arbeiten soll.

## Was gehört rein

- **Kritische Pflicht-Regeln zuerst** — als abgesetzter Block mit `**PFLICHT:**`-Label, ganz oben.
- **Projekt-Kontext** in 2–3 Sätzen: Was, wofür, wer nutzt es.
- **Tech-Stack** als knappe Liste (Runtime, Framework, DB, Tests, Linting).
- **Konventionen**, die nicht aus dem Code ablesbar sind (Branch-Schema, Commit-Format, Fehler-Format).
- **Aktueller Fokus** — was gerade ansteht; pro Session aktualisiert.

## Was gehört NICHT rein

- Globale Regeln, die für *alle* deine Projekte gelten → die gehören in eine globale Instruktions-Datei, nicht hierher.
- Informationen, die im Code stehen (Ordnerstruktur, die offensichtlich ist).
- Secrets, Tokens, private Pfade.
- Optionale Sektionen, die auf dieses Projekt nicht zutreffen — weglassen.

## Form

> **PFLICHT — Kurz halten:**
> Projektspezifischer Inhalt unter ~80 Zeilen. Eine Instruktions-Datei, die niemand zu Ende liest, wird auch von der AI überflogen.

- Pflicht-Regeln als `**PFLICHT:**`-Block, Abweichungs-Protokolle als `**WARNUNG:**`-Block.
- Code-Blöcke für Commands; bei verschachtelten Fences `~~~` statt ` ``` ` verwenden, damit Copy-Paste sauber bleibt.
- Platzhalter im `{{ FELD }}`-Format für Werte, die der Nutzer einsetzt.
