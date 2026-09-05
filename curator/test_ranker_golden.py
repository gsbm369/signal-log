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

# Narrow band, as in the original. Hacker News sits at the floor.
SOURCE_WEIGHTS = {
    "Ars Technica": 1.10,
    "LWN": 1.10,
    "TechCrunch": 0.95,
    "Random Blog": 0.90,
    "Hacker News": 0.85,
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
    # Lowest-weight source, fresh, two title hits ("exploited", "rce").
    # Relevance must carry this past heavier but irrelevant sources.
    item("Actively exploited RCE in Chromium sandbox", "Hacker News", 2,
         "A CVE with an exploit in the wild.", url="https://ex.com/chromium-rce"),

    # Same story reworded, different URL -> only the title stage can catch it.
    item("Actively exploited RCE in Chromium sandbox!", "TechCrunch", 6,
         "cve exploit", url="https://other.com/chromium-sandbox-rce-bug"),

    # THE NOISE LIST, verbatim pattern /^security updates for /i. Freshest item
    # in the set; must be dropped before scoring ever runs.
    item("Security updates for Thursday", "LWN", 1,
         "Updates for kubernetes, docker, postgres, python and the linux kernel.",
         url="https://lwn.net/Articles/1001/"),

    # THE TITLE-FIRST TRAP, and not caught by any noise pattern. Headline carries
    # no focus term; body carries four. Must score relevance 1.15 (topic bonus
    # only, no focus hits) rather than 3.0.
    item("Architecting memory and storage in the AI era", "Ars Technica", 1,
         "Covers kubernetes, docker, inference and the linux kernel in depth.",
         url="https://ex.com/architecting-memory"),

    # Relevant headline but a full half-life old (36h -> x0.5). 4th Hacker News
    # item, so the per-source cap removes it.
    item("Kubernetes 1.35 ships with in-place pod resizing", "Hacker News", 36,
         "kubernetes release", url="https://ex.com/k8s-135"),

    # Fresh, heavier source, zero focus terms. Under an ADDITIVE relevance this
    # outranked the Postgres item below; under a multiplicative one it must not.
    item("A rooster alarm clock app arrives on iOS", "TechCrunch", 1,
         "It crows at you.", url="https://ex.com/rooster"),

    # Lightest source, fresh, one title hit. The additive-vs-multiplicative test.
    item("Postgres 18 adds asynchronous IO", "Random Blog", 3,
         "postgres performance", url="https://ex.com/pg18-aio"),

    # Further Hacker News items, so the per-source cap of 3 actually fires.
    item("Grafana 12 adds native Loki trace correlation", "Hacker News", 5,
         "grafana loki observability", url="https://ex.com/grafana-12"),
    item("Terraform provider for Proxmox reaches 1.0", "Hacker News", 8,
         "terraform proxmox", url="https://ex.com/tf-proxmox"),
    item("eBPF tracing lands in the mainline kernel", "Hacker News", 10,
         "ebpf linux", url="https://ex.com/ebpf-mainline"),

    # Extra-list noise (listicle). Not in the ported list; this project's feeds
    # produce these and the original's never did.
    item("Top 10 laptops for 2026", "Ars Technica", 0.5, "listicle",
         url="https://ex.com/top-10-laptops"),

    # Duplicate URL after canonicalisation, deliberately lower-scoring than its
    # twin so the survivor is the better one.
    item("Chromium sandbox escape under active attack", "Ars Technica", 20,
         "cve", url="https://www.ex.com/chromium-rce/?utm_source=newsletter"),

    # Stub.
    item("Breaking news", "TechCrunch", 0.2, "docker kubernetes",
         url="https://ex.com/breaking"),
]

# --------------------------------------------------------------------------- #
# The frozen expectation. Regenerate with --print after an intentional change.
# --------------------------------------------------------------------------- #

