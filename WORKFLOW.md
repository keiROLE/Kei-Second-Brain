# From a Douyin Video to a Published Article

> A real-feeling person's first complete loop through Kei-Second-Brain — every skill, in one story. The person is **fictional**; the example files it touches are **real files in this repo** — open them alongside the story.

The story takes place in the week of **2026-09-15**. Every skill in `.agents/skills/` appears exactly once.

---

## The person

**Alex** recently started learning PC hardware from zero. No background in building computers — just a curiosity about how machines work, and a habit of collecting notes that never came together. This week Alex found a method that actually closes the loop.

---

## Step 1 · Capture — a video becomes a clipping

Alex scrolled Douyin and found **小坚果搞机 (Xiaojian Guo)**, a DIY-PC creator, explaining **how to pick a monitor** — size, resolution, refresh rate. The video was useful, so Alex did what the system expects:

1. Copied the video link into a **video-to-text tool**.
2. Got the verbatim transcript.
3. Clipped the transcript into the vault, kept **verbatim, unedited**, as a raw clipping:

```
0_Inbox/clippings/xiaojian-guo-monitor-episode.md
```

> 📄 **Real file — open it.** It is the input material of the whole system: raw, truthful, unattributed knowledge not yet. Note what it does *not* have: no structure, no type, no tags. That is the point of an inbox — it only collects.

The **capture principle**: a clipping is input material. Never edit it while capturing; the compile step decides what the knowledge is.

---

## Step 2 · Compile — raw material becomes knowledge

With material in the inbox, Alex ran the compile skill on it:

```
/by-1   →   "compile this clipping"
```

The agent read the clipping, classified it (a **framework** — it gives steps/criteria for choosing a monitor), and wrote a typed entry:

```
1_Wiki/frameworks/monitor-selection-guide.md
```

> 📄 **Real file — open it.** Notice what compile added:
> - **Frontmatter** — `type: framework`, `source: 0_Inbox/clippings/xiaojian-guo-monitor-episode.md` (traceability), `confidence: high`, `author: agent`.
> - **Structured body** — the three decision axes as tables (size / resolution / refresh rate).
> - **Honest filtering** — the video's marketing line ("DM me your budget") was **dropped**: it is not knowledge.
> - **`## See also`** — empty on purpose: no established relation yet, and links are earned, not assigned.

Over the next days Alex kept watching (CPU, GPU, RAM episodes), clipped each one, then ran the batch version:

```
/by-a   →   "compile everything"
```

It scanned the inbox, compiled all unprocessed clippings, wrote back `processed: true`, and produced a compile report:

```
3_KBI-log/2026-09-15-compile-report.md
```

> *(The example vault keeps one entry per type, so the CPU/GPU/RAM entries are illustrative — your vault will grow them for real.)*

The **compile principle**: raw material becomes knowledge only here — typed, sourced, confidence-rated, link-earned.

---

## Step 3 · Distill & record — conversations and daily notes

Not all knowledge comes from videos. Alex asked the AI "which GPU is enough for a 2K monitor?", and the conversation contained a genuinely reusable conclusion. That is what `/chat-distill` is for — it filters agent conversations by value and lands only the keepers:

```
/chat-distill   →   "distill this week's conversations"
```

The kept excerpt became a raw note with conversation-specific frontmatter (`source_type: chat`, `source_agent: agent`), then was compiled into a wiki entry like any other material:

```
0_Inbox/chat-distill/2026-09-15-agent-example.md
```

Meanwhile, every evening Alex logged the day's progress into the daily note with `/rec-1` (append-only, one line per event):

```
/rec-1   →   "log today's progress"
0_Inbox/diary/2026-09-15.md
```

The **record principle**: diary is raw material too — append, never rewrite.

---

## Step 4 · Iterate — keep the vault honest

By now the wiki had a dozen entries. Alex ran the health check:

```
/kbi   →   "knowledge base iteration"
```

