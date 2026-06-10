# Ruleset: spec

Ein Design- / Konzept-Dokument. Hält fest, *was* gebaut wird und *warum*, **bevor** Code entsteht.

## Was gehört rein

- **Zweck & Kontext** — wozu das Ganze, für wen, woraus abgeleitet.
- **Architektur** — die Bausteine und wie sie zusammenhängen; bei Code ein Verzeichnis-/Komponenten-Baum.
- **Bewusste Entscheidungen** — getroffene Trade-offs, am besten als Tabelle „Option A vs. B → Grund".
- **Ablauf** — die Schritte, falls es ein Prozess ist.
- **Nicht-Ziele** — was bewusst *nicht* gebaut wird. Verhindert Scope Creep.
- **Offene Punkte** — als Checkliste für die Implementierung.

## Was gehört NICHT rein

- Fertiger Code oder Implementierungs-Details, die sich noch ändern.
- Entscheidungen ohne Begründung („wir nehmen X" ohne *warum*).
- Status-Tracking (gehört ins session-log oder Task-Board).

## Form

- Status im Frontmatter (`draft` / `approved` / `implemented`).
- Ein Kurz-Zitat-Block oben (`>`) mit Stand und Herkunft des Dokuments.
- Entscheidungen als Tabelle, nicht als Fließtext — macht Trade-offs vergleichbar.

> **INFO — Designprinzip:**
> Eine gute Spec erklärt **warum**, nicht nur **was**. Das *Was* veraltet, das *Warum* hilft beim nächsten Umbau.
