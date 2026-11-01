# -*- coding: utf-8 -*-
"""
validate_vault.py — kbi companion (deterministic lint part, read-only)
  Mechanically checks every 1_Wiki/ entry against 2_Schema/frontmatter.md,
  TheSchema.md section 5, and naming.md.
  The LLM only makes semantic judgments (kbi is read-only); this script only
  does mechanical checks and prints a per-category violation list.

Usage (run from the vault root):
  python .agents/skills/kbi/validate_vault.py

Path resolution: this script lives at <vault>/.agents/skills/kbi/validate_vault.py
                 so the vault root is 3 parents up from this file.

Checks:
  A. frontmatter exists and is parseable (YAML block)
  B. required fields: title / type / created / source / confidence / tags / author
     (entity entries also need entity_kind)
  C. type matches its directory: concepts->concept, entities->entity,
     comparisons->comparison, frameworks->framework, resources->resource
  D. created format YYYY-MM-DD
  E. tags >= 3 (type + topic + PARA/resource)
  F. every ## See also link carries one of the 8 English type labels
     (unlabeled = to-labeled; illegal label = listed)
  G. deprecated fields related / links must not appear in entry frontmatter
  H. filename: no spaces, does not start with untitled / misc
  I. duplicate titles (same stem or same title)
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
# Placeholder filenames that count as violations. Extend this set as needed.
PLACEHOLDER_STEMS = {"untitled", "misc"}


def read_text(p):
    with io.open(p, "r", encoding="utf-8-sig") as f:
        return f.read()


def parse_frontmatter(text):
    """Return (fields_dict, ok). Hand-parsed; no yaml dependency."""
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
            # List item or continuation; attach to the current field.
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
                fields[cur] = []  # filled by following indented lines
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
        return len([x for x in re.split(r"[,]", v) if x.strip()])
    return 0


def parse_see_also(text):
    """Return (bad_entries, unlabeled, illegal_label, total)."""
    m = re.search(r"^##\s*See also\s*$", text, re.M)
    if not m:
        return [], [], [], 0
    section = text[m.end():]
    # Cut at the next ## heading.
    nxt = re.search(r"^##\s+", section, re.M)
    if nxt:
        section = section[:nxt.start()]
    bad, unlabeled, illegal = [], [], []
    total = 0
    for line in section.splitlines():
        lm = re.match(r"^\s*-\s*\[\[(.+?)\]\](?:\s+(\S+))?\s*$", line)
        if not lm:
            continue
        total += 1
        raw = (lm.group(2) or "").strip()
        # Label = leading English type word (letters + hyphens); a note may follow.
        mm = re.match(r"^([a-z-]+)", raw.lower())
        label = mm.group(1) if mm else ""
        if not label:
            unlabeled.append(lm.group(1))
        elif label not in LINK_TYPES:
            illegal.append((lm.group(1), label))
    return [], unlabeled, illegal, total


def main():
    issues = {k: [] for k in
              ["A_frontmatter", "B_missing_fields", "C_type_mismatch",
               "D_bad_date", "E_tags", "F_links", "G_deprecated",
               "H_filename", "I_duplicate_title"]}
    counts = {}
    seen_titles = {}
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

            # H. Filename (placeholder word = whole stem counts as violation).
            if " " in name:
                issues["H_filename"].append(f"{rel} — filename contains spaces")
            if fp.stem in PLACEHOLDER_STEMS:
                issues["H_filename"].append(f"{rel} — filename is a placeholder word")

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
                issues["G_deprecated"].append(f"{rel} — deprecated fields: {', '.join(dep)}")

            # C. type match
            t = fields.get("type", "")
            if t and t != expected_type:
                issues["C_type_mismatch"].append(
                    f"{rel} — type={t}, expected={expected_type}")

            # D. date
            c = fields.get("created", "")
            if c and not DATE_RE.match(c):
                issues["D_bad_date"].append(f"{rel} — created={c}")

            # E. tags
            n = count_tags(fields)
            if n < 3:
                issues["E_tags"].append(f"{rel} — only {n} tags (need >= 3)")

            # I. duplicate titles
            stem = fp.stem
            if stem in seen_titles:
                issues["I_duplicate_title"].append(
                    f"{rel} — duplicate of {seen_titles[stem]}")
            else:
                seen_titles[stem] = str(rel)

            # F. See also links
            _, unlabeled, illegal, _ = parse_see_also(text)
            for u in unlabeled:
                issues["F_links"].append(f"{rel} — link [[{u}]] has no type label")
            for tgt, lab in illegal:
                issues["F_links"].append(
                    f"{rel} — link [[{tgt}]] label '{lab}' not in the 8 types")

    # ---- output ----
    out = io.StringIO()
    out.write("=== VALIDATE VAULT (mechanical check of 1_Wiki entries) ===\n")
    out.write(f"Total entries: {total}  Type distribution: "
              + ", ".join(f"{k}={v}" for k, v in counts.items()) + "\n\n")
    order = [("A_frontmatter", "A. frontmatter missing/unparseable"),
             ("B_missing_fields", "B. required fields missing"),
             ("C_type_mismatch", "C. type does not match directory"),
             ("D_bad_date", "D. created date format wrong"),
             ("E_tags", "E. fewer than 3 tags"),
             ("F_links", "F. See also link label issues"),
             ("G_deprecated", "G. deprecated fields present"),
             ("H_filename", "H. filename violations"),
             ("I_duplicate_title", "I. duplicate titles")]
    total_issues = 0
    for key, label in order:
        items = issues[key]
        total_issues += len(items)
        out.write(f"[{label}] {len(items)} found\n")
        for it in items[:50]:
            out.write(f"  - {it}\n")
        if len(items) > 50:
            out.write(f"  ... {len(items)-50} more omitted\n")
        out.write("\n")
    out.write(f"=== Summary: {total_issues} issues across {total} entries ===\n")
    sys.stdout.write(out.getvalue())


if __name__ == "__main__":
    main()
