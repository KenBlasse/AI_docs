# Prompt-Vorlage: Template erstellen

> Gib dieser AI: (1) deinen ausgefüllten `describe-type.md`, (2) das passende Ruleset
> (selbst erstellt oder mitgeliefert), (3) eine mitgelieferte `templates/*` als Referenz,
> (4) diesen Prompt.

---

Du erstellst ein **Template** für einen Dokumenttyp — ein Gerüst, das ein Mensch oder eine AI
mit Inhalt füllt, sodass das Ergebnis automatisch dem Ruleset entspricht.

Regeln:

1. **Jinja2-Syntax.** Platzhalter als `{{ feld }}`, optionale Defaults als
   `{{ feld | default("Hinweis was hier hin soll") }}`. Schleifen mit `{% for %}` nur, wenn
   der Typ wiederholte Elemente hat (z. B. mehrere Abschnitte).

2. **Frontmatter zuerst** (außer bei HTML-Zielformat): YAML-Block mit allen im Ruleset/Schema
   geforderten Pflichtfeldern, `title`/`type`/`created` immer dabei.

3. **Struktur folgt dem Ruleset.** Jede Pflicht-Section aus dem Ruleset wird im Template als
   leere, beschriftete Section vorgezeichnet — der Nutzer sieht sofort, was zu füllen ist.

4. **Format = Zielformat.** Markdown-Typ → `.md`-Template. HTML-Zielformat (Newsletter o. ä.)
   → echtes, mail-client-gehärtetes HTML mit Inline-CSS und Tabellen-Layout, kein Markdown.

5. **Keine Beispieldaten fest eincodieren** — nur Platzhalter und Default-Hinweise.

Orientiere dich an der mitgelieferten Referenz. Gib **nur** das fertige Template aus.
