# -*- coding: utf-8 -*-
"""
audit_links.py — kbi companion (deterministic part, read-only)
  Vault-wide link audit: broken-link list, islands/half-islands, incoming/outgoing counts.
  LLM does semantic judgment (gaps/hallucination/relations); link parsing is this script's job.

Usage: python audit_links.py

Path resolution: this script lives at <vault>/.agents/skills/kbi/audit_links.py
                 so the vault root is 3 parents up from this file.
"""
import os, re, io
from pathlib import Path

WIKI = Path(__file__).resolve().parents[3] / "1_Wiki"
EXCLUDE = {"templates", "archive"}


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


def main():
    entries = {}   # normalized name -> entry relpath
    files = {}    # relpath -> body (frontmatter stripped)
    for dp, dn, fn in os.walk(WIKI):
        dn[:] = [x for x in dn if x not in EXCLUDE]
        for f in fn:
            if not f.endswith(".md") or f == "index.md":
                continue
            rel = os.path.relpath(os.path.join(dp, f), WIKI)
            head, body = split_fm(read_text(os.path.join(dp, f)))
            files[rel] = body
            stem = f[:-3]
            entries[norm(stem)] = rel
            tm = re.search(r'^title\s*:\s*"?([^"\n]+)"?', head, re.M)
            if tm:
                entries[norm(tm.group(1).strip())] = rel
            am = re.search(r"^aliases\s*:\s*\n((?:\s+-\s+.+\n?)+)", head, re.M)
            if am:
                for al in re.findall(r"-\s+(.+)", am.group(1)):
                    entries[norm(al.strip())] = rel

    link_re = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
    out = {r: set() for r in files}
    broken = {}
    for rel, body in files.items():
        for t in link_re.findall(body):
            tn = norm(t)
            out[rel].add(tn)
            if tn not in entries:
                broken.setdefault(rel, set()).add(t.strip())

    incoming = {r: 0 for r in files}
    for rel, targets in out.items():
        for tn in targets:
            if tn in entries and entries[tn] in incoming:
                incoming[entries[tn]] += 1

    print("== Broken links ==")
    if broken:
        for rel in sorted(broken):
            print(f"  {rel}: missing {', '.join(sorted(broken[rel]))}")
    else:
        print("  none")

    print("\n== Islands (in=0 and out=0) ==")
    islands = [r for r in files if incoming[r] == 0 and not out[r]]
    print("  " + ("\n  ".join(sorted(islands)) if islands else "none"))

    print("\n== Half-islands (in=0 and out<=1) ==")
    semi = [r for r in files if incoming[r] == 0 and 0 < len(out[r]) <= 1]
    print("  " + ("\n  ".join(sorted(semi)) if semi else "none"))

    print(f"\nTotal entries {len(files)}; broken links {len(broken)}; islands {len(islands)}; half-islands {len(semi)}")


if __name__ == "__main__":
    main()
