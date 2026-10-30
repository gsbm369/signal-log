#!/usr/bin/env python3
"""buzz.py must report only what it measured, and touch nothing else.

No network: every lookup is answered by a fake Algolia. Each case below is a
way the buzz field could LIE to the Instagram agent that reads it:

  - another story from the same site counted as this one (Algolia's url search
    is full-text: a Verge URL returns other Verge stories)
  - a failed lookup written as 0 ("could not see" becomes "nobody cared")
  - a refresh that rewrites addedAt or any other line of the post
  - a post rewritten every cycle although nothing changed (git churn)
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import buzz  # noqa: E402

FAILURES: list[str] = []
URL = "https://www.theverge.com/tech/101/phone-screen-cracks"
POST = f"""---
title: "Phone screen cracks"
description: "x"
pubDate: 2026-10-29T10:00:00+00:00
addedAt: 2026-10-29T12:17:00+00:00
source: "The Verge"
category: gadgets
sourceUrl: "{URL}?utm_source=rss"
heat: 80
score: 1.2
readMinutes: 1
---

Body stays.
"""


def hit(url, points, comments=0):
    return {"url": url, "points": points, "num_comments": comments}


def fake(hits=None, fail=False):
    calls = []

    def fetch(q):
        calls.append(q)
        if fail:
            raise TimeoutError("planted")
        return {"hits": hits or []}
    fetch.calls = calls
    return fetch


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)


def main() -> int:
    same_site = hit("https://www.theverge.com/tech/999/a-different-story", 900, 400)
    check("a different story on the same site is not counted",
          buzz.hn_lookup(URL, fake([same_site])) == (0, 0))
    check("the same URL (scheme, www, utm, trailing slash ignored) is counted",
          buzz.hn_lookup(URL, fake([hit("http://theverge.com/tech/101/phone-screen-cracks/", 42, 7)])) == (42, 7))
    check("of several submissions, the best one is reported with its own comments",
          buzz.hn_lookup(URL, fake([hit(URL, 12, 90), hit(URL, 310, 140), same_site])) == (310, 140))
    check("a failed lookup is unknown (None), never zero", buzz.hn_lookup(URL, fake(fail=True)) is None)
    check("a malformed answer is unknown", buzz.hn_lookup(URL, lambda q: {"nope": 1}) is None)

    check("buzz 0 points -> 0", buzz.buzz_from(0) == 0)
    check("buzz full points -> 100", buzz.buzz_from(buzz.BUZZ_FULL_POINTS) == 100)
    check("buzz is capped at 100", buzz.buzz_from(50_000) == 100)
    vals = [buzz.buzz_from(p) for p in (1, 5, 20, 80, 300)]
    check("buzz rises with points", vals == sorted(vals) and len(set(vals)) == 5, str(vals))

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        p = d / "post.md"

        p.write_text(POST)
        st = buzz.refresh(d, fake(fail=True))
        check("a failed lookup leaves the post byte-identical", p.read_text() == POST)
        check("  ... and is counted as failed, not changed",
              st["buzz_failed"] == 1 and st["buzz_changed"] == 0, str(st))

        st = buzz.refresh(d, fake([hit(URL, 310, 140)]))
        out = p.read_text()
        check("a measured story gets hnPoints, hnComments and buzz",
              "hnPoints: 310\n" in out and "hnComments: 140\n" in out
              and f"buzz: {buzz.buzz_from(310)}\n" in out, out)
        before = [l for l in POST.splitlines()]
        after = [l for l in out.splitlines() if not l.startswith(buzz.FIELDS)]
        check("every other line, addedAt included, is unchanged", before == after)
        check("  ... counted as changed and on HN", st["buzz_changed"] == 1 and st["buzz_on_hn"] == 1, str(st))

        st = buzz.refresh(d, fake([hit(URL, 310, 140)]))
        check("unchanged values do not rewrite the post", p.read_text() == out and st["buzz_changed"] == 0, str(st))

        st = buzz.refresh(d, fake(fail=True))
        check("a later failed lookup keeps the last measured value", p.read_text() == out)

        st = buzz.refresh(d, fake([hit(URL, 450, 200)]))
        out2 = p.read_text()
        check("rising points are written in place, no duplicate lines",
              out2.count("hnPoints:") == 1 and "hnPoints: 450\n" in out2, out2)

        p.write_text(POST)
        buzz.refresh(d, fake([]))
        check("looked up with no submission is a measured zero",
              "hnPoints: 0\n" in p.read_text() and "buzz: 0\n" in p.read_text())

        p.write_text(POST)
        st = buzz.refresh(d, fake([hit(URL, 9)]), budget_s=-1)
        check("posts past the budget are skipped and left as they were",
              p.read_text() == POST and st["buzz_skipped"] == 1, str(st))

    src = (HERE / "ranker.py").read_text()
    check("the ranker reads none of the buzz fields",
          not any(f in src for f in ("buzz", "hnPoints", "hnComments")))

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All buzz tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
