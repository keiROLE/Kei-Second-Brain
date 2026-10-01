# -*- coding: utf-8 -*-
"""
validate_vault.py — kbi companion (deterministic lint part)
  Mechanical lint of every 1_Wiki/ entry against 2_Schema/frontmatter.md,
  TheSchema.md §3/§4 and naming.md. The LLM only makes semantic judgments
  (kbi is read-only); this script only runs mechanical checks and lists violations.

Usage (from the vault root):
  python .agents/skills/kbi/validate_vault.py

Checks:
  A. frontmatter present and parsable
  B. required fields: title / type / created / source / confidence / tags / author
     (entity entries also require entity_kind)
  C. type matches containing directory (concepts->concept, ...)
  D. created date format YYYY-MM-DD
  E. tags >= 3 (type tag + topic + PARA/area)
  F. every `## See also` link carries one of the 8 English type labels
     (label = leading english word; a trailing note like "related (index)" is tolerated)
  G. deprecated fields related / links must not appear in entry frontmatter
  H. filenames: no spaces; placeholder stem (untitled / misc) is a violation
  I. duplicate titles (same stem)
"""
import re
import sys
import io
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
WIKI = VAULT / "1_Wiki"
TYPE_DIR = {
    "concepts": "concept",
    "entities": "entity",
    "comparisons": "comparison",
    "frameworks": "framework",
    "resources": "resource",
}
LINK_TYPES = {"apply", "contrast", "cause", "example",
              "part-of", "background", "related", "prerequisite"}
REQUIRED = ["title", "type", "created", "source", "confidence", "tags", "author"]
DEPRECATED = ["related", "links"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER_STEMS = {"untitled", "misc"}


def read_text(p):
    with io.open(p, "r", encoding="utf-8-sig") as f:
        return f.read()


def parse_frontmatter(text):
    """Return (fields_dict, ok). Hand-rolled parser; no yaml dependency."""
    m = re.match(r"\A---\n(.*?)\n---", text, re.S)
    if not m:
        return None, False
    block = m.group(1)
    fields = {}
    cur = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith(" "):
            # list item / continuation line; scalar continuation is conservatively ignored
            if cur is not None:
                item = line.strip().lstrip("- ").strip()
                curval = fields.get(cur)
                if isinstance(curval, list):
                    curval.append(item)
                elif curval is None:
                    fields[cur] = [item]
            continue
        mm = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if mm:
            cur = mm.group(1)
            val = mm.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                fields[cur] = [x.strip() for x in val[1:-1].split(",") if x.strip()]
            elif val == "":
                fields[cur] = []
            else:
                fields[cur] = val
    return fields, True


def count_tags(fields):
    v = fields.get("tags")
    if v is None:
        return 0
    if isinstance(v, list):
        return len(v)
    if isinstance(v, str):
        return len([x for x in re.split(r"[,，]", v) if x.strip()])
    return 0


def parse_see_also(text):
    """Return (unlabeled, illegal, total)."""
    m = re.search(r"^##\s*See also\s*$", text, re.M)
    if not m:
        return [], [], 0
    section = text[m.end():]
    nxt = re.search(r"^##\s+", section, re.M)
    if nxt:
        section = section[:nxt.start()]
    unlabeled, illegal = [], []
    total = 0
    for line in section.splitlines():
        lm = re.match(r"^\s*-\s*\[\[(.+?)\]\](?:\s+(\S+))?\s*$", line)
        if not lm:
            continue
        total += 1
        raw = (lm.group(2) or "").strip()
        mm = re.match(r"^([a-z-]+)", raw.lower())
        label = mm.group(1) if mm else ""
        if not label:
            unlabeled.append(lm.group(1))
        elif label not in LINK_TYPES:
            illegal.append((lm.group(1), label))
    return unlabeled, illegal, total


def main():
    issues = {k: [] for k in
              ["A_frontmatter", "B_missing_fields", "C_type_mismatch",
               "D_bad_date", "E_tags", "F_links", "G_deprecated",
               "H_filename", "I_duplicate_title"]}
    counts = {}
    seen_stems = {}
    total = 0

    for d, expected_type in TYPE_DIR.items():
        dpath = WIKI / d
        if not dpath.is_dir():
            counts[d] = 0
            continue
        files = sorted(dpath.glob("*.md"))
        counts[d] = len(files)
        for fp in files:
            total += 1
            rel = fp.relative_to(VAULT)
            text = read_text(fp)
            name = fp.name

            # H. filename
            if " " in name:
                issues["H_filename"].append(f"{rel} — space in filename")
            if fp.stem in PLACEHOLDER_STEMS:
                issues["H_filename"].append(f"{rel} — placeholder stem")

            # A. frontmatter
            fields, ok = parse_frontmatter(text)
            if not ok:
                issues["A_frontmatter"].append(str(rel))
                continue

            # B. required fields
            missing = [k for k in REQUIRED if k not in fields]
            if fields.get("type") == "entity" and "entity_kind" not in fields:
                missing.append("entity_kind")
            if missing:
                issues["B_missing_fields"].append(f"{rel} — missing: {', '.join(missing)}")

            # G. deprecated fields
            dep = [k for k in DEPRECATED if k in fields]
            if dep:
                issues["G_deprecated"].append(f"{rel} — deprecated: {', '.join(dep)}")

            # C. type match
            t = fields.get("type", "")
            if t and t != expected_type:
                issues["C_type_mismatch"].append(f"{rel} — type={t}, expected={expected_type}")

            # D. date
            c = fields.get("created", "")
            if c and not DATE_RE.match(c):
                issues["D_bad_date"].append(f"{rel} — created={c}")

            # E. tags
            n = count_tags(fields)
            if n < 3:
                issues["E_tags"].append(f"{rel} — {n} tags (need >= 3)")

            # I. duplicate stem
            if fp.stem in seen_stems:
                issues["I_duplicate_title"].append(f"{rel} — same stem as {seen_stems[fp.stem]}")
            else:
                seen_stems[fp.stem] = str(rel)

            # F. See-also labels
            unlabeled, illegal, _ = parse_see_also(text)
            for u in unlabeled:
                issues["F_links"].append(f"{rel} — link [[{u}]] has no type label")
            for tgt, lab in illegal:
                issues["F_links"].append(f"{rel} — link [[{tgt}]] label '{lab}' not in 8 types")

    # ---- output ----
    out = io.StringIO()
    out.write("=== VALIDATE VAULT (1_Wiki mechanical lint) ===\n")
    out.write(f"Entries: {total}  type distribution: "
              + ", ".join(f"{k}={v}" for k, v in counts.items()) + "\n\n")
    order = [("A_frontmatter", "A. missing/unparsable frontmatter"),
             ("B_missing_fields", "B. missing required fields"),
             ("C_type_mismatch", "C. type-directory mismatch"),
             ("D_bad_date", "D. created date format"),
             ("E_tags", "E. tags < 3"),
             ("F_links", "F. See-also link label issues"),
             ("G_deprecated", "G. deprecated fields"),
             ("H_filename", "H. filename violations"),
             ("I_duplicate_title", "I. duplicate titles")]
    total_issues = 0
    for key, label in order:
        items = issues[key]
        total_issues += len(items)
        out.write(f"[{label}] {len(items)}\n")
        for it in items[:50]:
            out.write(f"  - {it}\n")
        if len(items) > 50:
            out.write(f"  … {len(items)-50} more omitted\n")
        out.write("\n")
    out.write(f"=== Summary: {total_issues} issues across {total} entries ===\n")
    sys.stdout.write(out.getvalue())


if __name__ == "__main__":
    main()
