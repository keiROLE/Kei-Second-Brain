# AGENTS.md — Kei-Second-Brain Vault Guide

This file is the **single authoritative entry point** of Kei-Second-Brain: directory conventions, the authoritative skill inventory, operating rules and quick commands all live here. Detailed rules live in `2_Schema/` (`TheSchema.md` = global rules, `frontmatter.md` = field spec, `naming.md` = naming + PARA, `pipeline.md` = operating manual). **Every AI task in this vault reads this file first.**

`README.md` is the project showcase for GitHub visitors — it introduces the methodology but is **not** a system document; when a rule question arises, this file and `2_Schema/TheSchema.md` are the authority.

---

## Operating Rules (mandatory)

1. **Archive before delete/overwrite**: any deletion, overwrite or rewrite of vault files must first move the original into `1_Wiki/archive/` (prepend `YYYY-MM-DD-` on name conflict), then apply the change. **Permanent deletion is forbidden** (no un-recoverable removal).
2. **Only touch what was named**: do not expand the task scope. Read the original file before modifying it; keep content that was not asked to be changed.

## Core Directory Conventions

| Path | Role |
|------|------|
| `0_Inbox/` | Raw material layer: unprocessed input (diary/, weekly-review/, chat-distill/, clippings/). Read-only, never edited in place. |
| `1_Wiki/` | Knowledge compilation layer: compiled entries (concepts/entities/comparisons/frameworks/resources), templates/, archive/, index.md |
| `2_Schema/` | Configuration layer·rules: TheSchema, frontmatter, naming, pipeline, templates |
| `3_KBI-log/` | Iteration layer: compile reports, iteration reports, link audits, system changelog |
| `4_Outputs/` | Output layer: content compiled from entries (articles, scripts, posts) |
| `.agents/skills/` | Project skills (SKILL.md files + companion scripts). Read the corresponding SKILL.md before using a skill. |

## Document-Type Tasks

Before creating or modifying documents (PDF / Word / PPT / HTML), follow the quality red lines in `2_Schema/TheSchema.md` §8 and the operating manual in `2_Schema/pipeline.md` — no fabrication, traceable facts, structure over decoration.

## Project Skills (authoritative inventory)

This vault ships **9** project skills. Read the corresponding `SKILL.md` under `.agents/skills/<name>/` before using a skill.

> **Single source of truth**: this inventory (name / trigger / responsibility / output) is maintained **only in this file**. README.md names the skills but does not copy this table. When in doubt, follow this file. After modifying a skill, update this table.

| Skill | Name | Trigger | Responsibility | Output |
|-------|------|---------|----------------|--------|
| by-1 | Single compile | "compile this" | read one document → extract knowledge → compile into 1_Wiki/ | wiki entries + index update |
| by-a | Bulk compile | "/by-a", "compile everything" | scan vault for unprocessed files → group & bulk compile (run find_uncompiled.py first) | wiki entries + index + compile report |
| kbi | KB iteration analysis | "/kbi", "health check" | scan vault: gaps / uncompiled / broken links / hallucinations / islands / link audit (run audit_links.py first) | iteration report (read-only) |
| jh-1 | Topic map | "topic map" | scan entries by topic → knowledge map → merge/new suggestions | knowledge map |
| wr-1 | Weekly review | "/wr-1", "weekly review" | compile last complete Mon–Sun 7 diaries → weekly review doc (run review_status.py first) | 0_Inbox/weekly-review/MMDD-last-week-review.md |
| rec-1 | Minimal diary record | "record it" | append minimal lines to today's diary `# 记录：` section | diary append (append-only) |
| chat-distill | AI conversation distill | "distill conversation" | collect chat logs → 3-gate filter → store → compile → link | chat-distill store + wiki entries |
| chiselplan | Planning / phase review | "re-plan", "phase review" | goals → task phases → write plan (optionally creates its own skill) | plan file |
| blog-1 | Blog document generation | — | create article / project page / share docs for the blog | keiROLE blog data dir md |

## Quick Commands

| What you want | Trigger |
|---------------|---------|
| Weekly review | /wr-1 |
| Compile one document | /by-1 |
| Compile everything unprocessed | /by-a |
| KB health check / iteration | /kbi |
| Topic map | /jh-1 |
| Record this into the diary | /rec-1 |
| Distill an AI conversation | /chat-distill |
| Re-plan / phase review | /chiselplan |
| Blog documents | /blog-1 |

## Diary Frontmatter

Diary notes use `weekly_reviewed: YYYY-MM-DD` after being covered by a weekly review; reviewed notes are skipped and not re-processed.
