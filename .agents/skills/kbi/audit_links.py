# -*- coding: utf-8 -*-
"""
audit_links.py — kbi companion (deterministic part, read-only)
  Vault-wide link audit: broken-link list, islands/half-islands, incoming/outgoing counts.
  LLM does semantic judgment (gaps/hallucination/relations); link parsing is this script's job.

Usage: python audit_links.py

Path resolution: this script lives at <vault>/.agents/skills/kbi/audit_links.py
                 so the vault root is 3 parents up from this file.

Fix notes (2026-09-21):
  1. Valid targets now index the whole vault (previously only 1_Wiki, which mis-reported
     the TheSchema-mandated `## 原文档` back-links to 0_Inbox/diary/Clippings source files
     as broken).
  2. The `## 原文档` section is skipped for link auditing (it is a source-backlink section,
     not navigation).
  3. Path-style links (e.g. [[0_Inbox/000/认知记录/核心刚性.md]]) resolve by exact
     vault-relative path.
  4. Connectivity (incoming/outgoing, islands/half-islands) counts wiki-to-wiki links only.
"""
import os, re, io
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
WIKI = VAULT / "1_Wiki"
EXCLUDE = {".git", ".obsidian", ".trash", ".agents", ".claude", ".claudian",
           ".verysync", ".preview", ".dashboard-backup", ".sessions",
           ".doubaowork", "templates", "archive"}


def read_text(p):
    with io.open(p, "r", encoding="utf-8-sig") as f:
        return f.read()


def split_fm(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def norm(s):
    return s.strip().lower()


def strip_section(body, heading):
    """Remove a '## heading' section (used to exclude the ## 原文档 source section)."""
    sec = re.search(r"^##\s*%s\s*\n(.*?)(?=\n##\s|\Z)" % re.escape(heading), body, re.M | re.S)
    if not sec:
        return body
    return body[:sec.start()] + body[sec.end():]


def main():
    # 1) Index the whole vault: file stem / title / aliases (valid targets are vault-wide)
    vault_names = set()      # normalized name -> resolvable
    wiki_entries = {}        # normalized name -> wiki entry relpath (connectivity only)
    files = {}               # wiki relpath -> body (frontmatter and 原文档 section stripped)
    for dp, dn, fn in os.walk(VAULT):
        dn[:] = [x for x in dn if x not in EXCLUDE and not x.startswith(".")]
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = Path(dp) / f
            rel = os.path.relpath(p, VAULT)
            head, body = split_fm(read_text(p))
            stem = f[:-3]
            vault_names.add(norm(stem))
            tm = re.search(r'^title\s*:\s*"?([^"\n]+)"?', head, re.M)
            if tm:
                vault_names.add(norm(tm.group(1).strip()))
            am = re.search(r"^aliases\s*:\s*\n((?:\s+-\s+.+\n?)+)", head, re.M)
            if am:
                for al in re.findall(r"-\s+(.+)", am.group(1)):
                    vault_names.add(norm(al.strip()))
            # Only 1_Wiki entries participate in graph connectivity
            if rel.startswith("1_Wiki" + os.sep) and f != "index.md":
                relw = os.path.relpath(p, WIKI)
                wiki_entries[norm(stem)] = relw
                if tm:
                    wiki_entries[norm(tm.group(1).strip())] = relw
                if am:
                    for al in re.findall(r"-\s+(.+)", am.group(1)):
                        wiki_entries[norm(al.strip())] = relw
                files[relw] = strip_section(body, "原文档")

    link_re = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
    out = {}                 # outgoing links (wiki targets only, for connectivity)
    broken = {}
    for rel, body in files.items():
        out[rel] = set()
        for t in link_re.findall(body):
            tn = norm(t)
            # Path-style links: resolve by exact vault-relative path
            if "/" in t or "\\" in t or t.endswith(".md"):
                pt = t.strip().replace("/", os.sep).replace("\\", os.sep).lstrip(os.sep)
                if pt.startswith("1_Wiki" + os.sep):
                    resolved = (WIKI / pt[len("1_Wiki" + os.sep):]).is_file()
                else:
                    resolved = (VAULT / pt).is_file()
                if not resolved:
                    broken.setdefault(rel, set()).add(t.strip())
                continue
            if tn in wiki_entries:
                out[rel].add(tn)
            if tn not in vault_names:
                broken.setdefault(rel, set()).add(t.strip())

    incoming = {r: 0 for r in files}
    for rel, targets in out.items():
        for tn in targets:
            if tn in wiki_entries and wiki_entries[tn] in incoming:
                incoming[wiki_entries[tn]] += 1

    print("== Broken links (vault-wide resolution; `## 原文档` source section excluded) ==")
    if broken:
        for rel in sorted(broken):
            print(f"  {rel}: missing {', '.join(sorted(broken[rel]))}")
    else:
        print("  none")

    print("\n== Islands (in=0 and out=0, wiki-to-wiki links only) ==")
    islands = [r for r in files if incoming[r] == 0 and not out[r]]
    print("  " + ("\n  ".join(sorted(islands)) if islands else "none"))

    print("\n== Half-islands (in=0 and out<=1) ==")
    semi = [r for r in files if incoming[r] == 0 and 0 < len(out[r]) <= 1]
    print("  " + ("\n  ".join(sorted(semi)) if semi else "none"))

    print(f"\nTotal entries {len(files)}; broken links {len(broken)}; islands {len(islands)}; half-islands {len(semi)}")


if __name__ == "__main__":
    main()
