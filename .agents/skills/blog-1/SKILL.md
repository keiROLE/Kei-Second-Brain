---
name: blog-1
description: Create new documents (article / project / share) from the knowledge base into the Output layer (4_outputs/) — auto-generate frontmatter + English slug, write to 4_outputs/, then remind the user to build/publish. Triggers on "/blog-1".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# blog-1 — Blog Document Generator

## Role

You are the document generator of the Output layer. Create markdown files that follow the blog's conventions and place them in `4_outputs/` (the Output layer — see `2_Schema/TheSchema.md` §1).

**Output directory**: `4_outputs/` — every file lands here, at the repo root of the Output layer. If the user also publishes to an external blog site, they copy from `4_outputs/` themselves; this skill writes into the vault only.

## Trigger

User says "/blog-1" with a content type and parameters.

## Commands

### Article (data/blogs/posts/)

```
/blog-1 article "Title" "Category" "Body"
```

### Project (data/projects/)

```
/blog-1 project "Title" "Category" "Description" [tech:"stack"] [link:"url"] [status:"active"|"completed"]
```

### Share (data/shares/)

> **Strict rule**: shares can only be **third-party files, websites, tools or resources you discovered and recommend**. Never your own creative work (self-authored content goes to "article" or "project").

```
/blog-1 share "Title" "Category" "Description" [link:"url"]
```

## Workflow

### Step 1: Parse parameters

**Article**: title (required), category (required), body (required, may be multi-line Markdown).

**Project**: title (required), category (required), description (required), tech (optional), link (optional, default ""), status (optional, default "active"; only "active" or "completed").

**Share**: title (required), category (required), description (required), link (optional, default "").

### Step 2: Generate the filename (slug)

From the title to an English slug:
1. Remove punctuation and special characters.
2. Lowercase.
3. Replace spaces with hyphens.
4. Collapse consecutive hyphens.
5. Strip leading/trailing hyphens.

Example: "How I Rebuilt My Knowledge Base with LLM Wiki" → `llm-wiki-knowledge-base-rebuild`.

**Dedup**: if the slug already exists, append `-2`, `-3`, etc.

### Step 3: Generate frontmatter

**Article** (`data/blogs/posts/`):
```yaml
---
title: "Title"
date: "YYYY-MM-DD"
category: "Category"
---
```

**Project** (`data/projects/`):
```yaml
---
title: "Title"
date: "YYYY-MM-DD"
tag: "Project"
desc: "Description"
tech: "Stack"
link: "url"
status: "active"
---
```

**Share** (`data/shares/`):
```yaml
---
title: "Title"
date: "YYYY-MM-DD"
tag: "Category"
desc: "Description"
link: "url"
---
```

### Step 4: Generate the full file

- Article: frontmatter + full body (preserve the user's Markdown formatting).
- Project: frontmatter + optional body.
- Share: frontmatter + optional body.

### Step 5: Write the file

Write to the Output layer:
- Article: `4_outputs/<slug>.md`
- Project: `4_outputs/<slug>.md`
- Share: `4_outputs/<slug>.md`

### Step 6: Confirm

```
## Generated

| Field | Value |
|-------|-------|
| Type | article/project/share |
| File | <slug>.md |
| Path | 4_outputs/<slug>.md |
| Title | "Title" |
| Date | YYYY-MM-DD |

Next: publish from `4_outputs/` (copy to your site's data directory, or `npm run build` if you use a static-site generator).
```

## Rules

1. **Ownership**: `shares` only holds third-party resources (others' websites, tools, files, tutorials). Your own articles → `4_outputs/` (type `article`); your own projects → `4_outputs/` (type `project`).
2. **Date format**: `YYYY-MM-DD`.
3. **Encoding**: UTF-8.
4. **No overwriting**: only create new files.
5. **Slug dedup**: auto-append suffixes on collision.
6. **Optional fields** (tech/link/status): write into frontmatter only when provided.
7. **Body preserved**: the article's Markdown (headings, lists, tables, quotes) is kept as-is.
8. **Empty link**: write `""` when link is empty.
