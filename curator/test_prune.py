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

    # The case the report asked for explicitly, with NO legacy post involved:
    # both posts carry addedAt, and the one with the OLDER pubDate must survive
    # because it was added here more recently.
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        curate.CONTENT_DIR = d
        old_article_new_here = post(d, "2024-11-02", recent, "brendan-gregg-flame-graphs")
        new_article_old_here = post(d, "2026-09-10", older, "todays-funding-round")

        print("\n-- old pubDate + new addedAt beats new pubDate + old addedAt --")
        check("pruned exactly one", curate.prune_posts(1), 1)
        check("the 2024 article added 5 minutes ago SURVIVES",
              old_article_new_here.exists(), True)
        check("the 2026 article added 9 days ago is pruned",
              new_article_old_here.exists(), False)

    # Legacy ordering is DEFINED, not incidental: no addedAt sorts before every
    # addedAt, and legacy posts sort among themselves by filename.
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        curate.CONTENT_DIR = d
        l_old = post(d, "2026-09-01", None, "older-legacy")
        l_new = post(d, "2026-09-09", None, "newer-legacy")
        modern = post(d, "2020-01-01", recent, "ancient-article-added-today")

        print("\n-- legacy ordering --")
        keys = [curate._added_at(x) for x in (l_old, l_new, modern)]
        check("a post without addedAt keys on '0' + filename", keys[0][0], "0")
        check("a post with addedAt keys on 'A' + timestamp", keys[2][0], "A")
        check("every legacy post sorts before every addedAt post",
              max(keys[0], keys[1]) < keys[2], True)
        check("legacy posts sort among themselves by filename",
              keys[0] < keys[1], True)
        check("pruning two takes both legacy posts, oldest filename first",
              (curate.prune_posts(1), l_old.exists(), l_new.exists(), modern.exists()),
              (2, False, False, True))

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All prune tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
