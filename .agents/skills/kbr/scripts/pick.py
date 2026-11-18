"""Pick concepts by urgency, time since review, and novelty."""

import argparse
import json
import random
from datetime import date

from common import load_config, load_index, load_json, save_json, state_lock

REASONS = {
    "dredge": "Low recall or high importance",
    "coverage": "Long time since last review",
    "new": "Never reviewed",
}


def days_since(last, today):
    try:
        return (today - date.fromisoformat(last)).days
    except (TypeError, ValueError):
        return float("inf")


def quota_by_pool(ratios, count):
    weights = [ratios[name] for name in REASONS]
    if any(weight < 0 for weight in weights) or not sum(weights):
        raise SystemExit("Pool ratios must be nonnegative and have a positive sum.")
    shares = [count * weight / sum(weights) for weight in weights]
    quotas = [int(share) for share in shares]
    order = sorted(range(len(shares)), key=lambda i: shares[i] - quotas[i], reverse=True)
    for position in order[:count - sum(quotas)]:
        quotas[position] += 1
    return dict(zip(REASONS, quotas))


def pick(config, index, state, count, today):
    concepts = {item["id"]: item for item in index["concepts"]}
    recalled = state.get("concepts", {})
    dredge, coverage, new = [], [], []
    for cid in concepts:
        review = recalled.get(cid, {}).get("recall", {})
        if not review.get("count", 0):
            new.append(cid)
            continue
        interval = days_since(review.get("last"), today)
        if interval < config["min_interval_days"]:
            continue
        coverage.append((cid, interval))
        score = review.get("score", config["unknown_default_score"])
        importance = review.get("importance", 50)
        if score < 90 or importance >= 70:
            dredge.append((cid, (100 - score) * importance / 100))

    dredge.sort(key=lambda item: item[1], reverse=True)
    coverage.sort(key=lambda item: item[1], reverse=True)
    pools = {
        "dredge": [cid for cid, _ in dredge[:config["dredge_pool_size"]]],
        "coverage": [cid for cid, _ in coverage[:config["coverage_pool_size"]]],
        "new": new,
    }
    selected = {}
    for name, quota in quota_by_pool(config["pool_ratios"], count).items():
        available = [cid for cid in pools[name] if cid not in selected]
        for cid in random.sample(available, min(quota, len(available))):
            selected[cid] = REASONS[name]

    for cid in [*new, *(cid for cid, _ in coverage)]:
        if len(selected) >= count:
            break
        selected.setdefault(cid, "Eligible fallback")

    return [
        {"id": cid, "title": concepts[cid]["title"], "path": concepts[cid]["path"], "reason": reason}
        for cid, reason in selected.items()
    ]


def next_item(config, index, state, count, today):
    queue = config["state_dir"] / "pending.json"
    pending = load_json(queue, {})
    known = {item["id"] for item in index["concepts"]}
    recalled = state.get("concepts", {})

    def review_count(cid):
        return recalled.get(cid, {}).get("recall", {}).get("count", 0)

    items = []
    if pending.get("created") == today.isoformat():
        items = [
            item for item in pending.get("items", [])
            if item["id"] in known
            and review_count(item["id"]) == item["review_count"]
            and (
                not item["review_count"]
                or days_since(recalled[item["id"]]["recall"]["last"], today) >= config["min_interval_days"]
            )
        ]
    if not items:
        items = [
            {**item, "review_count": review_count(item["id"])}
            for item in pick(config, index, state, count, today)
        ]
    if not items:
        queue.unlink(missing_ok=True)
        return None
    current = {"created": today.isoformat(), "items": items}
    if current != pending:
        save_json(queue, current)
    head = items[0]
    return {key: head[key] for key in ("id", "title", "path", "reason")} | {"remaining": len(items) - 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, help="Override the configured batch size.")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    parser.add_argument("--next", action="store_true", help="Return one item from today's queue.")
    args = parser.parse_args()

    config = load_config()
    count = config["batch_size"] if args.count is None else args.count
    if count < 1:
        parser.error("The batch size must be at least one.")
    index = load_index(config)
    state_path = config["state_dir"] / "recall_state.json"
    today = date.today()

    if args.next:
        with state_lock(config["state_dir"]):
            item = next_item(config, index, load_json(state_path, {}), count, today)
        if args.json:
            print(json.dumps(item, indent=2))
        elif item:
            print(f"{item['title']} [{item['id']}] — {item['reason']} ({item['remaining']} remaining)")
        else:
            print("No concepts are eligible for review today.")
        return

    items = pick(config, index, load_json(state_path, {}), count, today)
    if args.json:
        print(json.dumps(items, indent=2))
    else:
        for i, item in enumerate(items, 1):
            print(f"{i}. {item['title']} [{item['id']}] — {item['reason']}")


if __name__ == "__main__":
    main()
