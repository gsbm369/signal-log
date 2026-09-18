#!/usr/bin/env python3
"""The built home page must be EXACTLY the owner's reference selection.

This is an independent implementation of the reference, written from the
owner's spec rather than from index.astro, compared slot by slot against the
built index.html. Two implementations agreeing is evidence; one implementation
checked against itself is not.

  tier     today if age <= 24h, week if age <= 7d, otherwise excluded
           (age = sample time - AUTHOR date)
  order    today before week; within a tier, score best first; then id
  fold     tier == today, by order, first 5
  section  fixed order; pool = category, not in fold, not excluded, by order;
           at most 2 per source in a section (Petri: 1); first 6
           week cards labelled; empty -> "No new posts this week."

Exit 0 identical, 1 mismatch, 2 cannot check.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

POSTS = Path(os.environ.get("CONTENT_DIR", "/app/site/src/content/posts"))
INDEX = Path(os.environ.get("BUILT_INDEX", "/app/site/dist/index.html"))
ORDER = ["microsoft", "system_design", "devops_linux", "languages", "company_eng",
         "deep_dives", "fintech", "aggregators", "gaming"]
PER_SOURCE = {"Petri": 1}
FM = lambda k: re.compile(rf'^{k}:\s*"?(.*?)"?\s*$', re.M)


def clock() -> datetime:
    raw = os.environ.get("CYCLE_START_UTC", "")
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00")) if raw else datetime.now(timezone.utc)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def load(now):
    out = []
    for f in POSTS.glob("*.md"):
        t = f.read_text(encoding="utf-8")[:1500]
        g = lambda k, d="": (FM(k).search(t).group(1) if FM(k).search(t) else d)
        pub = datetime.fromisoformat(g("pubDate").replace("Z", "+00:00"))
        age_h = (now - pub).total_seconds() / 3600
        tier = "today" if age_h <= 24 else "week" if age_h <= 7 * 24 else "stale"
        out.append({"id": f.stem, "cat": g("category", "aggregators"), "src": g("source"),
                    "score": float(g("score", "0") or 0), "tier": tier})
    return out


def expected(posts, declared):
    rank = {"today": 0, "week": 1}
    elig = sorted((p for p in posts if p["tier"] != "stale"),
                  key=lambda p: (rank[p["tier"]], -p["score"], p["id"]))
    fold = [p["id"] for p in elig if p["tier"] == "today"][:5]
    secs = {}
    for cat in [c for c in ORDER if c in declared]:
        seen, items = {}, []
        for p in elig:
            if len(items) == 6:
                break
            if p["cat"] != cat or p["id"] in fold:
                continue
            if seen.get(p["src"], 0) >= PER_SOURCE.get(p["src"], 2):
                continue
            seen[p["src"]] = seen.get(p["src"], 0) + 1
            items.append(p["id"])
        secs[cat] = items
    return fold, secs


def rendered(html):
    ids = lambda chunk, sec: [m for m in re.findall(
        rf'<article\b[^>]*data-section="{sec}"[^>]*>.*?href="/posts/([^"/]+)/?"', chunk, re.S)]
    fold = ids(html, "fold")
    secs = {k: ids(body, k) for k, body in
            re.findall(r'<section[^>]*data-section="([a-z_]+)"[^>]*>(.*?)</section>', html, re.S)}
    order = re.findall(r'<section[^>]*data-section="([a-z_]+)"', html)
    empty = {k for k, body in re.findall(r'<section[^>]*data-section="([a-z_]+)"[^>]*>(.*?)</section>', html, re.S)
             if "No new posts this week." in body}
    return fold, secs, order, empty


def main() -> int:
    if not (INDEX.exists() and POSTS.exists()):
        print("  cannot check: built index or posts missing")
        return 2
    now = clock()
    posts = load(now)
    html = INDEX.read_text(encoding="utf-8")
    declared = set(re.findall(r'<section[^>]*data-section="([a-z_]+)"', html))
    ef, es = expected(posts, declared)
    rf, rs, rorder, empty = rendered(html)

    bad = []
    if rf != ef:
        bad.append(f"fold differs\n      expected {ef}\n      rendered {rf}")
    want_order = [c for c in ORDER if c in declared]
    if rorder != want_order:
        bad.append(f"section order {rorder} != {want_order}")
    for cat in want_order:
        if rs.get(cat, []) != es[cat]:
            bad.append(f"[{cat}] differs\n      expected {es[cat]}\n      rendered {rs.get(cat)}")
        if not es[cat] and cat not in empty:
            bad.append(f"[{cat}] is empty but lacks 'No new posts this week.'")

    print(f"\n-- built page vs the owner's reference selection, clock {now:%Y-%m-%d %H:%M}Z --")
    print(f"   fold      expected {len(ef)}  rendered {len(rf)}  {'MATCH' if rf == ef else 'DIFFERS'}")
    for cat in want_order:
        print(f"   {cat:<15} expected {len(es[cat])}  rendered {len(rs.get(cat, []))}  "
              f"{'MATCH' if rs.get(cat, []) == es[cat] else 'DIFFERS'}")
    missing = [c for c in ORDER if c not in declared]
    if missing:
        print(f"   (not declared on this site, so no section: {', '.join(missing)})")
    if bad:
        print("\n  SELECTION DOES NOT MATCH THE REFERENCE:")
        for b in bad:
            print(f"    {b}")
        return 1
    print("\n  every slot matches the reference exactly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
