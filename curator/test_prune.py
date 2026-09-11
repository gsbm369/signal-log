#!/usr/bin/env python3
"""The pruner must keep what this site published most recently, not what its
AUTHOR published most recently.

This is the failure the newsletter pivot walked into: prune_posts sorted by
filename, and a filename begins with the article's own pubDate. On a news site
those coincide. On this one a Brendan Gregg post is dated 216 days ago, so under
a filename sort every evergreen story was first in line to be deleted. The
deep_dives category had a 100% publish rate and a 0% survival rate, and no
metric showed it because publishing and pruning are counted separately.

No network, no model, no API key.
"""
from __future__ import annotations

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


def post(dirpath: Path, pub: str, added: str | None, slug: str) -> Path:
    front = [f"title: \"{slug}\"", f"pubDate: {pub}T00:00:00+00:00"]
    if added:
        front.append(f"addedAt: {added}")
    p = dirpath / f"{pub}-{slug}.md"
    p.write_text("---\n" + "\n".join(front) + "\ncategory: deep_dives\n---\n\nbody\n")
    return p


def main() -> int:
    now = datetime.now(timezone.utc)
    recent = (now - timedelta(minutes=5)).isoformat()
    older = (now - timedelta(days=9)).isoformat()

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        curate.CONTENT_DIR = d

        # The whole point: an ANCIENT article this site published five minutes
        # ago, against a fresh news story it published nine days ago.
        evergreen = post(d, "2025-02-06", recent, "flame-graphs-revisited")
        stale_news = post(d, "2026-09-09", older, "quarterly-results-roundup")
        legacy = post(d, "2026-09-08", None, "written-before-addedat-existed")

        print("\n-- keeping 2 of 3 --")
        removed = curate.prune_posts(2)
        check("pruned exactly one", removed, 1)
        check("the 216-day-old post published 5 minutes ago SURVIVES",
              evergreen.exists(), True)
        check("a legacy post with no addedAt is pruned first", legacy.exists(), False)
        check("the recent-dated news story survives on its addedAt",
              stale_news.exists(), True)

        print("\n-- under the OLD filename sort this is what happened --")
        by_filename = sorted(p.name for p in (evergreen, stale_news, legacy))
        check("filename order would have deleted the evergreen post first",
              by_filename[0], evergreen.name)

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All prune tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
