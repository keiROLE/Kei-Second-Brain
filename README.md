# Kei-Second-Brain

**An AI-compiled second brain.** A complete, open methodology for running a personal knowledge base where **AI compiles, maintains and outputs** — not just stores.

This repository is a fully working system: a documented architecture, 9 reusable AI skills, and a complete sample knowledge base that demonstrates the whole pipeline.

> Chinese version: [README.zh.md](README.zh.md)（中文版，以英文版为准）

---

## What this is

Kei-Second-Brain is a personal knowledge-base methodology turned into a reusable system. The core idea:

> **Knowledge is not stored — it is compiled.**

Raw material (diary notes, clippings, AI conversations, transcripts) flows into an inbox. An AI agent compiles it into structured knowledge entries. A health-check pass keeps the vault honest. And the compiled knowledge feeds back into new content — articles, video scripts, posts.

The repo contains three things:

| Part | Location | What it is |
|------|----------|------------|
| **The system** | `2_Schema/` | The rules: architecture, frontmatter spec, naming, link rules, pipeline manual |
| **The skills** | `.agents/skills/` | 9 AI skills (compile, iterate, review, plan...) that run the system |
| **The example** | `0_Inbox/` `1_Wiki/` `3_KBI-log/` `4_Outputs/` | A complete sample vault showing every stage of the pipeline — format demonstrations (one entry per type, placeholders), plus one **real** capture→compile run (see "A real example") |

## How it differs from other methods

| Method | What it gives you | What this system adds |
|--------|-------------------|-----------------------|
| **PARA** | A classification skeleton (Projects / Areas / Resources / Archive) — this system **borrows its tag system**; most entries carry PARA tags | PARA only says *where things go*. Kei-Second-Brain adds an **AI compile layer** (raw material becomes knowledge entries automatically), a **maintain layer** (health checks, link audits, hallucination detection) and an **output layer** (knowledge feeds back into content). |
| **Zettelkasten** | Atomic notes linked into a web of thought — this system **borrows the linking idea** (typed `## See also` links) | ZK is handwritten. Here entries are **compiled by AI**, with quality red lines (no fabrication, source traceability, confidence levels) to prevent hallucination. |

**In one sentence**: PARA provides the skeleton, Zettelkasten provides the linking idea, Kei-Second-Brain provides the **AI compile pipeline + active maintenance + knowledge-backed output** — the three things that make a knowledge base actually grow.

## Prerequisites

You need two tools:

1. **Obsidian** — the vault runs in Obsidian (free). Any recent version works.
2. **An AI client that supports custom skills/agents** — e.g. Claude Code, or any agent that can read markdown instructions and act on files. The skills in `.agents/skills/` are plain markdown instruction files (SKILL.md); your AI client just needs to be able to load and follow them.

No coding, no server, no database required.

## Architecture

```
0_Inbox/                             1_Wiki/                            2_Schema/
Raw material layer (read-only)       Knowledge compilation layer        Configuration layer
diary/  weekly-review/               concepts/  entities/               TheSchema (rules)
chat-distill/  clippings/            comparisons/  frameworks/          AGENTS (AI behavior)
                                      resources/  index.md              frontmatter/naming
                                                                        pipeline (operating manual)
3_KBI-log/                           4_Outputs/
Iteration layer                      Output layer
compile reports / iteration reports  articles, scripts, posts
```

| Layer | Role | Who writes |
|-------|------|------------|
| `0_Inbox/` | Raw material — source of truth | You (append-only) |
| `1_Wiki/` | Compiled knowledge entries | AI (via skills) |
| `2_Schema/` | The rules the vault runs on | You + AI |
| `3_KBI-log/` | Reports: compiles, health checks, audits | AI |
| `4_Outputs/` | Content compiled from entries | AI (from wiki) |

## The pipeline (one paragraph)

