---
title: "Diary Template"
type: template
---

# Daily Note — YYYY-MM-DD

> Daily note format. Raw capture only: append, never rewrite. Compilation happens later via `/by-1` / `/by-a`.

```yaml
---
abstract: Diary
author: Kei
tags:
  - diary
processed: false
---
```

## 记录 / Log

What happened — one line per event. Tags (`#event`, `#project`) go at the **start** of each block, before the text. Link produced artifacts: `[[entry-name]]`.

## 输入 / Input

What you consumed — `#learn` / `#method` blocks with raw notes in your own words. This is the raw material the compile skills turn into wiki entries.

## 计划 / Plan

Link the active plan file (`[[plan_2]]`) and list today's temporary tasks as checkboxes.
