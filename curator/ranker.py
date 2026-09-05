#!/usr/bin/env python3
"""
Deterministic article ranking. No model, no API call, no cost.

A port of the heuristic from netlify/functions/news/feeds.mjs — the logic, not
the language. Every stage the original performs is here:

  1. noise filter        drop routine digest/roundup posts outright
  2. recency decay       exponential, 36h half-life
  3. source weighting    per-feed multiplier from feeds.yml
  4. relevance boost     focus-stack keyword hits, title weighted over summary
  5. cross-source dedupe normalised title + canonical URL
  6. per-source cap      one prolific blog cannot dominate the front page

The constants below are the tunable surface. They were reconstructed from the
description of feeds.mjs rather than copied from it, so they are the most likely
place for the two implementations to diverge — check these first if the ordering
does not match the original.
"""

from __future__ import annotations

import math
import re
import unicodedata
from datetime import datetime, timezone
from typing import Any, Iterable

# --------------------------------------------------------------------------- #
# Tunables — align these with feeds.mjs
# --------------------------------------------------------------------------- #

HALF_LIFE_HOURS = 36.0        # score halves every 36 hours
TITLE_HIT_WEIGHT = 2.0        # a focus-stack term in the title counts double
SUMMARY_HIT_WEIGHT = 1.0
RELEVANCE_CAP = 6.0           # stop rewarding keyword stuffing past this
RELEVANCE_SCALE = 0.18        # how much each capped hit lifts the score
PER_SOURCE_CAP = 3            # max articles from any one feed in the final list
MIN_TITLE_WORDS = 3           # anything shorter is a stub, not a story

# Topics the blog actually cares about. A hit boosts; a miss is not a penalty.
FOCUS_STACK: tuple[str, ...] = (
    # infrastructure / ops
    "docker", "kubernetes", "k8s", "ansible", "terraform", "proxmox", "nginx",
    "self-hosted", "selfhosted", "homelab", "observability", "grafana",
    "prometheus", "loki", "systemd", "linux", "kernel", "ebpf", "networking",
    # data
    "postgres", "postgresql", "sqlite", "redis", "clickhouse", "duckdb",
    # languages / runtime  ("go" alone is too ambiguous in prose — golang only)
    "python", "rust", "golang", "typescript", "wasm", "webassembly",
    # AI
    "llm", "claude", "anthropic", "openai", "gpt", "gemini", "mistral",
    "inference", "transformer", "fine-tun", "rag", "embedding", "ollama",
    "open-weight", "open weights", "benchmark",
    # security
    "cve", "vulnerab", "exploit", "zero-day", "0-day", "ransomware",
    "supply chain", "rce", "privilege escalation", "breach",
    # hardware that matters to the above
    "gpu", "nvidia", "amd", "arm", "risc-v", "tpu", "datacenter", "data center",
)

# Terms matched as a prefix, so "fine-tun" also catches "fine-tuning"/"fine-tuned".
PREFIX_TERMS: frozenset[str] = frozenset({"fine-tun", "vulnerab", "embedding"})


def _compile_focus(terms: Iterable[str]) -> tuple[tuple[str, re.Pattern[str]], ...]:
    """Word-boundary patterns.

    Naive substring matching is wrong here and was caught in testing: bare "arm"
    matched al*arm*, w*arm*ing and fr*am*e, handing a relevance boost (and an
    "arm" tag) to a rooster alarm-clock app and a climate story.
    """
    out = []
    for t in terms:
        esc = re.escape(t.strip())
        tail = r"\w*" if t in PREFIX_TERMS else (r"\b" if t[-1].isalnum() else "")
        out.append((t.strip(), re.compile(rf"\b{esc}{tail}", re.I)))
    return tuple(out)


FOCUS_PATTERNS = _compile_focus(FOCUS_STACK)


# Routine digest / roundup / listicle posts. Matched against the title.
NOISE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.I)
    for p in (
        r"^\s*(daily|weekly|monthly)\s+(digest|roundup|round-up|recap|briefing|newsletter)",
        r"\b(what we know so far|everything you need to know|here'?s what)\b",
        r"\bbest\s+\d+\b|\btop\s+\d+\b|\b\d+\s+(best|things|ways|tips|tools|reasons)\b",
        r"\b(deals?|discount|coupon|sale|black friday|cyber monday|prime day)\b",
        r"\b(giveaway|sweepstake|sponsored|advertisement)\b",
        r"^\s*(ask|tell)\s+hn\s*:",           # discussion threads, not news
        r"\b(open thread|weekly thread|who is hiring|freelancer\?)\b",
        r"\b(live ?blog|liveblog|as it happened)\b",
        r"\b(horoscope|recipe|wordle|crossword)\b",
    )
)

# Query/tracking params stripped when canonicalising a URL.
TRACKING_PARAMS = re.compile(
    r"(?:^|&)(utm_[^=&]*|ref|ref_src|source|src|fbclid|gclid|mc_cid|mc_eid|"
    r"cmpid|ncid|sh|at_medium|at_campaign|__twitter_impression|guccounter)=[^&]*",
    re.I,
)

