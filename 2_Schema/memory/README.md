---
type: schema-doc
created: 2026-11-01
updated: 2026-11-01
tags:
  - memory
  - schema
---

# Memory — Working Memory Module for AI Agents

## What this is

This folder is the **working memory** module for AI agents operating this knowledge base.
Instead of reconstructing context from conversation history every session, the agent reads a
compact snapshot per active work domain before acting on it.

One domain file = **current status snapshot + key asset entry points + key people + red lines
+ to be filled**. It is not a wiki article; it is what the agent must know in order to act
correctly on that domain today.

## Directory structure

```
2_Schema/memory/
├── README.md            # this file: module contract + usage rules
├── memory-index.md      # master index: one row per domain doc (created with the first domain)
├── memory-template.md   # blank template for a new domain doc
└── Memory-*.md          # one file per active domain, created as needed
```

## The master index

`memory-index.md` is the navigation table. It lists every domain doc with a one-line summary
and the trigger for when the agent must open it:

| Domain | Doc | One-line summary | When to read |
|--------|-----|------------------|--------------|
| [domain name] | [[Memory-...]] | [current phase, not just the topic] | [what kind of question means "open this first"] |

Index rules:

- One row per domain doc; remove the row when a domain is archived.
- The summary must state the **current phase / state**, e.g. "paused since YYYY-MM, assets preserved and restartable", not just the topic name.
- "When to read" states the trigger condition in plain terms.

Every domain doc carries the `memory` tag plus one or two domain-specific tags.

## How to create a new domain doc

1. Copy `memory-template.md` to `Memory-<DomainName>.md`.
2. Fill the frontmatter: set `domain`, keep `type: memory`, set `created` and `updated` to today's date.
3. Fill sections in order: one-liner → current status → key assets → people → red lines → to be filled.
4. Add one row to the master index table.
5. Keep it a snapshot: terse and pointer-heavy. Details live in the linked files; this file only holds what the agent must know before acting.

## Usage rules (AI agents must read)

1. **Read before acting.** Whenever the user touches a domain, open that domain doc first, then follow the user's instruction. Do not act from conversation history alone.
2. **One source of truth for status.** The state of a domain = the domain doc plus the ledgers or trackers it points to. Do not judge from memory of past chats.
3. **Update first.** When a session produces new status (new progress, new red line, new person), write it back to the matching domain doc and bump its `updated` date before continuing the conversation.
4. **Red lines are hard constraints.** The "Red lines" section in every domain doc outranks convenience, defaults, and casual phrasing in the moment. If a red line blocks a request, stop and say so instead of working around it.
5. **When unsure, ask.** If the domain doc does not cover the situation and you are not certain, ask the user. Do not guess.

## Maintenance

- **Sync the `updated` date.** Every time a domain doc changes, update its `updated:` frontmatter field to that day. A stale `updated` date is the signal that the snapshot is rotten.
- **Fill "To be filled" incrementally.** Unknown fields start as open checkboxes (`- [ ]`); close them (`- [x]`) with a date once they are answered in conversation.
- **Defer to the doc, not impressions.** When the doc and a vague recollection conflict, the doc wins. If the doc looks wrong, verify with the user rather than silently overriding it.
- **Keep it operator-scoped.** This module tracks one operator's active work domains; do not grow it into a general-purpose wiki.

## Frontmatter convention

Each domain doc uses this shape (see `memory-template.md` for the full skeleton):

```md
---
type: memory
domain: [domain name]
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - memory
  - [domain tag]
---
```