The agent scanned the whole vault and produced a **read-only** iteration report:

```
3_KBI-log/2026-09-15-iteration-report.md
```

What it found:

| Finding | What Alex did |
|---------|---------------|
| A broken link in an old entry | fixed the pointer |
| An isolated entry with no real relation | left it alone — isolation can be intentional |
| A knowledge gap: no "GPU tier list" entry | asked the AI GPU-tier questions, then filled it via `/chat-distill` |
| A suspected hallucination | deleted it (see: AI proposals are labeled `> 💡 AI proposal (unverified)`) |

Alex also ran the topic aggregator to see the whole hardware topic in one map:

```
/jh-1   →   "aggregate the PC hardware topic"
```

It produced a knowledge map (which entries are parent/child/sibling, where links are missing) — the topic view that decides what to learn next.

The **iterate principle**: the vault is never "done" — health checks and topic maps are what keep compiled knowledge trustworthy.

---

## Step 5 · Plan & review — direction and reflection

Learning needs a plan, so Alex kicked off a project with `/chiselplan`:

```
/chiselplan   →   "plan my PC-learning project"
```

It wrote a plan file with a final goal and task phases (foundation → build → deep-dive). During the week it can even create a companion daily-loop skill (default name `plan-1`) that rolls today's 3-5 tasks from the current phase — but Alex kept it simple this week.

At week's end, `/wr-1` compiled the seven diary notes into a weekly review:

```
/wr-1   →   "weekly review"
0_Inbox/weekly-review/0915-last-week-review.md
```

The **plan & review principle**: raw material feeds forward (plan) and backward (review) — the loop stays self-correcting.

---

## Step 6 · Output — knowledge becomes content

Finally, Alex wanted to write up what was learned. `/blog-1` turns compiled entries into articles:

```
/blog-1   →   "article: PC Hardware Notes, from my wiki entries"
```

It generated a markdown file with frontmatter + slug in the Output layer:

```
4_Outputs/pc-hardware-notes.md
```

> The article was written **from the compiled entries**, not from memory — sources and confidence levels carried over. Alex published it on a personal blog. A reader asked a question about monitor refresh rates; that question became the next video Alex watched, the next clipping, the next compile.

**The output principle**: knowledge that never leaves the vault is a diary. Output closes the loop — and the loop feeds itself.

---

## The whole loop, one picture

```
        capture               compile                maintain               output
video/transcript ──▶ 0_Inbox ──▶ 1_Wiki ──▶ kbi / jh-1 checks ──▶ 4_Outputs ──▶ article
     ▲                  │            │                │                   │
     │                  │            ▼                ▼                   │
     └──── new questions ◀── diary / weekly review ◀── plan / distill ◀────┘
```

Raw material flows in; knowledge is compiled, kept honest, and pushed back out as content; the content raises new questions; the questions become new raw material.

---

## Skill map — all 9, when each one runs

| Skill | Trigger | In this story |
|-------|---------|---------------|
| `/by-1` | "compile this" | Step 2 — the monitor clipping → a framework entry |
| `/by-a` | "compile everything" | Step 2 — batch-compiled the CPU/GPU/RAM clippings |
| `/chat-distill` | "distill conversations" | Step 3 — kept one valuable AI conversation |
| `/rec-1` | "log today's progress" | Step 3 — appended the daily diary line |
| `/kbi` | "knowledge base iteration" | Step 4 — health check, broken links, gaps, hallucinations |
| `/jh-1` | "aggregate topic X" | Step 4 — PC-hardware knowledge map |
| `/chiselplan` | "plan my project" | Step 5 — learning project with phases (can create `plan-1`) |
| `/wr-1` | "weekly review" | Step 5 — 7 diary notes → weekly review |
| `/blog-1` | "article / project / share" | Step 6 — PC Hardware Notes → `4_Outputs/` |

You do not need all nine at the start. The minimal start is **capture → `/by-1` → read the entry**. Add the rest when the loop asks for them.
