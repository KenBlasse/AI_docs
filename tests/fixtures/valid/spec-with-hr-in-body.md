---
title: "Spec mit Trennlinie im Body"
type: spec
created: 2026-06-10
status: draft
---

# Body enthält selbst eine Trennlinie

Text oben.

---

Text unten. Die Regex-Variante hätte hier das Frontmatter falsch abgegrenzt.

```yaml
# sogar ein Fake-Frontmatter im Code-Fence:
---
title: "nicht das echte"
---
```
