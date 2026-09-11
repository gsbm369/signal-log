#!/usr/bin/env python3
"""The seen-store must record what was PUBLISHED, not what was considered.

Recording every candidate is survivable while retention is 45 days. It is
archive-burning the moment a category remembers forever: one measured run took
85 deep_dives candidates, published the 6 the cap allowed, and marked all 85
seen permanently. Ten Brendan Gregg posts, twenty from jvns and forty from Dan
Luu were spent to publish six, and being permanent they could never be reached
again.

Two independent things had to be true for that to happen — `retention_days:
null` and a store that recorded candidates — and each looked reasonable on its
own. Both are tested here.

No network, no model, no API key.
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curate  # noqa: E402

FAILURES: list[str] = []


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}\n          got : {got}\n          want: {want}")


class Story:
    """Stands in for summarizers.Summary — only source_article is read."""
    def __init__(self, art):
        self.source_article = art


def art(key, category="deep_dives"):
    return {"key": key, "category": category, "title": key, "url": f"https://ex.com/{key}"}


def main() -> int:
    print("\n-- a scored-but-unpublished candidate must NOT be recorded --")
    # The shape of the real failure: a whole archive ranked, a capped few
    # published.
    ranked = [art(f"gregg{i:02d}") for i in range(10)]
    stories = [Story(ranked[0]), Story(ranked[1])]
    seen: dict = {}
    added = curate.record_published(seen, ranked, stories)

    check("only the published items are recorded", added, 2)
    check("seen holds exactly the published keys",
          sorted(seen), ["gregg00", "gregg01"])
    unpublished = [a["key"] for a in ranked[2:]]
    check("every scored-but-unpublished candidate is ABSENT from seen",
          [k for k in unpublished if k in seen], [])
    check("the recorded entry carries its category",
          seen["gregg00"]["category"], "deep_dives")

    print("\n-- the old behaviour, for contrast --")
    check("recording all candidates would have burned the archive",
          len(ranked) - added, 8)

    print("\n-- re-running does not re-stamp an item already recorded --")
    first_date = seen["gregg00"]["date"]
    again = curate.record_published(seen, ranked, stories)
    check("no duplicate entries added", again, 0)
    check("the original date is preserved", seen["gregg00"]["date"], first_date)

    print("\n-- retention: forever really is forever, 45d really expires --")
    policies = {
        "deep_dives": {**curate.POLICY_DEFAULTS, "retention_days": None},
        "aggregators": {**curate.POLICY_DEFAULTS, "retention_days": 45},
    }
    ancient = (datetime.now(timezone.utc) - timedelta(days=400)).isoformat()
    store = {
        "keep_forever": {"date": ancient, "category": "deep_dives"},
        "expire_me":    {"date": ancient, "category": "aggregators"},
        "legacy_entry": {"date": ancient, "category": None},
    }
    with tempfile.TemporaryDirectory() as td:
        curate.STATE_DIR = Path(td)
        curate.SEEN_FILE = Path(td) / "seen.json"
        curate.save_seen(store, policies)
        written = json.loads(curate.SEEN_FILE.read_text())

    check("a deep_dives entry 400 days old is KEPT", "keep_forever" in written, True)
    check("an aggregators entry 400 days old is dropped", "expire_me" in written, False)
    check("a legacy entry with no category expires at the 45-day default",
          "legacy_entry" in written, False)

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All seen-store tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
