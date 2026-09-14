---
title: "Frontmatter Field Specification"
type: schema
updated: 2026-09-14
tags:
  - config
  - frontmatter
---

# Frontmatter Field Specification

The measured inventory of YAML frontmatter fields used across the vault: required / optional / deprecated.

---

## 1. 1_Wiki entries (compiled knowledge)

| Field | Required | Notes |
|-------|----------|-------|
| `title` | Yes | Entry title, in double quotes if it contains special chars |
| `type` | Yes | Matches the containing directory: `concept` / `entity` / `comparison` / `framework` / `resource` |
| `created` | Yes | `YYYY-MM-DD` |
| `source` | Yes | Full path of the source file(s). Compilation traceability. |
| `confidence` | Yes | `high` / `medium` / `low` |
| `tags` | Yes | ≥ 3 tags: type + topic + PARA category |
| `aliases` | Optional | Alias array to reduce navigation ambiguity |
| `author` | Optional | `cc` for AI-produced content |
| `entity_kind` | Required for entities | `person` / `organization` / `project` / `product` |

Example:

```yaml
---
title: "Attention Economics"
type: concept
created: 2026-09-14
source: 0_Inbox/clippings/attention-economics.md
confidence: high
tags:
  - concept
  - media
  - para/resource
aliases:
  - attention economy
author: cc
---
```

## 2. 0_Inbox / diary

| Field | Required | Notes |
|-------|----------|-------|
| `processed` | Recommended | `true` / `false`; missing field also counts as unprocessed when scanning |
| `abstract` | Optional | One-line summary |
| `weekly_reviewed` | Optional | Date value `YYYY-MM-DD` after the weekly review covered it |

## 3. Deprecated fields

| Field | Status | Replacement |
|-------|--------|-------------|
| `related` | Deprecated | Links go in the `## See also` section at the end of the entry |
| `links` | Deprecated | Same as above |
