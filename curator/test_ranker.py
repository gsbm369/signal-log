#!/usr/bin/env python3
"""Tests for the deterministic ranker. No network, no model, no API key.

Run:  python3 curator/test_ranker.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ranker  # noqa: E402

NOW = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)
FAILURES: list[str] = []


def check(name: str, got, want) -> None:
    if got == want:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}\n          got:  {got!r}\n          want: {want!r}")


def check_true(name: str, cond, detail: str = "") -> None:
    check(name, bool(cond) or detail or False, True)


def art(title, source="X", hours_old=0.0, summary="", url=None):
    return {
        "title": title, "source": source, "summary": summary,
        "url": url or f"https://example.com/{abs(hash(title))}",
        "published": NOW - timedelta(hours=hours_old),
    }


print("\n-- recency decay (36h half-life) --")
check("fresh article scores 1.0", round(ranker.recency_factor(NOW, NOW), 3), 1.0)
check("36h old scores 0.5", round(ranker.recency_factor(NOW - timedelta(hours=36), NOW), 3), 0.5)
check("72h old scores 0.25", round(ranker.recency_factor(NOW - timedelta(hours=72), NOW), 3), 0.25)
check("future date clamps to 1.0", round(ranker.recency_factor(NOW + timedelta(hours=5), NOW), 3), 1.0)

print("\n-- focus-stack matching is word-bounded (the 'arm' bug) --")
for text in ["Clucky's new alarm app wakes you", "Global warming will exceed limits",
             "working on a frame for this", "disarm the alert"]:
    score, matched = ranker.relevance_hits(text, "")
    check(f"no false 'arm' in {text[:28]!r}", "arm" in matched, False)
check("real ARM still matches", "arm" in ranker.relevance_hits("New ARM server chip", "")[1], True)
check("'go' no longer matches prose", "golang" in ranker.relevance_hits("we go to press", "")[1], False)
check("golang matches", "golang" in ranker.relevance_hits("A golang rewrite", "")[1], True)
check("prefix term fine-tun matches fine-tuning",
      "fine-tun" in ranker.relevance_hits("fine-tuning a model", "")[1], True)
check("title hit outweighs summary hit",
      ranker.relevance_hits("kubernetes news", "")[0] > ranker.relevance_hits("x", "kubernetes news")[0], True)

print("\n-- noise filter --")
for t in ["Daily digest: everything that happened", "Top 10 laptops for 2026",
          "Best 5 ways to speed up Docker", "Ask HN: what do you use?",
          "Who is hiring? (September 2026)", "Black Friday deals on SSDs",
          "Everything you need to know about AI"]:
    check_true(f"noise: {t[:34]!r}", ranker.is_noise(t))
for t in ["Actively exploited sandbox RCE in Chromium", "Postgres 18 released"]:
    check(f"not noise: {t[:34]!r}", ranker.is_noise(t), False)

print("\n-- URL canonicalisation --")
check("strips utm + www + scheme",
      ranker.canonical_url("https://www.Example.com/a/?utm_source=x&utm_medium=y"), "example.com/a")
check("keeps meaningful query",
      ranker.canonical_url("https://example.com/p?id=42&utm_campaign=z"), "example.com/p?id=42")
check("strips fragment and trailing slash",
      ranker.canonical_url("http://example.com/post/#section"), "example.com/post")
check("collapses amp suffix", ranker.canonical_url("https://example.com/story/amp/"), "example.com/story")

print("\n-- title normalisation catches reworded duplicates --")
a = ranker.normalise_title("OpenAI Confirms the 'Wiki Incident'")
b = ranker.normalise_title("OpenAI confirms wiki incident")
check("reworded headlines collapse", a, b)
check("different stories do not collapse",
      ranker.normalise_title("Postgres 18 released") == ranker.normalise_title("Redis 8 released"), False)

print("\n-- dedupe, per-source cap, ordering --")
pool = [
    art("Actively exploited RCE in Chromium", "HN", 1, "cve exploit rce"),
    art("Actively exploited RCE in Chromium!", "Verge", 2, "cve"),          # dupe title
    art("Same link different title", "HN", 3, url="https://ex.com/x?utm_source=a"),
    art("Another headline entirely", "Verge", 3, url="https://www.ex.com/x/"),  # dupe url
    art("Kubernetes 1.35 ships", "HN", 4, "kubernetes"),
    art("Docker adds a feature", "HN", 5, "docker"),
    art("Terraform provider update", "HN", 6, "terraform"),                 # 4th from HN
    art("Top 10 gadgets", "HN", 1),                                          # noise
]
ranked, st = ranker.rank(pool, {"HN": 3.0, "Verge": 2.0}, per_source_cap=3, now=NOW)
check("noise dropped", st["noise"], 1)
check("url duplicate dropped", st["dupe_url"], 1)
check("title duplicate dropped", st["dupe_title"], 1)
check("per-source cap enforced", sum(1 for a in ranked if a["source"] == "HN") <= 3, True)
check("something was capped", st["capped"] >= 1, True)
check("highest score first", ranked[0]["title"], "Actively exploited RCE in Chromium")
check("scores descend", all(ranked[i]["_score"] >= ranked[i + 1]["_score"] for i in range(len(ranked) - 1)), True)

print("\n-- stub filter --")
_, st2 = ranker.rank([art("Too short", "HN", 1)], {"HN": 1.0}, now=NOW)
check("two-word title rejected as stub", st2["stub"], 1)

print("\n-- source weight matters, all else equal --")
r, _ = ranker.rank([art("Kubernetes ships a thing", "Weak", 1, "kubernetes"),
                    art("Kubernetes ships something", "Strong", 1, "kubernetes")],
                   {"Weak": 1.0, "Strong": 5.0}, now=NOW)
check("heavier source ranks first", r[0]["source"], "Strong")

print()
if FAILURES:
    print(f"FAILED: {len(FAILURES)} test(s) -> {FAILURES}")
    sys.exit(1)
print("All ranker tests passed.")
