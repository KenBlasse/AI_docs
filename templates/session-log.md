---
title: "{{ title }}"
type: session-log
created: {{ created }}
---

## {{ created }} — {{ title }}

**Symptom / Kontext:**
{{ context | default("Was war die Ausgangslage?") }}

**Ursache:**
{{ cause | default("Root Cause — nicht nur das Symptom.") }}

**Lösung:**
{{ solution | default("Was wurde gemacht.") }}

**Verifiziert:** {{ verified | default("Wie geprüft wurde, dass es wirklich funktioniert.") }}

{% if lesson %}**Merke:** {{ lesson }}{% endif %}
