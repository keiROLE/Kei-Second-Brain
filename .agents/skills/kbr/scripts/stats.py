"""Summarize recall coverage, priority, and review history."""

import argparse
from collections import Counter

from common import load_config, load_index, load_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=10, help="Number of priority entries to show.")
    args = parser.parse_args()
    if args.top < 0:
        parser.error("--top must be nonnegative.")

    config = load_config()
    index = load_index(config)
    directory = config["state_dir"]
    state = load_json(directory / "recall_state.json", {})
    reviews = state.get("concepts", {})
    concepts = index["concepts"]
    unseen = []
    priority = []
    for item in concepts:
        review = reviews.get(item["id"], {}).get("recall", {})
        score = review.get("score", config["unknown_default_score"])
        importance = review.get("importance", 50)
        count = review.get("count", 0)
        last = review.get("last", "never")
        priority.append(((100 - score) * importance / 100, item["title"], score, importance, count, last))
        if not count:
            unseen.append(item["title"])

    print(f"Indexed concepts: {len(concepts)}")
    print(f"Recalled: {len(concepts) - len(unseen)}; never recalled: {len(unseen)}")
    if unseen:
        print("  " + ", ".join(unseen[:8]) + (" …" if len(unseen) > 8 else ""))
    types = Counter(item.get("type") or "unknown" for item in concepts)
    print("Entry types:", dict(types))
    print("\nRecall priority by (100 − score) × importance / 100:")
    for urgency, title, score, importance, count, last in sorted(priority, key=lambda row: -row[0])[:args.top]:
        print(f"  {urgency:6.1f}  score={score:>3}  importance={importance:>3}  reviews={count}  last={last}  {title}")

    days = Counter(item["date"] for item in state.get("history", []))
    if days:
        print("\nReviews by date:", dict(sorted(days.items())))


if __name__ == "__main__":
    main()
