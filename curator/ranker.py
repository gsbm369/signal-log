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

# Relevance is a MULTIPLIER, not an addend, and starts at a neutral 1.0:
#
#     score     = recency * source_weight * relevance
#     relevance = 1 + focus_hits * FOCUS_HIT_BONUS + (TOPIC_BONUS if topics else 0)
#
# This is structural, and it is what keeps source weight from becoming the
# ranking. Under an additive lift, a weight-2.0 source with zero relevance beat
# a weight-1.0 source with two focus hits. As a multiplier they compete in the
# same unit: 2.00 x 1.00 = 2.00 loses to 1.00 x 2.15 = 2.15.
FOCUS_HIT_BONUS = 0.5         # each TITLE focus hit
TOPIC_BONUS = 0.15            # flat bonus if the item has any topic at all

PER_SOURCE_CAP = 3            # max articles from any one feed in the final list
MIN_TITLE_WORDS = 3           # anything shorter is a stub, not a story

# Source weight breaks ties between comparably relevant stories. It must not be
# able to lift an irrelevant one to the top, so the band is deliberately narrow
# (+/-25%). A 2.0-vs-1.0 spread makes the source the ranking.
SOURCE_WEIGHT_MIN = 0.85
SOURCE_WEIGHT_MAX = 1.30
DEFAULT_SOURCE_WEIGHT = 1.00

# Topics the blog actually cares about. A hit boosts; a miss is not a penalty.
FOCUS_STACK: tuple[str, ...] = (
    # infrastructure / ops
    "docker", "kubernetes", "k8s", "ansible", "terraform", "proxmox", "nginx",
    "self-hosted", "selfhosted", "homelab", "observability", "grafana",
    "prometheus", "loki", "systemd", "linux", "kernel", "ebpf", "networking",
    # Short, collision-prone terms. The original guarded these with literal
    # surrounding spaces (' iac ', ' aws ', ' gcp '), which silently misses a
    # title that STARTS with the term and any trailing punctuation — "AWS,"
    # and "AWS outage" both fail that test. Word boundaries handle both.
    "iac", "aws", "gcp", "azure", "cloudflare",
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
# Terms whose inflections matter. Strict \b...\b would make "exploit" miss
# "actively exploited", which is exactly the headline shape that should score
# highest. Caught by the golden test, not by any filter test.
PREFIX_TERMS: frozenset[str] = frozenset({
    "fine-tun", "vulnerab", "embedding", "exploit", "breach", "benchmark",
    "inference", "transformer",
})


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


# --------------------------------------------------------------------------- #
# Noise
# --------------------------------------------------------------------------- #

# VERBATIM from netlify/functions/news/feeds.mjs. Routine daily posts that rank
# high on recency and say nothing. Do not edit without editing the original.
NOISE_PATTERNS_ORIGINAL: tuple[re.Pattern[str], ...] = (
    re.compile(r"^security updates for ", re.I),
    re.compile(r"^\[\$\]"),                                       # LWN subscriber-only teasers
    re.compile(r"^(weekly edition|kernel prepatch|stable kernel)", re.I),
    re.compile(r"^friday five", re.I),
    re.compile(r"^(this week|week) in ", re.I),
)

# Additional patterns for THIS project's feeds. The original polls LWN, Phoronix
# and vendor blogs; this one polls Hacker News and TechCrunch, which produce a
# different kind of routine post — listicles, deals, and discussion threads —
# that the original never needed to filter. Kept separate so the ported list
# above stays verbatim and auditable.
#
# Disable with `extra_noise_filter: false` in feeds.yml.
NOISE_PATTERNS_EXTRA: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.I)
    for p in (
        r"^\s*(daily|weekly|monthly)\s+(digest|roundup|round-up|recap|briefing|newsletter)",
        r"\b(what we know so far|everything you need to know|here'?s what)\b",
        r"\bbest\s+\d+\b|\btop\s+\d+\b|\b\d+\s+(best|things|ways|tips|tools|reasons)\b",
        r"\b(deals?|discount|coupon|sale|black friday|cyber monday|prime day)\b",
        r"\b(giveaway|sweepstake|sponsored|advertisement)\b",
        r"^\s*(ask|tell)\s+hn\s*:",
        r"\b(open thread|weekly thread|who is hiring|freelancer\?)\b",
        r"\b(live ?blog|liveblog|as it happened)\b",
        r"\b(horoscope|recipe|wordle|crossword)\b",
    )
)

NOISE_PATTERNS: tuple[re.Pattern[str], ...] = NOISE_PATTERNS_ORIGINAL + NOISE_PATTERNS_EXTRA

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


