# Sample Knowledge Base — Format Demonstration

> **Fictional content disclaimer**: This sample vault is a format demonstration only. All concrete content has been removed — entries keep their structure (frontmatter + sections) with placeholders. It is not related to any real account or person. 本示例库仅为格式演示，具体内容已全部移除，与任何真实账号或个人无关。

This folder is a complete, runnable example of the Kei-Second-Brain system — a small Obsidian vault showing how one person runs the full pipeline: **input → compile → maintain → output**. Every file keeps the *real format* of the system (the exact frontmatter and section structure your own vault will use), with placeholder content.

## How the sample maps to the pipeline

| Pipeline stage | Where in this sample |
|----------------|----------------------|
| ① Input (capture) | `0_Inbox/` — diary, weekly review, distilled AI conversation, web clipping (one format example each) |
| ② Transcribe | (implied — transcripts would land in `0_Inbox/` too) |
| ③ Compile | `1_Wiki/` — one entry per type (concept / entity / comparison / framework / resource) |
| ④ Maintain | `3_KnowledgeBaseIterationLog/` — compile report + iteration report (format examples) |
| ⑤ Output | `4_outputs/` — an article format compiled from the wiki entries |

## Suggested reading order

1. `README.md` (repo root) — what the system is and how to set up your own
2. `2_Schema/TheSchema.md` — the rules that govern this vault
3. This folder, in order:
   - `0_Inbox/diary/` — the diary format (raw material, unprocessed)
   - `3_KnowledgeBaseIterationLog/2026-09-13-compile-report.md` — what /by-a produces
   - `1_Wiki/` — the compiled-entry formats
   - `3_KnowledgeBaseIterationLog/2026-09-13-iteration-report.md` — what /kb-iter finds
   - `4_outputs/output-sample.md` — the output format

## The loop, in one paragraph

A capture lands in the diary (input). The compile skill turns it into a wiki entry (compile). The iteration skill checks the vault and suggests what is missing (maintain). An article or script pulls from the entries (output). Next week's diary records what that content brought back — and the loop runs again.

> The configuration layer (2_Schema, skills, directory names) is English-only; the example layer is bilingual (`*.md` = English, `*.zh.md` = Chinese). English is authoritative.
