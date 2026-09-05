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
check("exploit matches 'exploited' (verb form)",
      "exploit" in ranker.classify("Actively exploited flaw", "")[1], True)
check("short terms are boundary-guarded: aws",
      "aws" in ranker.classify("AWS, us-east-1 down", "")[1], True)
check("aws does not match inside a word",
      "aws" in ranker.classify("He guffaws at the outage", "")[1], False)
check("gcp matches at start of title",
      "gcp" in ranker.classify("GCP raises egress prices", "")[1], True)

print("\n-- title-first classification (the LWN trap) --")
digest = ("Security updates for Thursday",
          "Updates for kubernetes, docker, postgres, python and the linux kernel.")
score, tags = ranker.classify(*digest)
check("body-only terms give the topic bonus only", round(score, 4), 1.15)
check("body-only terms still become tags", len(tags) >= 4, True)
real = ranker.classify("Kubernetes 1.35 ships", "")
check("one title hit -> 1 + 0.5 + 0.15", round(real[0], 4), 1.65)
check("two title hits -> 1 + 1.0 + 0.15", round(ranker.classify("docker and kubernetes", "")[0], 4), 2.15)
check("no topics at all -> neutral 1.0", round(ranker.classify("a rooster clock", "")[0], 4), 1.0)
check("title outscores an identically-worded body",
      ranker.classify("kubernetes docker", "")[0] > ranker.classify("nothing here", "kubernetes docker")[0], True)
t2 = ranker.classify("Docker ships a feature", "this also mentions kubernetes")
check("title tag comes first", t2[1][0], "docker")
check("body adds only tags the title lacked", "kubernetes" in t2[1], True)

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

print("\n-- relevance MULTIPLIES, so it competes with source weight --")
r, _ = ranker.rank(
    [art("Postgres 18 adds asynchronous IO", "Light", 3, "postgres"),
     art("A rooster alarm clock app", "Heavy", 1, "it crows")],
    {"Light": 0.90, "Heavy": 0.95}, now=NOW)
check("relevant light source beats irrelevant heavier one", r[0]["source"], "Light")

print("\n-- source weight is clamped to the band --")
check("3.0 clamps to max", ranker.clamp_weight(3.0), ranker.SOURCE_WEIGHT_MAX)
check("0.1 clamps to min", ranker.clamp_weight(0.1), ranker.SOURCE_WEIGHT_MIN)
check("1.0 passes through", ranker.clamp_weight(1.0), 1.0)

print("\n-- ported NOISE list, verbatim patterns --")
for t in ["Security updates for Thursday", "[$] A subscriber-only article",
          "Weekly Edition for September 5", "Kernel prepatch 6.19-rc4",
          "Stable kernel 6.18.2", "Friday Five: what shipped",
          "This week in Rust #601", "Week in review: containers"]:
    check_true(f"ported noise: {t[:32]!r}", ranker.is_noise(t, extra=False))
check("ported list alone does not drop a listicle",
      ranker.is_noise("Top 10 laptops for 2026", extra=False), False)
check("extra list does drop it", ranker.is_noise("Top 10 laptops for 2026", extra=True), True)

print("\n-- dedupe registers keys even for rejected items --")
pool2 = [
    art("Chromium RCE exploited", "A", 1, url="https://ex.com/rce"),
    art("Chromium RCE exploited!", "B", 2, url="https://other.com/rce-bug"),   # title dupe
    art("Totally different words here", "C", 3, url="https://www.ex.com/rce/?utm_source=n"),
]
_, st3 = ranker.rank(pool2, {"A": 1.0, "B": 1.0, "C": 1.0}, now=NOW)
check("title dupe caught", st3["dupe_title"], 1)
check("url dupe caught even though its twin was itself rejected", st3["dupe_url"], 1)

print("\n-- source weight matters, all else equal --")
r, _ = ranker.rank([art("Kubernetes ships a thing", "Weak", 1, "kubernetes"),
                    art("Kubernetes ships something else", "Strong", 1, "kubernetes")],
                   {"Weak": 0.85, "Strong": 1.30}, now=NOW)
check("heavier source ranks first", r[0]["source"], "Strong")

print()
if FAILURES:
    print(f"FAILED: {len(FAILURES)} test(s) -> {FAILURES}")
    sys.exit(1)
print("All ranker tests passed.")