def is_noise(title: str, extra: bool = True) -> bool:
    patterns = NOISE_PATTERNS if extra else NOISE_PATTERNS_ORIGINAL
    return any(p.search(title or "") for p in patterns)


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #


def recency_factor(published: datetime, now: datetime | None = None) -> float:
    """Exponential decay: 1.0 when fresh, 0.5 at HALF_LIFE_HOURS."""
    now = now or datetime.now(timezone.utc)
    age_h = max(0.0, (now - published).total_seconds() / 3600.0)
    return math.pow(2.0, -age_h / HALF_LIFE_HOURS)


def classify(title: str, summary: str) -> tuple[float, list[str]]:
    """Title-first classification, matching the original's classify().

    The score (focusHits) is counted from the TITLE ALONE. The body may add tags
    the title did not already produce, but it cannot lift the score.

    This asymmetry is load-bearing, not an oversight. Scoring combined text was
    the original's first-version bug: LWN package-list digests match five topics
    from their body and took the top slot on relevance alone, despite the
    headline saying nothing. A body that mentions Kubernetes is not a story
    about Kubernetes; a headline that does, is.
    """
    t, b = title or "", summary or ""
    title_tags: list[str] = []
    body_tags: list[str] = []

    for term, pat in FOCUS_PATTERNS:
        if pat.search(t):
            title_tags.append(term)
        elif pat.search(b):
            body_tags.append(term)      # tag only — contributes no focus hit

    topics = title_tags + body_tags
    relevance = 1.0 + len(title_tags) * FOCUS_HIT_BONUS + (TOPIC_BONUS if topics else 0.0)
    return relevance, topics


# Kept as an alias so existing callers and tests read naturally.
relevance_hits = classify


def score_article(art: dict[str, Any], source_weight: float, now: datetime) -> dict[str, Any]:
    recency = recency_factor(art["published"], now)
    relevance, topics = classify(art["title"], art.get("summary", ""))
    weight = clamp_weight(source_weight)
    score = recency * weight * relevance
    art = dict(art)
    art["_score"] = round(score, 5)
    art["_recency"] = round(recency, 4)
    art["_relevance"] = round(relevance, 3)
    art["_weight"] = round(weight, 3)
    art["_matched"] = topics[:6]
    return art


def clamp_weight(w: float) -> float:
    """Keep source weight inside the narrow band. A feeds.yml typo of 3.0 would
    otherwise silently turn source into the whole ranking."""
    return max(SOURCE_WEIGHT_MIN, min(SOURCE_WEIGHT_MAX, float(w)))


# --------------------------------------------------------------------------- #
# Pipeline
# --------------------------------------------------------------------------- #


def rank(
    articles: Iterable[dict[str, Any]],
    source_weights: dict[str, float] | None = None,
    limit: int | None = None,
    per_source_cap: int = PER_SOURCE_CAP,
    now: datetime | None = None,
    extra_noise: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Rank and thin a candidate pool. Returns (ranked, stats)."""
    now = now or datetime.now(timezone.utc)
    weights = source_weights or {}
    stats = {"in": 0, "noise": 0, "stub": 0, "dupe_url": 0, "dupe_title": 0, "capped": 0}

    scored: list[dict[str, Any]] = []
    for art in articles:
        stats["in"] += 1
        title = art.get("title", "")
        if is_noise(title, extra=extra_noise):
            stats["noise"] += 1
            continue
        if len(title.split()) < MIN_TITLE_WORDS:
            stats["stub"] += 1
            continue
        scored.append(score_article(
            art, float(weights.get(art.get("source", ""), DEFAULT_SOURCE_WEIGHT)), now))

    # Highest score first, so the survivor of a duplicate pair is the best one.
    scored.sort(key=lambda a: a["_score"], reverse=True)

    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for art in scored:
        cu = canonical_url(art.get("url", ""))
        nt = normalise_title(art.get("title", ""))
        dropped = False

        if cu and cu in seen_urls:
            stats["dupe_url"] += 1
            dropped = True
        elif nt and nt in seen_titles:
            stats["dupe_title"] += 1
            dropped = True

        # Register BOTH keys even when dropping. A rejected duplicate still
        # claims its identity: without this, an article discarded as a title
        # duplicate never registers its URL, so a third article sharing that
        # URL sails through. Surfaced by the golden test reporting dupe_url=0
        # where the fixture plainly contained a URL twin.
        seen_urls.add(cu)
        seen_titles.add(nt)

        if not dropped:
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
