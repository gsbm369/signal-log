#!/usr/bin/env python3
"""
GOLDEN TEST — freezes the full ranked ORDER of a fixed fixture.

Filter tests prove a stage fires. They cannot catch the failure that matters
most here: a change to HALF_LIFE_HOURS, TITLE_HIT_WEIGHT, RELEVANCE_SCALE or a
source weight that silently degrades ranking quality while every filter still
passes.

This asserts the exact output order for a frozen set of items at fixed
timestamps. Any change to the scoring constants produces a diff that has to be
consciously approved rather than drifting in unnoticed.

It also documents the decisions: the commentary on each expected position says
WHY that story outranks the next one.

To re-approve after an intentional constant change:
    python3 curator/test_ranker_golden.py --print
and paste the emitted block over EXPECTED_ORDER.

Run:  python3 curator/test_ranker_golden.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ranker  # noqa: E402

# Frozen clock. Every fixture age is relative to this, so the test is
# deterministic regardless of when it runs.
NOW = datetime(2026, 9, 5, 12, 0, 0, tzinfo=timezone.utc)

SOURCE_WEIGHTS = {
    "Hacker News": 3.0,
    "TechCrunch": 2.0,
    "Ars Technica": 2.0,
    "LWN": 1.0,
    "Random Blog": 1.0,
}


def item(title, source, hours_old, summary="", url=None):
    # URLs are explicit, never derived from the title. Deriving them made two
    # "different" fixtures collide on a truncated slug, so a title-dedupe
    # assertion was silently being satisfied by the URL-dedupe stage instead.
    assert url, f"fixture {title!r} needs an explicit url"
    return {
        "title": title, "source": source, "summary": summary, "url": url,
        "published": NOW - timedelta(hours=hours_old),
    }


# --------------------------------------------------------------------------- #
# The fixture. Deliberately contains every tension the ranker must resolve.
# --------------------------------------------------------------------------- #

FIXTURE = [
    # Strong source, fresh, focus terms in the TITLE ("exploited", "rce").
    item("Actively exploited RCE in Chromium sandbox", "Hacker News", 2,
         "A CVE with an exploit in the wild.", url="https://ex.com/chromium-rce"),

    # Same story reworded, weaker source, older -> deduped on normalised TITLE
    # (its URL is deliberately different, so only the title stage can catch it).
    item("Actively exploited RCE in Chromium sandbox!", "TechCrunch", 6,
         "cve exploit", url="https://other.com/chromium-sandbox-rce-bug"),

    # The LWN trap: headline says nothing, body stuffed with five focus terms.
    # Title-first classification must give this 0 relevance.
    item("Security updates for Thursday", "LWN", 1,
         "Updates for kubernetes, docker, postgres, python and the linux kernel.",
         url="https://lwn.net/Articles/1001/"),

    # Relevant headline but a full half-life old (36h -> x0.5). 4th HN item,
    # so the per-source cap should remove it.
    item("Kubernetes 1.35 ships with in-place pod resizing", "Hacker News", 36,
         "kubernetes release", url="https://ex.com/k8s-135"),

    # Fresh, heavy source, zero focus terms in the title.
    item("A rooster alarm clock app arrives on iOS", "TechCrunch", 1,
         "It crows at you.", url="https://ex.com/rooster"),

    # Weakest source, fresh, strong title relevance.
    item("Postgres 18 adds asynchronous IO", "Random Blog", 3,
         "postgres performance", url="https://ex.com/pg18-aio"),

    # 2nd and 3rd Hacker News items.
    item("Terraform provider for Proxmox reaches 1.0", "Hacker News", 8,
         "terraform proxmox", url="https://ex.com/tf-proxmox"),
    item("eBPF tracing lands in the mainline kernel", "Hacker News", 10,
         "ebpf linux", url="https://ex.com/ebpf-mainline"),

    # Noise: dropped outright despite being the freshest item in the set.
    item("Top 10 laptops for 2026", "Ars Technica", 0.5, "listicle",
         url="https://ex.com/top-10-laptops"),

    # Duplicate URL after canonicalisation (www + utm + trailing slash), and
    # deliberately LOWER-scoring than its twin so the survivor is the better one.
    item("Chromium sandbox escape under active attack", "Ars Technica", 20,
         "cve", url="https://www.ex.com/chromium-rce/?utm_source=newsletter"),

    # Stub: too short to be a story.
    item("Breaking news", "TechCrunch", 0.2, "docker kubernetes",
         url="https://ex.com/breaking"),
]

# --------------------------------------------------------------------------- #
# The frozen expectation. Regenerate with --print after an intentional change.
# --------------------------------------------------------------------------- #

EXPECTED_ORDER = [
    # 1. score=4.9651  rec=0.96  rel=4.0  Hacker News
    #    Heaviest source, nearly fresh, two title hits ("exploited", "rce").
    #    "exploited" only matches because `exploit` is a PREFIX term — with a
    #    strict ... it scored 2.0 and fell to third. This test caught that.
    "Actively exploited RCE in Chromium sandbox",

    # 2. score=4.4234  rec=0.86  rel=4.0  Hacker News
    #    Same source and relevance as #3; wins on being 2h fresher.
    "Terraform provider for Proxmox reaches 1.0",

    # 3. score=4.2563  rec=0.82  rel=4.0  Hacker News
    #    Third and last Hacker News item the per-source cap allows.
    "eBPF tracing lands in the mainline kernel",

    # 4. score=1.9619  rec=0.98  rel=0.0  TechCrunch
    #    A DELIBERATE, VISIBLE TRADEOFF: an irrelevant story from a weight-2.0
    #    source outranks a relevant one from a weight-1.0 source, because source
    #    weight is multiplicative with recency while relevance is an additive
    #    lift capped at +108% (RELEVANCE_CAP 6.0 x RELEVANCE_SCALE 0.18).
    #    Raising RELEVANCE_SCALE, or making relevance multiplicative, would flip
    #    #4 and #5. That is a real editorial choice — this line is where it is
    #    recorded, and changing it must be a conscious diff.
    "A rooster alarm clock app arrives on iOS",

    # 5. score=1.2837  rec=0.94  rel=2.0  Random Blog
    #    Weakest source, but relevance lifts it clear of the LWN digest below.
    "Postgres 18 adds asynchronous IO",

    # 6. score=0.9809  rec=0.98  rel=0.0  LWN
    #    THE LWN TRAP. Freshest item in the set (1h) with five focus terms in the
    #    body — kubernetes, docker, postgres, python, linux — and a headline that
    #    says nothing. Title-first classification gives it rel=0.0, so recency
    #    alone cannot carry it. Scoring combined title+summary put this FIRST.
    "Security updates for Thursday",

    # Absent by design:
    #   "Kubernetes 1.35 ..."          4th Hacker News item -> per-source cap
    #   "Actively exploited RCE ...!"  reworded twin        -> title dedupe
    #   "Chromium sandbox escape ..."  www+utm twin of #1   -> URL dedupe
    #   "Top 10 laptops for 2026"      listicle             -> noise filter
    #   "Breaking news"                two words            -> stub filter
]

EXPECTED_STATS = {"noise": 1, "stub": 1, "dupe_url": 1, "dupe_title": 1, "capped": 1}


def run():
    return ranker.rank(FIXTURE, SOURCE_WEIGHTS, per_source_cap=3, now=NOW)


def main() -> int:
    ranked, stats = run()

    if "--print" in sys.argv:
        print("EXPECTED_ORDER = [")
        for a in ranked:
            print(f'    {a["title"]!r},'
                  f'  # score={a["_score"]:.4f} rec={a["_recency"]:.2f} rel={a["_relevance"]:.1f}'
                  f' src={a["source"]}')
        print("]")
        print(f"EXPECTED_STATS = {{'noise': {stats['noise']}, 'stub': {stats['stub']}, "
              f"'dupe_url': {stats['dupe_url']}, 'dupe_title': {stats['dupe_title']}, "
              f"'capped': {stats['capped']}}}")
        return 0

    failures: list[str] = []
    got = [a["title"] for a in ranked]

    print("\n-- ranked order --")
    for i, a in enumerate(ranked):
        want = EXPECTED_ORDER[i] if i < len(EXPECTED_ORDER) else "<nothing expected>"
        ok = a["title"] == want
        print(f'  {"PASS" if ok else "FAIL"}  {i+1}. score={a["_score"]:.4f} '
              f'rec={a["_recency"]:.2f} rel={a["_relevance"]:.1f} {a["source"][:14]:<14} {a["title"][:52]}')
        if not ok:
            print(f'        expected: {want}')

    if got != EXPECTED_ORDER:
        failures.append("ranked order changed")
        print("\n  ORDER DIFF")
        print(f"    got : {got}")
        print(f"    want: {EXPECTED_ORDER}")

    print("\n-- filter stats --")
    for k, v in EXPECTED_STATS.items():
        ok = stats.get(k) == v
        print(f'  {"PASS" if ok else "FAIL"}  {k}={stats.get(k)} (expected {v})')
        if not ok:
            failures.append(f"stats.{k}")

    print("\n-- invariants that must hold whatever the constants are --")
    inv = [
        ("body-stuffed digest scores 0 relevance",
         next(a["_relevance"] for a in ranked if a["title"].startswith("Security updates")) == 0.0),
        ("digest does not take the top slot",
         not ranked[0]["title"].startswith("Security updates")),
        ("scores are non-increasing",
         all(ranked[i]["_score"] >= ranked[i + 1]["_score"] for i in range(len(ranked) - 1))),
        ("per-source cap respected",
         max(sum(1 for a in ranked if a["source"] == s) for s in SOURCE_WEIGHTS) <= 3),
        ("36h-old item decayed to half",
         abs(ranker.recency_factor(NOW - timedelta(hours=36), NOW) - 0.5) < 1e-9),
    ]
    for name, ok in inv:
        print(f'  {"PASS" if ok else "FAIL"}  {name}')
        if not ok:
            failures.append(name)

    print()
    if failures:
        print(f"FAILED: {failures}")
        print("If the change was intentional, re-approve with:")
        print("    python3 curator/test_ranker_golden.py --print")
        return 1
    print("Golden ranking matches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
