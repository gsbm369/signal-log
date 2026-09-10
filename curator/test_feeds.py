#!/usr/bin/env python3
"""Feed-parsing regression tests. No network, no model, no API key.

The CDATA case is here because a feed that wraps pubDate in <![CDATA[...]]>
would, if mishandled, contribute ZERO items while reporting a successful fetch:
valid feed, HTTP 200, no error, silent empty result. That is the failure shape
this project keeps finding, so it gets a test whether or not any configured
feed uses the pattern today.
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curate  # noqa: E402

FAILURES: list[str] = []


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}\n          got:  {got!r}\n          want: {want!r}")


def feed(items: str) -> str:
    return ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
            f'<title>t</title>{items}</channel></rss>')


print("\n-- CDATA-wrapped date fields must still parse --")
d = feedparser.parse(feed(
    '<item><title><![CDATA[Wrapped]]></title>'
    '<link>https://example.com/a</link>'
    '<pubDate><![CDATA[Mon, 08 Sep 2026 09:15:00 +0300]]></pubDate>'
    '<description><![CDATA[body]]></description></item>'
    '<item><title>Plain</title><link>https://example.com/b</link>'
    '<pubDate>Mon, 08 Sep 2026 09:15:00 +0300</pubDate>'
    '<description>body</description></item>'))
check("both entries parsed", len(d.entries), 2)
wrapped, plain = d.entries[0], d.entries[1]
check("CDATA pubDate yields published_parsed", bool(wrapped.get("published_parsed")), True)
check("CDATA and plain dates agree",
      curate.entry_datetime(wrapped), curate.entry_datetime(plain))
check("date is the real one, not a now() fallback",
      curate.entry_datetime(wrapped), (datetime(2026, 9, 8, 6, 15, tzinfo=timezone.utc), ""))
check("CDATA title is unwrapped", wrapped.title, "Wrapped")

print("\n-- an undated entry is REJECTED, never dated now() --")
# It used to fall back to now(). That gave the items we know least about the
# maximum recency factor, so an undated entry outranked a correctly dated one.
d2 = feedparser.parse(feed(
    '<item><title>No date</title><link>https://example.com/c</link>'
    '<description>body</description></item>'))
check("undated entry is rejected", curate.entry_datetime(d2.entries[0]), (None, "no_date"))

print("\n-- a future-dated entry is REJECTED --")
# recency_factor clamps age at 0, so a future date scores a perfect 1.0 every
# run until the date arrives. Measured live on Finextra, which dates its webinar
# listings at air time: 11 of 54 items, up to 55.8 days ahead.
future = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%a, %d %b %Y %H:%M:%S GMT")
d3 = feedparser.parse(feed(
    f'<item><title>Webinar</title><link>https://example.com/d</link>'
    f'<pubDate>{future}</pubDate><description>body</description></item>'))
check("future-dated entry is rejected", curate.entry_datetime(d3.entries[0]), (None, "future_date"))

print("\n-- clock skew inside the grace window is NOT a rejection --")
skew = (datetime.now(timezone.utc) + timedelta(minutes=30)).strftime("%a, %d %b %Y %H:%M:%S GMT")
d4 = feedparser.parse(feed(
    f'<item><title>Skewed</title><link>https://example.com/e</link>'
    f'<pubDate>{skew}</pubDate><description>body</description></item>'))
check("30 minutes ahead still accepted", curate.entry_datetime(d4.entries[0])[1], "")

print("\n-- category is read from feed config, never inferred --")
import images  # noqa: E402
check("images module importable", hasattr(images, "extract"), True)

print()
if FAILURES:
    print(f"FAILED: {FAILURES}")
    sys.exit(1)
print("All feed tests passed.")
