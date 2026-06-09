# Ruleset: session-log

Ein chronologisches Arbeitsjournal / Changelog. Ein Eintrag pro Arbeitseinheit (Session, Sprint, Tag), der für die *Zukunft* relevant ist.

## Was gehört rein

Ein Eintrag, wenn **mindestens eines** zutrifft:

- Neue Infrastruktur / neues Setup eingerichtet (Dienst, Tool, Integration)
- Nicht-triviale Konfig-Änderung mit Auswirkung über die Session hinaus
- Bug-Fix mit nicht-offensichtlicher Ursache (würde sonst erneut recherchiert)
- Projekt-Meilenstein (released, deployed, MVP fertig)
- Konzept-/Recherche-Ergebnis, das eine Entscheidung getroffen hat

## Was gehört NICHT rein

- Routine-Tasks (Datei lesen, Frage beantworten, Status-Update)
- Reine Reviews ohne Änderung
- Einzelne Lookups (über Versionsverlauf / Suche auffindbar)
- Detail-Wissen, das in ein eigenes Dokument gehört → hier nur ein **Pointer** auf das Detail-Dokument

## Wie ein Eintrag aufgebaut ist

- Überschrift: `## YYYY-MM-DD — <prägnanter Titel>`
- Knapper Block, gegliedert nach: **Symptom / Kontext → Ursache → Lösung → verifiziert**
- Bei Bug-Fixes immer die **Root Cause** nennen, nicht nur den Fix
- Eine `Merke:`-Zeile, wenn es eine wiederverwendbare Lehre gibt

## Pflege

- Neueste Einträge oben.
- Wächst die Datei über ~200 Zeilen: älteste Einträge in ein Archiv (`session-log-YYYY.md`) auslagern.
