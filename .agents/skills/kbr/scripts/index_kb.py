"""Build the local active-recall index from the wiki."""

import argparse
from datetime import datetime

from common import FRONTMATTER, load_config, save_json

try:
    import yaml
except ImportError:
    raise SystemExit("Install the recall dependency with python -m pip install PyYAML.") from None


def extract_snippet(body):
    paragraphs = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith(">") and line[1:].strip():
            return line[1:].strip()[:180]
        if line and not line.startswith(("#", "|", "```")):
            paragraphs.append(line)
    return " ".join(paragraphs)[:180]


def list_field(value):
    if isinstance(value, list):
        return [str(item) for item in value]
    return [value] if isinstance(value, str) and value else []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="Print only the summary.")
    args = parser.parse_args()

    config = load_config()
    wiki = config["kb_path"]
    if not wiki.is_dir():
        parser.error(f"Wiki directory not found: {wiki}")

    concepts, skipped = [], []
    excluded_dirs = set(config["exclude_dirs"])
    for path in sorted(wiki.rglob("*.md")):
        relative = path.relative_to(wiki)
        rel = relative.as_posix()
        if (any(part.startswith(".") or part in excluded_dirs for part in relative.parts)
                or path.name in config["exclude_files"]
                or any(word.casefold() in path.name.casefold() for word in config["exclude_patterns"])
                or not path.resolve().is_relative_to(wiki)):
            skipped.append(rel)
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            skipped.append(rel)
            continue
        match = FRONTMATTER.match(text)
        try:
            fields = yaml.safe_load(match[1]) if match else {}
        except yaml.YAMLError:
            skipped.append(rel)
            continue
        if not isinstance(fields, dict):
            fields = {}
        body = text[text.find("\n", match.end()) + 1:] if match else text
        concepts.append({
            "id": relative.with_suffix("").as_posix(),
            "path": rel,
            "title": str(fields.get("title") or path.stem),
            "type": str(fields.get("type") or ""),
            "aliases": list_field(fields.get("aliases")),
            "tags": list_field(fields.get("tags")),
            "snippet": extract_snippet(body),
            "mtime": path.stat().st_mtime,
        })

    output = config["state_dir"] / "index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    save_json(output, {
        "built": datetime.now().astimezone().isoformat(timespec="seconds"),
        "count": len(concepts),
        "excluded_count": len(skipped),
        "kb_root": str(wiki),
        "concepts": concepts,
    })
    if not args.quiet:
        for path in skipped:
            print(f"Skipped: {path}")
    print(f"Indexed {len(concepts)} concepts, skipped {len(skipped)}. Index: {output}")


if __name__ == "__main__":
    main()