_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "to", "of", "in", "on",
    "for", "and", "or", "with", "at", "by", "from", "as", "it", "its", "that",
    "this", "new", "now", "how", "why", "what", "says", "said",
}


# --------------------------------------------------------------------------- #
# Normalisation
# --------------------------------------------------------------------------- #


def canonical_url(url: str) -> str:
    """Strip tracking params, AMP suffixes, www and trailing slashes."""
    u = (url or "").strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = re.sub(r"#.*$", "", u)
    if "?" in u:
        head, _, query = u.partition("?")
        query = TRACKING_PARAMS.sub("", query).lstrip("&")
        u = f"{head}?{query}" if query else head
    u = re.sub(r"/(amp|amp\.html)/?$", "/", u)
    return u.rstrip("/")


def normalise_title(title: str) -> str:
    """Reduce a headline to a comparable key, so two outlets covering the same
    story with slightly different wording collapse together."""
    t = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    t = t.lower()
    t = re.sub(r"[‘’“”']", "", t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    words = [w for w in t.split() if w not in _STOPWORDS and len(w) > 2]
    return " ".join(sorted(words[:12]))


def is_noise(title: str) -> bool:
    return any(p.search(title or "") for p in NOISE_PATTERNS)


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #


def recency_factor(published: datetime, now: datetime | None = None) -> float:
    """Exponential decay: 1.0 when fresh, 0.5 at HALF_LIFE_HOURS."""
    now = now or datetime.now(timezone.utc)
    age_h = max(0.0, (now - published).total_seconds() / 3600.0)
    return math.pow(2.0, -age_h / HALF_LIFE_HOURS)


def relevance_hits(title: str, summary: str) -> tuple[float, list[str]]:
    """Weighted focus-stack hits. Title matches count for more than body ones."""
    t, s = title or "", summary or ""
    score, matched = 0.0, []
    for term, pat in FOCUS_PATTERNS:
        in_t, in_s = bool(pat.search(t)), bool(pat.search(s))
        if in_t or in_s:
            score += TITLE_HIT_WEIGHT if in_t else SUMMARY_HIT_WEIGHT
            matched.append(term)
    return min(score, RELEVANCE_CAP), matched


def score_article(art: dict[str, Any], source_weight: float, now: datetime) -> dict[str, Any]:
    recency = recency_factor(art["published"], now)
    rel, matched = relevance_hits(art["title"], art.get("summary", ""))
    # Source weight and recency are multiplicative — a weak source with a fresh
    # story should not outrank a strong source's fresh story. Relevance is an
    # additive lift so a niche-but-relevant piece can still surface.
    score = (source_weight * recency) * (1.0 + rel * RELEVANCE_SCALE)
    art = dict(art)
    art["_score"] = round(score, 5)
    art["_recency"] = round(recency, 4)
    art["_relevance"] = round(rel, 2)
    art["_matched"] = matched[:6]
    return art


# --------------------------------------------------------------------------- #
# Pipeline
# --------------------------------------------------------------------------- #


def rank(
    articles: Iterable[dict[str, Any]],
    source_weights: dict[str, float] | None = None,
    limit: int | None = None,
    per_source_cap: int = PER_SOURCE_CAP,
    now: datetime | None = None,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Rank and thin a candidate pool. Returns (ranked, stats)."""
    now = now or datetime.now(timezone.utc)
    weights = source_weights or {}
    stats = {"in": 0, "noise": 0, "stub": 0, "dupe_url": 0, "dupe_title": 0, "capped": 0}

    scored: list[dict[str, Any]] = []
    for art in articles:
        stats["in"] += 1
        title = art.get("title", "")
        if is_noise(title):
            stats["noise"] += 1
            continue
        if len(title.split()) < MIN_TITLE_WORDS:
            stats["stub"] += 1
            continue
        scored.append(score_article(art, float(weights.get(art.get("source", ""), 1.0)), now))

    # Highest score first, so the survivor of a duplicate pair is the best one.
    scored.sort(key=lambda a: a["_score"], reverse=True)

    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for art in scored:
        cu = canonical_url(art.get("url", ""))
        nt = normalise_title(art.get("title", ""))
        if cu and cu in seen_urls:
            stats["dupe_url"] += 1
            continue
        if nt and nt in seen_titles:
            stats["dupe_title"] += 1
            continue
        seen_urls.add(cu)
        seen_titles.add(nt)
        deduped.append(art)

    # Per-source cap, applied in score order so each source keeps its best.
    per_source: dict[str, int] = {}
    capped: list[dict[str, Any]] = []
    for art in deduped:
        src = art.get("source", "")
        if per_source.get(src, 0) >= per_source_cap:
            stats["capped"] += 1
            continue
        per_source[src] = per_source.get(src, 0) + 1
        capped.append(art)

    stats["out"] = len(capped if limit is None else capped[:limit])
    return (capped if limit is None else capped[:limit]), stats
