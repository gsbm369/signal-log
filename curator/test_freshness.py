#!/usr/bin/env python3
"""The 7-day freshness policy, curator side. No network, no model, no API key.

Owner policy, 2026-09-18: age = cycle start minus the AUTHOR's date; nothing
older than seven days is ingested, stored or rendered, in any category.

The case that forced the policy into code: measured live the same morning, a
Dan Luu post at 110 days held a Deep Dives slot because the per-category floor
protects each category's newest three REGARDLESS OF AGE. Age must beat the
floor, including when that empties a category.
"""
from __future__ import annotations

import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curate  # noqa: E402

FAILURES: list[str] = []
NOW = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}\n          got : {got}\n          want: {want}")


def post(d: Path, slug: str, cat: str, author_age_days: float, added_age_days: float = 0) -> Path:
    pub = NOW - timedelta(days=author_age_days)
    added = NOW - timedelta(days=added_age_days)
    f = d / f"{pub:%Y-%m-%d}-{slug}.md"
    f.write_text(f'---\ntitle: "{slug}"\npubDate: {pub.isoformat()}\n'
                 f'addedAt: {added.isoformat()}\ncategory: {cat}\n---\n\nbody\n')
    return f


def main() -> int:
    os.environ["CATEGORY_FLOOR"] = "3"

    print("\n-- age beats the floor, even when it empties the category --")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); curate.CONTENT_DIR = d
        luu = post(d, "dan-luu-110d", "deep_dives", 110, added_age_days=0.1)
        news = [post(d, f"g{i}", "gaming", 0.2 * i) for i in range(4)]
        removed = curate.prune_by_age(NOW)
        check("the 110-day post is pruned", luu.exists(), False)
        check("even though it was deep_dives' ONLY post (floor would have kept it)",
              sorted(x.stem.split("-", 3)[-1] for x in d.glob("*deep_dives*")), [])
        check("fresh posts in other categories are untouched", all(f.exists() for f in news), True)
        check("exactly one removed", removed, 1)
        # And the floor, run afterwards as prune_posts does, cannot bring it back.
        curate.prune_posts(max_posts=60)
        check("prune_posts afterwards has nothing to protect", luu.exists(), False)

    print("\n-- the boundary is the author's date, not addedAt --")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); curate.CONTENT_DIR = d
        # Added to the site five minutes ago, written eight days ago: stale.
        added_now = post(d, "written-8d-added-now", "system_design", 8, added_age_days=0.003)
        # Added six days ago, written six days ago: fresh.
        six = post(d, "six-days", "system_design", 6, added_age_days=6)
        seven_minus = post(d, "just-inside", "system_design", 6.99)
        curate.prune_by_age(NOW)
        check("8-day author date is pruned though addedAt is minutes ago", added_now.exists(), False)
        check("6-day post survives", six.exists(), True)
        check("6.99-day post survives (the limit is inclusive of 7 days)", seven_minus.exists(), True)

    print("\n-- an unreadable date is not 'within a week' --")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); curate.CONTENT_DIR = d
        f = d / "nodate.md"; f.write_text("---\ntitle: x\ncategory: gaming\n---\nbody\n")
        curate.prune_by_age(NOW)
        check("a post with no pubDate is removed", f.exists(), False)

    print("\n-- the 10-per-category ceiling, inside the 7-day set --")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); curate.CONTENT_DIR = d
        g = [post(d, f"g{i:02d}", "gaming", 1, added_age_days=i * 0.01) for i in range(14)]
        s = [post(d, f"s{i}", "system_design", 1) for i in range(3)]
        curate.prune_posts(max_posts=60)
        left = sorted(x.name for x in d.glob("*.md") if "-g" in x.name)
        check("gaming is cut to 10", len(left), 10)
        check("the four OLDEST-ADDED gaming posts went", [x.exists() for x in g[-4:]], [False] * 4)
        check("another category below the ceiling is untouched", all(x.exists() for x in s), True)

    print("\n-- LWN [$]: effective date is the RIPENING date --")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); curate.CONTENT_DIR = d
        # Ripened (became free) at NOW; the author wrote it nine days earlier.
        ripe_at = NOW
        os.environ["CYCLE_START_UTC"] = ripe_at.isoformat()
        check("cycle_start() is the ripening instant", curate.cycle_start(), ripe_at)
        # The REAL path: ripened_article() is exactly what _run() appends.
        rec = {"key": "k", "url": "https://lwn.net/Articles/1/", "title": "ripened",
               "source": "LWN.net", "category": "devops_linux",
               "first_seen": (NOW - timedelta(days=9)).isoformat()}
        art = curate.ripened_article(rec)
        check("ripened_article() dates it at the ripening instant, not first_seen",
              art["published"], ripe_at)
        pub = art["published"]
        f = d / f"{pub:%Y-%m-%d}-lwn-ripened.md"
        f.write_text(f'---\ntitle: "ripened"\npubDate: {pub.isoformat()}\n'
                     f'addedAt: {pub.isoformat()}\ncategory: devops_linux\n---\n\nbody\n')
        curate.prune_by_age(ripe_at)
        check("published on the ripening day", f.exists(), True)
        curate.prune_by_age(ripe_at + timedelta(days=6))
        check("still live six days after ripening", f.exists(), True)
        curate.prune_by_age(ripe_at + timedelta(days=8))
        check("aged out eight days after ripening", f.exists(), False)
        # Had it been dated by first_seen (nine days before ripening), it would
        # have been born expired:
        born = NOW - timedelta(days=9)
        check("dated by first_seen it would already be over the limit",
              (ripe_at - born) > timedelta(days=7), True)
        os.environ.pop("CYCLE_START_UTC", None)

    print("\n-- no configuration can widen ingest past seven days --")
    pol = curate.feed_policy({"category": "deep_dives", "ingest_days": 3650},
                             {"deep_dives": {**curate.POLICY_DEFAULTS, "ingest_days": 3650}})
    check("deep_dives' old 3650-day window is capped at 7", pol["ingest_days"], 7.0)

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All freshness tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