**Input**: video transcripts, web clippings, AI conversations and daily notes land in `0_Inbox/`. **Compile**: `/by-1` (single) or `/by-a` (bulk) turns them into typed entries in `1_Wiki/` — concept, entity, comparison, framework, resource — each with a source, a confidence level and typed links. **Maintain**: `/kbi` scans for gaps, broken links, islands and hallucinations and outputs a read-only iteration report. **Output**: entries are pulled into articles, video scripts and posts (e.g. `/blog-1`). Nothing runs automatically — every stage is user-triggered. The full operating manual is `2_Schema/pipeline.md`.

## A real example — capture → compile

The sample vault contains one **real** capture→compile run (everything else is a format skeleton):

1. **Capture** — the author's own video transcript about choosing a monitor was clipped into `0_Inbox/clippings/xiaojian-guo-monitor-episode.md`: real input, kept verbatim.
2. **Compile** — `/by-1` turned it into a typed entry: `1_Wiki/frameworks/monitor-selection-guide.md`.

The whole loop — one person, from a video to a published article, every skill used — is told as a story in **[WORKFLOW.md](WORKFLOW.md)**.

## Quick start

### Option A — explore the example first (recommended)

```bash
git clone https://github.com/keiROLE/Kei-Second-Brain.git
# open this folder in Obsidian ("Open folder as vault")
# browse 0_Inbox/ and 1_Wiki/ — start with the two "real example" files listed above
```

The repository *is* a complete sample vault. `0_Inbox/`, `1_Wiki/`, `2_Schema/`, `3_KBI-log/` and `4_Outputs/` show every stage of the pipeline — one entry per type as a format demonstration, plus one real capture→compile run.

### Option B — let an AI build your own

**You can hand this README to any AI assistant and ask it to set up the vault for you.** The AI will:

1. Create the five top-level directories (`0_Inbox/`, `1_Wiki/`, `2_Schema/`, `3_KBI-log/`, `4_Outputs/`) and their subdirectories.
2. Ask you to copy `2_Schema/` (rules) and `.agents/skills/` (skills) from this repo.
3. Walk you through your first cycle: write a diary note → run `/by-1` on it → see the compiled entry.

### Option C — build from scratch manually

1. New Obsidian vault.
2. Copy `2_Schema/` and `.agents/skills/` from this repo.
3. Read `2_Schema/TheSchema.md` (the rules) and `2_Schema/pipeline.md` (the operating manual).
4. Start writing raw notes in `0_Inbox/`, then trigger `/by-a` to compile them.

## Repository map

| Path | What |
|------|------|
| `AGENTS.md` | AI behavior contract (repo root — read first by AI clients) |
| `2_Schema/TheSchema.md` | Architecture, tags, 8 link types, quality red lines, workflows |
| `2_Schema/frontmatter.md` | Frontmatter field spec |
| `2_Schema/naming.md` | Naming + PARA classification |
| `2_Schema/pipeline.md` | End-to-end operating manual (input → output) |
| `.agents/skills/` | by-1, by-a, kbi, jh-1, wr-1, rec-1, chat-distill, blog-1, chiselplan |
| `WORKFLOW.md` | The whole system as a story — one person, one loop, every skill used |
| `0_Inbox/clippings/xiaojian-guo-monitor-episode.md` | Real clipped material (the example input) |
| `1_Wiki/frameworks/monitor-selection-guide.md` | The entry it was compiled into (the example output) |
| `4_Outputs/` | Output-layer format examples (articles compiled from entries) |

## Support & maintenance boundaries

- This is a **personal methodology shared in public — not a community project**.
- Issues are welcome: ask questions, report problems.
- **No promise of regular updates**; major versions ship irregularly as the author's own vault evolves.
- Pull requests are merged after discussion; large unrequested changes are not accepted.
- The sample content is fictional demonstration; support is limited to the methodology, not the demo data.

## License

**CC BY-NC 4.0** (Attribution-NonCommercial 4.0 International).

You are free to share and adapt, under the terms: attribution, and non-commercial use only. Full legal code: <https://creativecommons.org/licenses/by-nc/4.0/legalcode>. See [LICENSE](LICENSE).

---

*Built by Kei — AI-compiled knowledge, for people who want their notes to think back.*
