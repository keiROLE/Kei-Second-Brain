# -*- coding: utf-8 -*-
"""
find_uncompiled.py — by-a companion (deterministic part)
  List uncompiled files + write back `processed` markers.
  LLM does the compile judgment; this script only does file scanning and marking.

Usage:
  python find_uncompiled.py                      # list uncompiled candidates
  python find_uncompiled.py mark <file> ...      # processed: false -> true (frontmatter only)

Path resolution: this script lives at <vault>/.agents/skills/by-a/find_uncompiled.py
                 so the vault root is 3 parents up from this file.
"""
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
SCAN_DIRS = ["0_Inbox", "Clippings"]
EXCLUDE_DIRS = {".obsidian", ".trash", ".agents", ".claude", ".claudian",
                "archive", "templates", ".git", ".preview", ".dashboard-backup"}
INDEX = VAULT / "1_Wiki" / "index.md"
FRONTMATTER = re.compile(r"\A\ufeff*---[ \t]*\r?\n(.*?)(?=^---[ \t]*\r?$)", re.M | re.S)
FIELD = re.compile(r"""^(['"]?)([\w-]+)\1[ \t]*:[ \t]*(.*)$""")
SCALAR = re.compile(r"""^(?:"(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|.*?)(?=[ \t]+#|[ \t]*$)""")
PROCESSED = re.compile(r"""^(?P<key>['"]?processed['"]?[ \t]*:[ \t]*)(?P<value>[^\r\n]*)""", re.M)
SOURCE_COLUMN = re.compile(r"(?:sources?(?:\s*\([^)]*\))?|来源)", re.I)


def read_text(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def scalar_token(value):
    return "" if value.startswith("#") else SCALAR.match(value)[0]


def frontmatter(text):
    m = FRONTMATTER.match(text)
    if not m:
        return {}
    fm = {}
    current = None
    for line in m.group(1).splitlines():
        field = FIELD.match(line)
        if field:
            current = field[2]
            fm[current] = scalar_token(field[3]).strip("'\"")
            continue
        item = re.match(r"^[ \t]*-[ \t]+(.*)$", line)
        if current == "source" and item:
            previous = fm[current]
            if not previous or isinstance(previous, list):
                fm[current] = [*previous, scalar_token(item[1]).strip("'\"")]
    return fm


def rel_norm(p):
    return os.path.relpath(p, VAULT).replace("\\", "/").lstrip("/")


def source_path(cell):
    """Normalize a plain source path or a wikilink to a source note."""
    source = cell.strip().strip("`")
    if source.startswith("[[") and source.endswith("]]"):
        source = re.split(r"\\?\||#", source[2:-2], maxsplit=1)[0].strip()
        if source and not source.lower().endswith(".md"):
            source += ".md"
    if source.lower().endswith(".md"):
        return source.lstrip("/\\").replace("\\", "/")
    return None


def table_cells(line):
    """Split a Markdown table row without splitting wikilink aliases."""
    cells = []
    start = 1
    for token in re.finditer(r"\[\[[^\]]*\]\]|\\\||\|", line[1:]):
        if token[0] == "|":
            cells.append(line[start:1 + token.start()].strip())
            start = 1 + token.end()
    if line[start:].strip():
        cells.append(line[start:].strip())
    return cells


def index_sources():
    sources = set()
    column = None
    if INDEX.is_file():
        for line in read_text(INDEX).splitlines():
            line = line.lstrip()
            if not line.startswith("|"):
                column = None
                continue
            cells = table_cells(line)
            header_column = next((i for i, cell in enumerate(cells) if SOURCE_COLUMN.fullmatch(cell)), None)
            if header_column is not None:
                column = header_column
            elif column is not None and column < len(cells):
                source = source_path(cells[column])
                if source:
                    sources.add(source)
    return sources


def wiki_sources():
    """Read entry provenance when a compiled source is missing from the index."""
    sources = set()
    for folder in ("concepts", "entities", "comparisons", "frameworks", "resources"):
        for path in (VAULT / "1_Wiki" / folder).rglob("*.md"):
            if any(part.startswith(".") or part in EXCLUDE_DIRS for part in path.relative_to(VAULT).parent.parts):
                continue
            values = frontmatter(read_text(path)).get("source", "")
            if isinstance(values, str):
                if values.startswith("[") and not values.startswith("[[") and values.endswith("]"):
                    values = re.findall(r'''\[\[[^\]]+\]\]|"(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^,\s][^,]*''', values[1:-1])
                else:
                    values = [values]
            for value in values:
                source = source_path(value.strip().strip("'\""))
                if source:
                    sources.add(source)
    return sources


def processed_status(text):
    return frontmatter(text).get("processed", "").lower()


def iter_md():
    for d in SCAN_DIRS:
        root = VAULT / d
        if not root.is_dir():
            continue
        for dp, dn, fn in os.walk(root):
            dn[:] = [x for x in dn if x not in EXCLUDE_DIRS and not x.startswith(".")]
            for f in fn:
                if f.endswith(".md"):
                    yield os.path.join(dp, f)


def cmd_list():
    srcs = index_sources() | wiki_sources()
    todo, done, skip = [], [], []
    today_diary = f"0_Inbox/diary/{date.today()}.md"
    today_open = False
    bare_sources = {source for source in srcs if "/" not in source}
    if bare_sources:
        matches = defaultdict(list)
        for path in VAULT.rglob("*.md"):
            relative = path.relative_to(VAULT)
            if path.name in bare_sources and not any(
                part.startswith(".") or part in EXCLUDE_DIRS for part in relative.parent.parts
            ):
                matches[path.name].append(relative.as_posix())
        srcs.difference_update(bare_sources)
        srcs.update(paths[0] for paths in matches.values() if len(paths) == 1)
    for p in iter_md():
        rel = rel_norm(p)
        if rel == today_diary:
            today_open = True
            continue
        proc = processed_status(read_text(p))
        if proc == "skip":
            skip.append(rel)
        elif rel in srcs or proc == "true":
            done.append(rel)
        else:
            todo.append((rel, proc or "(no processed field)"))
    print("== Uncompiled candidates ==")
    for rel, st in todo:
        print(f"  {rel}   [{st}]")
    print(f"\nTotal {len(todo)} candidates; already compiled/true {len(done)}; skipped {len(skip)}")
    if today_open:
        print(f"Today's diary is still open, skipped: {today_diary}")


def cmd_mark(files):
    for p in files:
        p = Path(p)
        if not p.is_absolute():
            p = VAULT / p
        if not p.exists():
            print(f"  not found: {p}")
            continue
        txt = read_text(p)
        m = FRONTMATTER.match(txt)
        if not m:
            print(f"  no frontmatter, skipped: {p}")
            continue
        status = processed_status(txt)
        if status in {"skip", "true"}:
            print(f"  processed: {status}, skipped: {rel_norm(p)}")
            continue
        body = m.group(1)
        field = PROCESSED.search(body)
        if field:
            value = field["value"]
            previous = scalar_token(value)
            separator = " " if value.startswith("#") else ""
            body = body[:field.start("value")] + "true" + separator + value[len(previous):] + body[field.end():]
        else:
            newline = "\r\n" if txt[:m.start(1)].endswith("\r\n") else "\n"
            body += "processed: true" + newline
        new = txt[:m.start(1)] + body + txt[m.end(1):]
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"  marked: {rel_norm(p)}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "mark":
        cmd_mark(sys.argv[2:])
    else:
        cmd_list()