EXPECTED_ORDER = [
    # 1. 1.8197 = rec 0.89 x w 0.95 x rel 2.15   TechCrunch
    #    NOTE: this is the REWORDED TWIN, not the Hacker News original, which is
    #    4h fresher. TechCrunch 0.95 vs Hacker News 0.85 outweighs 4 hours of
    #    decay, so dedupe keeps the TechCrunch copy. Correct under the model and
    #    worth freezing: within a narrow band, source can still decide a tie.
    "Actively exploited RCE in Chromium sandbox!",

    # 2. 1.6598 = rec 0.91 x w 0.85 x rel 2.15   Hacker News
    #    Two title hits (grafana, loki). Beats #3 and #4 on recency alone.
    "Grafana 12 adds native Loki trace correlation",

    # 3. 1.5666 = rec 0.86 x w 0.85 x rel 2.15   Hacker News
    "Terraform provider for Proxmox reaches 1.0",

    # 4. 1.5074 = rec 0.82 x w 0.85 x rel 2.15   Hacker News
    #    Third and last Hacker News item the per-source cap allows.
    "eBPF tracing lands in the mainline kernel",

    # 5. 1.4017 = rec 0.94 x w 0.90 x rel 1.65   Random Blog
    #    THE MULTIPLICATIVE-RELEVANCE TEST. One title hit on the LIGHTEST source
    #    in the set, and it still beats the irrelevant TechCrunch item at #7.
    #    Under the previous additive lift this sat BELOW the rooster app: source
    #    weight was doing the ranking. Relevance and weight now compete in the
    #    same unit, so 0.90 x 1.65 = 1.49 beats 0.95 x 1.00 = 0.95.
    "Postgres 18 adds asynchronous IO",

    # 6. 1.2409 = rec 0.98 x w 1.10 x rel 1.15   Ars Technica
    #    THE TITLE-FIRST TRAP. Body names kubernetes, docker, inference and the
    #    linux kernel; the headline names none of them. rel = 1.15 is the topic
    #    bonus ALONE — zero focus hits. Scoring combined text would give this
    #    1 + 4x0.5 + 0.15 = 3.15 and put it first. Not caught by any noise
    #    pattern, so only title-first classification stops it.
    "Architecting memory and storage in the AI era",

    # 7. 0.9319 = rec 0.98 x w 0.95 x rel 1.00   TechCrunch
    #    Freshest survivor, decent source, zero topics -> neutral 1.0 multiplier.
    "A rooster alarm clock app arrives on iOS",

    # Absent by design:
    #   "Security updates for Thursday"   ported NOISE /^security updates for /i
    #   "Top 10 laptops for 2026"         extra NOISE (listicle)
    #   "Actively exploited RCE ..."      HN original -> title dedupe, lost to #1
    #   "Chromium sandbox escape ..."     www+utm twin -> URL dedupe
    #   "Kubernetes 1.35 ..."             4th Hacker News item -> per-source cap
    #   "Breaking news"                   two words -> stub filter
]

EXPECTED_STATS = {"noise": 2, "stub": 1, "dupe_url": 1, "dupe_title": 1, "capped": 1}


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
        ("noise-listed digest never reaches scoring",
         not any(a["title"].startswith("Security updates") for a in ranked)),
        ("body-stuffed item gets the topic bonus only, no focus hits",
         abs(next(a["_relevance"] for a in ranked
                  if a["title"].startswith("Architecting")) - 1.15) < 1e-9),
        ("body-stuffed item does not take the top slot",
         not ranked[0]["title"].startswith("Architecting")),
        ("relevance multiplies: a relevant light source beats an irrelevant heavier one",
         [a["title"] for a in ranked].index("Postgres 18 adds asynchronous IO")
         < [a["title"] for a in ranked].index("A rooster alarm clock app arrives on iOS")),
        ("source weights stay inside the band",
         all(ranker.SOURCE_WEIGHT_MIN <= a["_weight"] <= ranker.SOURCE_WEIGHT_MAX for a in ranked)),
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
