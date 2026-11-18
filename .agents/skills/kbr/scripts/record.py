"""Record a recall score and add the recall tag on the first review."""

import argparse
import re
from contextlib import nullcontext
from datetime import date

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

from common import FRONTMATTER, load_config, load_index, load_json, save_json, state_lock, write_text


def tagged_text(text):
    """Insert one tag while preserving the other frontmatter and the note body."""
    frontmatter = FRONTMATTER.match(text)
    if not frontmatter:
        return None
    fields = frontmatter[1]
    try:
        document = yaml.compose(fields, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return None
    if not isinstance(document, MappingNode):
        return None
    pair = next(((key, value) for key, value in document.value if key.value == "tags"), None)
    if pair is None:
        return None
    key, tags = pair
    if not isinstance(tags, SequenceNode) or tags.start_mark.index < key.end_mark.index:
        return None
    # A tagged or anchored collection is shared syntax and is left intact.
    if fields[tags.start_mark.index] not in "[-":
        return None
    if not all(isinstance(item, ScalarNode) and item.start_mark.index > tags.start_mark.index for item in tags.value):
        return None
    if any(item.value == "recall" for item in tags.value):
        return None
    if tags.flow_style:
        if tags.value:
            offset = tags.value[-1].end_mark.index
            addition = ", recall"
        elif fields[tags.start_mark.index] == "[":
            offset = tags.start_mark.index + 1
            addition = "recall"
        else:
            return None
        position = frontmatter.start(1) + offset
        return text[:position] + addition + text[position:]

    last = tags.value[-1]
    line_start = fields.rfind("\n", 0, last.start_mark.index) + 1
    newline_at = fields.find("\n", last.end_mark.index)
    prefix = re.fullmatch(r"([ \t]*)-[ \t]+", fields[line_start:last.start_mark.index])
    if newline_at == -1 or prefix is None or last.start_mark.line != last.end_mark.line:
        return None
    indent = prefix[1]
    newline = "\r\n" if fields[newline_at - 1] == "\r" else "\n"
    position = frontmatter.start(1) + newline_at + 1
    return text[:position] + indent + "- recall" + newline + text[position:]


def resolve_concept(index, key):
    for item in index["concepts"]:
        if key in (item["id"], item["path"]):
            return item
    matches = [item for item in index["concepts"] if key == item["title"] or key in item["aliases"]]
    if len(matches) != 1:
        raise SystemExit(f"Provide an exact concept ID. Found {len(matches)} title or alias matches for {key!r}.")
    return matches[0]


def record_review(config, concept, note, args):
    cid = concept["id"]
    state_path = config["state_dir"] / "recall_state.json"
    state = load_json(state_path, {"schema": 1, "concepts": {}, "history": []})
    records = state["concepts"]
    previous = records.get(cid, {}).get("recall", {})
    count = previous.get("count", 0) + 1
    importance = args.importance if args.importance is not None else previous.get("importance", 50)
    review_date = args.date.isoformat()
    if (previous.get("last"), previous.get("score"), previous.get("importance")) == (review_date, args.score, importance):
        print(f"Already recorded: {cid} score={args.score} importance={importance} ({review_date})")
        return
    record = {"score": args.score, "importance": importance, "count": count, "last": review_date}

    updated_note = None
    if count == 1:
        with note.open(encoding="utf-8", newline="") as handle:
            updated_note = tagged_text(handle.read())
    summary = f"{cid} score={args.score} importance={importance} count={count} ({review_date})"
    if args.dry_run:
        print(f"Would record: {summary}")
        if updated_note is not None:
            print(f"Would add recall tag: {concept['path']}")
        return

    if updated_note is not None:
        write_text(note, updated_note)
    records[cid] = {
        "path": concept["path"],
        "title": concept["title"],
        "aliases": concept["aliases"],
        "recall": record,
    }
    state["history"].append({
        "date": review_date, "concept": cid, "score": args.score, "importance": importance,
    })
    state["updated"] = date.today().isoformat()
    save_json(state_path, state)
    print(f"Recorded: {summary}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concept", required=True, help="Concept ID returned by pick.py.")
    parser.add_argument("--score", type=int, required=True, help="Recall score from 0 to 100.")
    parser.add_argument("--importance", type=int, help="Importance from 0 to 100. Defaults to the previous value.")
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(), help="Review date in YYYY-MM-DD.")
    parser.add_argument("--dry-run", action="store_true", help="Show the planned write without writing any files.")
    args = parser.parse_args()
    if not 0 <= args.score <= 100:
        parser.error("--score must be between 0 and 100.")
    if args.importance is not None and not 0 <= args.importance <= 100:
        parser.error("--importance must be between 0 and 100.")

    config = load_config()
    concept = resolve_concept(load_index(config), args.concept)
    note = (config["kb_path"] / concept["path"]).resolve()
    if not note.is_relative_to(config["kb_path"]) or not note.is_file():
        parser.error("The indexed note moved or is outside the wiki. Rebuild the index.")

    with nullcontext() if args.dry_run else state_lock(config["state_dir"]):
        record_review(config, concept, note, args)


if __name__ == "__main__":
    main()
