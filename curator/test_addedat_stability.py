#!/usr/bin/env python3
"""A post that survives a cycle must keep its addedAt.

WHY THIS IS THE MOST DAMAGING DEFECT THE PROJECT COULD HAVE, and the hardest to
see: addedAt is the feed's pubDate. If it were recomputed at build time rather
than written once per post, every subscriber would receive all 60 items as NEW
on every cycle — six times a day, for ever. The site would look perfect. The
curator metrics would be green. Only a person with a feed reader would know, and
they would unsubscribe rather than file a bug.

It is also invisible to a single observation: right after a big run, every
addedAt legitimately falls inside the same few minutes, which is exactly what
the broken version would produce too. Only a BEFORE and an AFTER across a cycle
can tell the two apart.

So this keeps its own snapshot in state/, compares every surviving post against
it, and updates it. Posts that were pruned are not failures; posts that changed
their addedAt are.

Exit 0 stable, 1 an addedAt moved, 2 nothing to compare yet.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTENT = Path(os.environ.get("CONTENT_DIR", HERE.parent / "site/src/content/posts"))
STATE = Path(os.environ.get("STATE_DIR", HERE / "state")) / "addedat.json"

ADDED = re.compile(r"^addedAt:\s*(\S+)\s*$", re.M)


def current() -> dict[str, str]:
    out = {}
    for f in sorted(CONTENT.glob("*.md")):
        m = ADDED.search(f.read_text(encoding="utf-8")[:1200])
        if m:
            out[f.name] = m.group(1)
    return out


def main() -> int:
    now = current()
    if not now:
        print("  no posts carry addedAt — nothing to compare")
        return 2

    if not STATE.exists():
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(now, indent=2, sort_keys=True))
        print(f"  first run — snapshotted {len(now)} post(s), nothing to compare yet")
        return 2

    before = json.loads(STATE.read_text())
    survivors = [k for k in before if k in now]
    moved = [(k, before[k], now[k]) for k in survivors if before[k] != now[k]]

    print(f"\n-- addedAt across cycles --")
    print(f"     tracked previously : {len(before)}")
    print(f"     survived           : {len(survivors)}")
    print(f"     pruned             : {len(before) - len(survivors)}")
    print(f"     new this cycle     : {len(set(now) - set(before))}")
    print(f"     addedAt MOVED      : {len(moved)}")

    STATE.write_text(json.dumps(now, indent=2, sort_keys=True))

    if moved:
        print("\n  FAIL — a surviving post changed its addedAt, so its RSS pubDate moved.")
        print("  Every subscriber will receive these as new items again:")
        for name, was, is_ in moved[:10]:
            print(f"    {name}\n      before {was}\n      after  {is_}")
        print("\n  addedAt must be written ONCE by write_post() and never recomputed.")
        return 1

    if not survivors:
        print("\n  nothing survived the last cycle — cannot conclude stability")
        return 2

    print(f"\n  {len(survivors)} surviving post(s) kept their addedAt. Feed pubDates are stable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
