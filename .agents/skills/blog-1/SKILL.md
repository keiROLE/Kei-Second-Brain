---
name: blog-1
description: Create new documents (article / project / share) for a blog site from the knowledge base — auto-generate frontmatter + English slug + correct directory, then remind the user to build. Triggers on "/blog-1".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# blog-1 — Blog Document Generator

## Role

You are the document generator for the user's blog site. Create markdown files that follow the blog's conventions and place them in the correct data directory.

**Target project path**: configured by the user (default assumption: a static-site project such as Astro/Next.js/Hugo with a `data/` directory; ask if not configured).

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

Write to the correct path:
- Article: `<blog-project>/data/blogs/posts/<slug>.md`
- Project: `<blog-project>/data/projects/<slug>.md`
- Share: `<blog-project>/data/shares/<slug>.md`

### Step 6: Confirm

```
## Generated

| Field | Value |
|-------|-------|
| Type | article/project/share |
| File | <slug>.md |
| Path | data/.../<slug>.md |
| Title | "Title" |
| Date | YYYY-MM-DD |

Next: run `npm run build` (or your site's build command) in the project directory.
```

## Rules

1. **Ownership**: `shares` only holds third-party resources (others' websites, tools, files, tutorials). Your own articles → `blogs/posts`; your own projects → `projects`.
2. **Date format**: `YYYY-MM-DD`.
3. **Encoding**: UTF-8.
4. **No overwriting**: only create new files.
5. **Slug dedup**: auto-append suffixes on collision.
6. **Optional fields** (tech/link/status): write into frontmatter only when provided.
7. **Body preserved**: the article's Markdown (headings, lists, tables, quotes) is kept as-is.
8. **Empty link**: write `""` when link is empty.
