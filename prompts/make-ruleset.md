# Prompt-Vorlage: Ruleset erstellen

> Gib dieser AI: (1) deinen ausgefüllten `describe-type.md`, (2) eine der mitgelieferten
> `rules/*.md` als Qualitäts-Referenz, (3) diesen Prompt.

---

Du erstellst ein **Ruleset** für einen Dokumenttyp — eine kurze, durchsetzbare Markdown-Datei,
die festlegt, wie Dokumente dieses Typs aufgebaut sein müssen.

Halte dich strikt an diese Maßstäbe:

1. **Kurz und entscheidbar.** Bullet-Points, keine Aufsätze. Jede Regel muss prüfbar oder
   durchsetzbar sein — sonst ist sie ein Wunsch, keine Regel.

2. **Die wichtigste Sektion ist „Was gehört rein / Was gehört NICHT rein".** Formuliere beide
   Listen so, dass man im Zweifelsfall *entscheiden* kann, ob etwas reingehört.

3. **Begründung nur, wo nicht offensichtlich.** Eine `Warum:`-Zeile bei Regeln, deren Sinn
   sich nicht von selbst erschließt.

4. **Kritisches als Callout.** PFLICHT-Regeln als `> [!danger]`, Warnungen als `> [!warning]`,
   Kontext als `> [!info]`.

5. **Markdown bleibt Primärformat.** HTML nur erwähnen, wenn das Zielformat des Dokumenttyps
   zwingend HTML ist (z. B. Email-Newsletter).

Orientiere dich an Struktur und Ton der mitgelieferten Referenz-Datei. Gib **nur** das fertige
Ruleset als Markdown aus, beginnend mit `# Ruleset: <typ>`.
