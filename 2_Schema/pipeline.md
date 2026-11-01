---
title: "Pipeline — End-to-End Operating Procedure"
type: schema
updated: 2026-11-01
tags:
  - config
  - pipeline
---

# Pipeline: From Input to Output — End-to-End Operating Procedure

This is the concrete operating manual for the full pipeline. The README gives a one-paragraph overview; **this document is what an AI (or a human) actually follows**.

The pipeline has seven stages. Every stage is **user-triggered** — nothing runs automatically.

```
① Record → ② Review → ③ Compile → ④ Maintain → ⑤ Distill → ⑥ Plan → ⑦ Output
```

**What lands in 0_Inbox/ (intake):**

| Input | Where it goes |
|-------|---------------|
| Daily note | `0_Inbox/diary/YYYY-MM-DD.md` |
| Web clipping | `0_Inbox/clippings/` |
| AI conversation log | `0_Inbox/chat-distill/` |
| Video / audio | `0_Inbox/` (transcribe first, or clip into `clippings/`) |

Intake rules: store first, organize later; no editing inside 0_Inbox; tag raw material `#inbox/raw`; leave `processed` unset or `false`. For video/audio: prefer official platform subtitles; otherwise transcribe with a Whisper-class tool; proofread names, brands, products and technical terms against context; segment long content and merge; mark inaudible parts `[inaudible 00:01:23]`; distinguish speakers when multiple.

---

## ① Record — daily note capture

**Goal**: scattered input enters 0_Inbox/ — in, never edited in place.

| Item | Detail |
|------|--------|
| Trigger | Daily diary; say "log this" at task wrap-up |
| Skill | `/rec-1` (minimal append) |
| Output | `0_Inbox/diary/YYYY-MM-DD.md` — appended under the `# Log:` section; append-only, never rewrite |
| Rule | 0_Inbox is read-only; AI only appends frontmatter markers |

## ② Review — weekly review

**Goal**: a week of diary notes compiled into a scannable weekly review.

| Item | Detail |
|------|--------|
| Trigger | "weekly review" / "last week's review" (usually every Monday) |
| Skill | `/wr-1` |
| Input | The 7 diary notes of the last full week (Mon–Sun) |
| Output | `0_Inbox/weekly-review/MMDD-weekly-review.md` |
| Writeback | Mark reviewed diaries `weekly_reviewed: YYYY-MM-DD`; skip notes already marked |

## ③ Compile — AI extracts knowledge units

**Goal**: raw material becomes structured entries in 1_Wiki/ (the core step).

| Item | Detail |
|------|--------|
| Trigger | "compile this" (single) / "compile all" (bulk) |
| Skill | `/by-1` (single) / `/by-a` (bulk; runs the deterministic uncompiled-file scan first) |
| Scan scope | `processed: false` **or missing the field**; **exclude `processed: skip`** |
| Output | The five entry types in `1_Wiki/` + `index.md` updated |
| Report | `3_KBI-log/YYYY-MM-DD-compile-report.md` (stats / entry details / skip categories) |
| Writeback | Original file `processed: true`; body unchanged; `skip` files are never written back |

Steps (by-a):
1. Scan 0_Inbox/ for files with `processed: false` **or missing the `processed` field**; exclude `processed: skip`.
2. For each file, extract knowledge units:
   - concepts → `1_Wiki/concepts/`
   - entities → `1_Wiki/entities/`
   - comparisons → `1_Wiki/comparisons/`
   - frameworks → `1_Wiki/frameworks/`
   - resources → `1_Wiki/resources/`
3. Use the matching template in `1_Wiki/templates/`.
4. Add a `## Source` section (mandatory traceability).
5. Add a `## See also` section; every link carries one of the 8 type labels. No label → no link.
6. Update `1_Wiki/index.md`.
7. Mark the source file `processed: true` (or move to `1_Wiki/archive/`).
8. Write the compile report to `3_KBI-log/YYYY-MM-DD-compile-report.md`.

Quality red lines apply throughout: no fabrication (`confidence: low` when unsure), AI supplements labeled `> 💡 AI note:`, numbers/dates/facts traceable, `author: agent`, links carry the 8 type labels (see TheSchema §3).

## ④ Maintain — health check & link audit

**Goal**: keep the knowledge base honest — health check, gap analysis, link audit.

| Item | Detail |
|------|--------|
| Trigger | "iterate the KB" / "health check" |
| Skill | `/kbi` (runs the deterministic link-audit script first) |
| Checks | coverage gaps / unprocessed files / broken links / hallucination candidates / island entries / link audit |
| Output | `3_KBI-log/YYYY-MM-DD-iteration-report.md` — **read-only recommendations**; fixes are applied only after user confirmation |

## ⑤ Distill — AI conversations into the KB

**Goal**: AI conversations (any client) are filtered into the knowledge base.

| Item | Detail |
|------|--------|
| Trigger | "distill conversations" / "tidy AI chats" |
| Skill | `/chat-distill` |
| Flow | collect conversation logs → three-gate filter → land in `0_Inbox/chat-distill/` → compile → link |
| Report | The compile report appends a "chat-distill stats" section |

## ⑥ Plan — goal breakdown & daily loop

**Goal**: goals broken down and pushed forward by a daily loop.

| Item | Detail |
|------|--------|
| Trigger | "re-plan" / "stage review" (set direction); "daily loop" (daily push) |
| Skill | `/chiselplan` (planning / stage review; writes `2_Schema/chiselplan/plan_2.md` and `plan_3.md`; never touches `plan_1.md`) |
| Daily loop | `/plan-1` (processes only `plan_2.md`) / `/plan-3` (processes only `plan_3.md`) |
| Output | Today's diary task section |

## ⑦ Output — knowledge back into content

**Goal**: compiled knowledge becomes new content — articles, scripts, shares.

| Item | Detail |
|------|--------|
| Trigger | Per blog / content needs |
| Skill | `/blog-1` (articles / project pages / shares; auto frontmatter + English slug) |
| Output | `4_Outputs/` — also where `/by-1` single compiles and `/jh-1` topic maps land |

Rules:
- Output derives from entries; entries remain the source of truth.
- No fabrication: anything not backed by an entry must be marked as inference.

---

## Quality red lines (apply to every stage)

- 0_Inbox/ is read-only (only frontmatter markers are appended).
- No fabrication; mark uncertainty with `confidence`.
- Numbers / dates / facts are traceable: "verified" vs "claimed by one party".
- AI supplements labeled `> 💡 AI note:`.
- AI-compiled content uses `author: agent`.

> **Lane isolation**: each stage stays in its lane — `/wr-1` only reviews, never compiles; `/kbi` only reports, never fixes; `/plan-1` / `/plan-3` only touch their own plan files. All outputs are traceable, reports are read-only, and fixes require user confirmation.
