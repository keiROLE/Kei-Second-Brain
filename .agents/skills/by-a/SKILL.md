---
name: by-a
description: Bulk-compile all new content into the LLM Wiki — scan the vault for unprocessed files and batch-compile them into 1_Wiki/. Triggers on "/by-a", "compile everything" or "process all new content".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# by-a — Bulk Compile

You are the bulk compile engine of the LLM Wiki. Your job: scan the whole vault in one pass, find every document not yet compiled, extract knowledge and structure it into the wiki.

## Trigger

User says "/by-a", "compile everything", "process all new content", or similar.

## Workflow

### Step 0: Discover new files

Scan the following locations for .md files with `processed: false` or **missing the `processed` field**:

1. `0_Inbox/` — all .md files in all subdirectories (exclude .png/.html etc.)
2. Other source folders the user points to.

**Exclusion rules**:
- Skip files already compiled (cross-check the "Source" column of `1_Wiki/index.md`).
- Skip pure password/secret files.
- Skip fiction/creative drafts.
- Skip images and non-.md files.

**Dedup rules**:
- Read the `source` field in frontmatter when present.
- Or use the relative file path as the unique id.
- Files already listed as sources in `1_Wiki/index.md` → skip.

### Step 1: Group by topic

Group new files by topic so each group is processed together. Grouping is your judgment call per vault; a generic example:

| Group | What goes in |
|-------|--------------|
| AI knowledge | ai/ notes, prompts |
| Mindset | cognition/thinking notes |
| Side business | business/ projects |
| Sales | sales-related notes |
| Media operations | content/self-media notes |
| Other | everything remaining |

### Step 2: Bulk compile

For every file in every group, run the same compile flow as `/by-1`:

1. Read the full file.
2. Split into knowledge units.
3. Classify (concept/entity/comparison/framework/resource).
4. Dedup against 1_Wiki/.
5. Create or supplement entries.
6. Use the correct template and frontmatter.

Bulk optimizations:
- Process groups in parallel when possible (independent groups).
- Update index.md once at the end.

### Step 3: Fragment handling

Scan files whose names contain "misc"/"untitled":
- Split by blank-line paragraphs.
- Classify each paragraph (see `2_Schema/naming.md` classification).
- Wiki-worthy → compile into entries.
- Passwords/tasks/creative → ignore or route to the matching PARA directory.

### Step 4: Update index.md

1. Read `1_Wiki/index.md`.
2. Add all new entries to the quick-nav, grouped by type.
3. Update the statistics.
4. Ensure no duplicate entries.
5. **Write back `processed` markers (mandatory)**: set `processed: false` → `true` on every source file compiled or scanned-and-skipped this round, **in the same pass as the index update**. Never update the index without writing back markers — otherwise the next scan re-processes the same files.

### Step 5: Output the compile report (with details)

**Output location (mandatory)**: write the report to `3_KnowledgeBaseIterationLog/YYYY-MM-DD-compile-report.md`. The compile report is the audit trail of how the knowledge base evolved — what was compiled, what was skipped.

```yaml
---
title: "by-a Bulk Compile Report (YYYY-MM-DD)"
type: analysis-report
created: YYYY-MM-DD
source_skill: "/by-a"
tags:
  - analysis
  - compile
  - para/resource
---
```

Body:
- Metrics table: files scanned / skipped / new entries / supplemented / ignored / final wiki count
- Type statistics before vs after (concept/entity/comparison/framework/resource)
- Per-group statistics
- New entries detail (name, source file, note)
- Supplemented entries detail
- Skipped files by category (already-compiled / passwords / fiction / tasks / meetings...)
- Recommended next steps (links to complete, suggested new entries, files worth compiling next)

### Step 6: (merged into Step 5 — no separate log file)

## Rules

1. **Safety first**: scan before writing; do not write too many files at once.
2. **Never modify originals**: source files stay read-only (frontmatter markers excepted).
3. **Label AI supplements**: `> 💡 AI note: ...`.
4. **Incremental compiling**: if more than ~20 new files, process in 2-3 rounds.
5. **Date format**: `YYYY-MM-DD`.
6. **Author marker**: `author: cc`.
7. **Links are earned, not assigned**: cross-links only in `## See also` with type labels; no label → no link.
8. **`processed` write-back is mandatory**: mark sources immediately, in the same pass as the index update.

## Difference from /by-1

| Dimension | /by-1 (single) | /by-a (bulk) |
|-----------|----------------|--------------|
| Input | one user-specified file | auto-scan of the vault |
| Scope | 1 file | all unprocessed files |
| Strategy | careful, one by one | grouped, parallel |
| When | a new note arrives | regular tidying / large batches |
