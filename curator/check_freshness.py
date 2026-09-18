#!/usr/bin/env python3
"""Publish gate: nothing on the built home page may be older than seven days.

Owner policy, 2026-09-18 — freshness over everything, evergreen retired:

    age        = cycle start (UTC) minus the AUTHOR's publication date
    today      age <= 24h
    this week  age <= 7d, and the card must SAY so with a visible label
    older      must not be rendered at all

The curator prunes and the layout filters, so in a healthy cycle this finds
nothing. It exists because both of those are upstream of the thing the reader
actually sees: this parses the BUILT index.html, the artifact about to be
published, and refuses the publish if the policy does not hold there. A card
that renders without data-published is a failure, not a pass — it cannot be
allowed to hide from the gate by omitting the attribute.

It also writes max_rendered_age_days per section into metrics.json, which the
inverted shipping default then carries to Loki without anyone naming it.

Exit 0 compliant, 1 violation (publish must be refused), 2 cannot check.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

INDEX = Path(os.environ.get("BUILT_INDEX", "/app/site/dist/index.html"))
# The per-category pages ("+N more") render cards too, and the policy is about
# what a reader can see, not about which page it is on. Every one is checked.
CATEGORY_PAGES = INDEX.parent / "category"
STATE = Path(os.environ.get("STATE_DIR", "/data/state")) / "metrics.json"
FRESH_DAYS = float(os.environ.get("FRESHNESS_DAYS", "7"))

ARTICLE = re.compile(r"<article\b([^>]*)>(.*?)</article>", re.S)
ATTR = re.compile(r'([a-z-]+)="([^"]*)"')


def cycle_start() -> datetime:
    raw = os.environ.get("CYCLE_START_UTC", "")
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00")) if raw else None
    except ValueError:
        dt = None
    dt = dt or datetime.now(timezone.utc)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def judge(a: dict, inner: str, where: str, now: datetime) -> tuple[float | None, str | None]:
    """(age in hours, violation) for one rendered card."""
    href = (re.search(r'href="(/posts/[^"]+)"', inner) or [None, "?"])[1]
    pub = a.get("data-published")
    if not pub:
        return None, f"[{where}] card without data-published: {href}"
    try:
        dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
    except ValueError:
        return None, f"[{where}] unparseable data-published={pub!r}: {href}"
    age_h = (now - dt).total_seconds() / 3600
    if age_h > FRESH_DAYS * 24:
        return age_h, f"[{where}] {age_h / 24:.1f} days old, over the {FRESH_DAYS:.0f}-day limit: {href}"
    if age_h > 24 and 'data-label="this-week"' not in inner:
        return age_h, f"[{where}] {age_h / 24:.1f}d old with NO 'this week' label: {href}"
    return age_h, None


def main() -> int:
    if not INDEX.exists():
        print(f"  no built index at {INDEX} — cannot check")
        return 2
    now = cycle_start()
    html = INDEX.read_text(encoding="utf-8", errors="replace")

    violations: list[str] = []
    per: dict[str, dict] = {}
    urls: dict[str, str] = {}

    cards = ARTICLE.findall(html)
    for attrs_raw, inner in cards:
        a = dict(ATTR.findall(attrs_raw))
        section = a.get("data-section", "?")
        href = (re.search(r'href="(/posts/[^"]+)"', inner) or [None, "?"])[1]
        age_h, bad = judge(a, inner, section, now)
        if bad:
            violations.append(bad)
        if age_h is None:
            continue
        row = per.setdefault(section, {"cards": 0, "today": 0, "week": 0,
                                       "older": 0, "oldest_h": 0.0})
        row["cards"] += 1
        row["oldest_h"] = max(row["oldest_h"], age_h)
        if age_h > FRESH_DAYS * 24:
            row["older"] += 1
        elif age_h > 24:
            row["week"] += 1
        else:
            row["today"] += 1
        if href in urls:
            violations.append(f"[{section}] {href} already rendered in [{urls[href]}]")
        urls.setdefault(href, section)

    page_cards = 0
    for page in sorted(CATEGORY_PAGES.glob("*/index.html")) if CATEGORY_PAGES.is_dir() else []:
        where = f"/category/{page.parent.name}/"
        seen: set[str] = set()
        for attrs_raw, inner in ARTICLE.findall(page.read_text(encoding="utf-8", errors="replace")):
            page_cards += 1
            _, bad = judge(dict(ATTR.findall(attrs_raw)), inner, where, now)
            if bad:
                violations.append(bad)
            href = (re.search(r'href="(/posts/[^"]+)"', inner) or [None, "?"])[1]
            if href in seen:
                violations.append(f"[{where}] {href} rendered twice on the page")
            seen.add(href)

    print(f"\n-- rendered cards vs the {FRESH_DAYS:.0f}-day policy, clock {now:%Y-%m-%d %H:%M}Z --")
    print(f"   {'section':<15}{'cards':>6}{'today':>7}{'week':>6}{'>7d':>5}{'oldest':>9}")
    order = ["fold"] + sorted(k for k in per if k not in ("fold", "tail")) + ["tail"]
    for k in order:
        if k in per:
            r = per[k]
            print(f"   {k:<15}{r['cards']:>6}{r['today']:>7}{r['week']:>6}"
                  f"{r['older']:>5}{r['oldest_h'] / 24:>8.1f}d")

    # Into metrics.json; the inverted shipping default carries it to Loki as
    # max_rendered_age_days_<section> without ship_to_loki.py naming it.
    if STATE.exists():
        try:
            m = json.loads(STATE.read_text())
            m["max_rendered_age_days"] = {k: round(v["oldest_h"] / 24, 2) for k, v in per.items()}
            m["rendered_cards"] = sum(v["cards"] for v in per.values())
            m["freshness_violations"] = len(violations)
            STATE.write_text(json.dumps(m, indent=2))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  WARN: could not record metrics: {exc}")

    if not cards:
        print("  no cards rendered at all")
    if violations:
        # Summarise by KIND before truncating the list. With only the first N
        # lines printed, a clock-skew failure that produces twenty unlabelled
        # cards pushes the one genuinely stale card off the end of the output —
        # measured, when a planted 8-day post was violation #21 of 21.
        kinds = {"over the limit": sum("over the" in v for v in violations),
                 "week card without label": sum("NO 'this week' label" in v for v in violations),
                 "URL rendered twice": sum("already rendered" in v or "rendered twice" in v
                                           for v in violations),
                 "card without data-published": sum("without data-published" in v or "unparseable" in v
                                                    for v in violations)}
        print(f"\n  REFUSING TO PUBLISH — {len(violations)} violation(s):")
        for k, n in kinds.items():
            if n:
                print(f"    {n:>3} × {k}")
        # Stale cards first: they are the violations the policy exists for.
        ordered = sorted(violations, key=lambda v: "over the" not in v)
        for v in ordered[:20]:
            print(f"    {v}")
        if len(ordered) > 20:
            print(f"    … and {len(ordered) - 20} more")
        return 1
    if page_cards:
        print(f"  + {page_cards} card(s) on {len(list(CATEGORY_PAGES.glob('*/index.html')))} category page(s)")
    print(f"\n  {len(cards)} card(s), all within {FRESH_DAYS:.0f} days, every week-old card labelled, no URL twice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
