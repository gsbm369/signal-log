"""Buzz: how much attention a story drew OUTSIDE this site.

`heat` is not this. heat is the ranker's score scaled against the best story
of the same run — trust x freshness x relevance, an editorial number that says
nothing about whether anyone read, shared or argued about the story. A
consumer of the RSS feed (the Instagram agent) that picks by heat is picking
by our own opinion of the story and calling it popularity.

This module measures one external signal, exactly, and refuses to guess:

  hnPoints    points of the highest-scoring Hacker News submission of THIS URL
  hnComments  comments on that same submission
  buzz        hnPoints on a 0-100 log scale (BUZZ_FULL_POINTS -> 100)

Three states, kept distinct because conflating them is the whole failure mode:

  fields absent   never looked up, or every lookup failed. UNKNOWN.
  hnPoints: 0     looked up; no submission of this URL exists. A measured zero.
  hnPoints: N     looked up; the best submission has N points.

A failed lookup leaves the post byte-identical. Writing 0 on a timeout would
turn "we could not see" into "nobody cared", and the agent would act on it.

Matching is on the CANONICAL URL (ranker.canonical_url), never on the domain
or the title: Algolia's url search is full-text, and for a story on
theverge.com it happily returns other Verge stories with 900 points.

Refreshed every cycle for every live post, because points accrue after we
publish: a story written at 0 is often at 300 a day later. Only the three buzz
lines are touched, and a post whose values did not change is not rewritten.
Nothing here is read by the ranker; selection stays deterministic and
model-free, and the golden ranking test proves it did not move.
"""
from __future__ import annotations

import json
import logging
import math
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

import ranker

log = logging.getLogger("curator.buzz")

HN_SEARCH = "https://hn.algolia.com/api/v1/search"
BUZZ_FULL_POINTS = 500       # a front-page story; anything above is 100
LOOKUP_TIMEOUT_S = 8
REFRESH_BUDGET_S = 90        # the whole refresh, not per post
FIELDS = ("hnPoints", "hnComments", "buzz")

Fetch = Callable[[str], dict[str, Any]]


def _fetch_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={
        "User-Agent": "signal.log-curator/2.0 (+https://github.com/gsbm369)",
    })
    with urllib.request.urlopen(req, timeout=LOOKUP_TIMEOUT_S) as resp:
        return json.loads(resp.read(1_000_000))


def hn_lookup(url: str, fetch: Fetch = _fetch_json) -> tuple[int, int] | None:
    """(points, comments) of the best HN submission of exactly this URL.

    (0, 0) when HN has none. None when the lookup itself failed — the caller
    must treat that as unknown, never as zero.
    """
    want = ranker.canonical_url(url)
    if not want:
        return None
    q = urllib.parse.urlencode({
        "query": url, "restrictSearchableAttributes": "url",
        "tags": "story", "hitsPerPage": 20,
    })
    try:
        data = fetch(f"{HN_SEARCH}?{q}")
        hits = data["hits"]
    except Exception as exc:  # network, HTTP, JSON, shape: all "could not see"
        log.debug("hn lookup failed for %s: %s", url, exc)
        return None
    best: tuple[int, int] | None = None
    for h in hits:
        if ranker.canonical_url(h.get("url") or "") != want:
            continue
        pts, com = int(h.get("points") or 0), int(h.get("num_comments") or 0)
        if best is None or pts > best[0]:
            best = (pts, com)
    return best or (0, 0)


def buzz_from(points: int) -> int:
    if points <= 0:
        return 0
    return min(100, round(100 * math.log1p(points) / math.log1p(BUZZ_FULL_POINTS)))


_FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def _source_url(text: str) -> str | None:
    m = _FRONT.match(text)
    if not m:
        return None
    u = re.search(r'^sourceUrl:\s*"?(.*?)"?\s*$', m.group(1), re.M)
    return u.group(1) if u else None


def apply(text: str, points: int, comments: int) -> str:
    """The post with its buzz lines set; every other byte unchanged."""
    m = _FRONT.match(text)
    if not m:
        return text
    keep = [l for l in m.group(1).split("\n") if not l.startswith(tuple(f"{f}:" for f in FIELDS))]
    keep += [f"hnPoints: {points}", f"hnComments: {comments}", f"buzz: {buzz_from(points)}"]
    return "---\n" + "\n".join(keep) + "\n---\n" + text[m.end():]


def refresh(content_dir: Path, fetch: Fetch = _fetch_json, workers: int = 8,
            budget_s: float = REFRESH_BUDGET_S) -> dict[str, int]:
    """Look up every live post and rewrite those whose buzz changed.

    Flat counters, for the metrics record:
      buzz_posts    posts considered
      buzz_failed   lookups that failed (post left as it was)
      buzz_skipped  posts not reached inside the budget (left as they were)
      buzz_changed  posts rewritten
      buzz_on_hn    posts with at least one HN submission of their URL
    """
    posts = sorted(content_dir.glob("*.md"))
    stats = {"buzz_posts": len(posts), "buzz_failed": 0, "buzz_skipped": 0,
             "buzz_changed": 0, "buzz_on_hn": 0}
    deadline = time.monotonic() + budget_s

    def one(path: Path) -> tuple[Path, str, tuple[int, int] | None | str]:
        text = path.read_text(encoding="utf-8")
        if time.monotonic() > deadline:
            return path, text, "skipped"
        url = _source_url(text)
        return path, text, (hn_lookup(url, fetch) if url else None)

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        for path, text, res in pool.map(one, posts):
            if res == "skipped":
                stats["buzz_skipped"] += 1
                continue
            if res is None:
                stats["buzz_failed"] += 1
                continue
            points, comments = res
            stats["buzz_on_hn"] += points > 0 or comments > 0
            new = apply(text, points, comments)
            if new != text:
                path.write_text(new, encoding="utf-8")
                stats["buzz_changed"] += 1
    return stats
