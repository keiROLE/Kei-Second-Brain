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
import sys, re, os, io
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
SCAN_DIRS = ["0_Inbox"]
EXCLUDE_DIRS = {".obsidian", ".trash", ".agents", ".claude", ".claudian",
                "archive", "templates", ".git", ".preview"}
INDEX = VAULT / "1_Wiki" / "index.md"


def read_text(p):
    with io.open(p, "r", encoding="utf-8-sig") as f:
        return f.read()


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^(\w[\w-]*)\s*:\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return fm


def rel_norm(p):
    return os.path.relpath(p, VAULT).replace("\\", "/").lstrip("/")


def index_sources():
    if not INDEX.exists():
        return set()
    srcs = set()
    for line in read_text(INDEX).splitlines():
        if "|" in line and "[[" not in line:
            for c in line.split("|"):
                c = c.strip()
                if c.endswith(".md"):
                    srcs.add(c.lstrip("/").replace("\\", "/"))
    return srcs


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
    srcs = index_sources()
    todo, done, skip = [], [], []
    for p in iter_md():
        rel = rel_norm(p)
        proc = frontmatter(read_text(p)).get("processed", "")
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


def cmd_mark(files):
    for p in files:
        p = Path(p)
        if not p.is_absolute():
            p = VAULT / p
        if not p.exists():
            print(f"  not found: {p}")
            continue
        txt = read_text(p)
        m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", txt, re.S)
        if not m:
            print(f"  no frontmatter, skipped: {p}")
            continue
        body = m.group(2)
        if re.search(r"^processed\s*:", body, re.M):
            body = re.sub(r"^processed\s*:.*$", "processed: true", body, flags=re.M)
        else:
            body = body.rstrip("\n") + "\nprocessed: true"
        new = m.group(1) + body + m.group(3) + txt[m.end():]
        with io.open(p, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"  marked: {rel_norm(p)}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "mark":
        cmd_mark(sys.argv[2:])
    else:
        cmd_list()
