#!/usr/bin/env python3
"""
signal.log curator
==================

Pulls RSS from the tech feeds, ranks it deterministically, and writes the top
stories into the Astro content directory as Markdown.

Two stages, deliberately separated:

  1. SELECTION  — ranker.py. Pure heuristic: recency decay, source weighting,
                  relevance, dedupe, per-source cap. No model in any mode.
  2. SUMMARY    — summarizers.py. Pluggable: none | ollama | anthropic.

The default backend is `none`, which uses each feed's own description. That means
the pipeline runs end to end with no API key and no spend.

Run:  python curate.py [--dry-run] [--count N] [--backend none|ollama|anthropic]
Env:  CONTENT_DIR, STATE_DIR, FEEDS_FILE, SUMMARIZER_BACKEND, ANTHROPIC_API_KEY
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import socket
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import feedparser
import yaml

import images
import ranker
import summarizers

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

FEEDS_FILE = Path(os.environ.get("FEEDS_FILE", HERE / "feeds.yml"))
CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", HERE.parent / "site/src/content/posts"))
STATE_DIR = Path(os.environ.get("STATE_DIR", HERE / "state"))
SEEN_FILE = STATE_DIR / "seen.json"

# Fallback retention for a category that declares none, and the expiry applied
# to LEGACY seen.json entries (the old flat {key: date} shape carried no
# category, so there is nothing to look a policy up by).
# THE ONLY UNBOUNDED NETWORK CALL IN THIS FILE, until now.
#
# feedparser.parse() takes no timeout argument and inherits the socket default,
# which is None — wait for ever. images.py, loki.py and summarizers.py all bound
# their calls; this one did not, and it is the one that talks to 28 third-party
# servers every cycle.
#
# A feed whose server completes the TCP handshake and then never sends a byte
# hangs its worker permanently. pool.map() waits for every worker, so the
# curator never returns, the builder container never exits, `docker compose run`
# never returns, and the cycle sits there until systemd's TimeoutStartSec fires
# 30 minutes later. Nothing alerts in the meantime, because from every monitor's
# point of view the job is still running. A hang must become a failure, because
# a failure is a thing that alerts.
#
# Set globally rather than per-call because feedparser offers no other hook. It
# is a single-purpose script, and every other network user here already passes
# an explicit timeout, so nothing else is affected by the default changing.
FEED_SOCKET_TIMEOUT = float(os.environ.get("FEED_SOCKET_TIMEOUT", "20"))
socket.setdefaulttimeout(FEED_SOCKET_TIMEOUT)

SEEN_RETENTION_DAYS = 45

# Clock skew allowance before an item counts as future-dated. Two hours is
# generous for a publisher whose server clock drifts; it is nowhere near the
# 4.8-to-55.8 days measured on Finextra's scheduled-webinar entries.
FUTURE_DATE_GRACE = timedelta(hours=2)

# Ingest-gate rejections, counted per source and per category per reason.
# A gate nobody can see refusing is a gate nobody can trust: these are logged
# at the end of collect() and shipped to Loki with the rest of the metrics.
REJECTS: dict[str, dict[str, int]] = {
    "too_old": {}, "no_date": {}, "future_date": {},
}
REJECTS_BY_CAT: dict[str, dict[str, int]] = {
    "too_old": {}, "no_date": {}, "future_date": {},
}
# A handful of raw date strings per source, kept for the acceptance report.
# Bounded: a broken feed must not turn the metric line into a log dump.
REJECT_SAMPLES: dict[str, list[str]] = {}


def _reject(reason: str, source: str, category: str, raw_date: str = "") -> None:
    REJECTS[reason][source] = REJECTS[reason].get(source, 0) + 1
    REJECTS_BY_CAT[reason][category] = REJECTS_BY_CAT[reason].get(category, 0) + 1
    if raw_date:
        bucket = REJECT_SAMPLES.setdefault(f"{reason}:{source}", [])
        if len(bucket) < 3:
            bucket.append(raw_date[:64])

log = logging.getLogger("curator")

# Written to $STATE_DIR/metrics.json every run — run-cycle.sh ships this to Loki.
METRICS: dict[str, Any] = {
    "articles_fetched": 0,
    "articles_new": 0,
    "articles_ranked": 0,
    "articles_kept": 0,
    "feeds_ok": 0,
    "feeds_failed": 0,
    "dropped_noise": 0,
    "dropped_dupe": 0,
    "dropped_capped": 0,
    "backend": "",
    "model": "",
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_read_tokens": 0,
    "cost_usd": 0.0,
    "curator_status": "not_run",
    "error": None,
    "duration_s": 0.0,
}


def write_metrics() -> None:
    """Persist run metrics where the cycle script can find them. Never raises."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        (STATE_DIR / "metrics.json").write_text(json.dumps(METRICS, indent=2))
    except OSError as exc:
        log.warning("could not write metrics.json: %s", exc)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:max_len].strip("-") or "untitled"


def url_key(url: str) -> str:
    """Stable identity for an article, reusing the ranker's canonicalisation."""
    return hashlib.sha256(ranker.canonical_url(url).encode()).hexdigest()[:20]


def strip_html(raw: str, limit: int = 600) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = re.sub(r"&[a-z]+;|&#\d+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def entry_raw_date(entry: Any) -> str:
    """The date string as the feed wrote it, for diagnosing a rejection."""
    for field in ("published", "updated", "created"):
        v = getattr(entry, field, None)
        if v:
            return str(v)
    return ""


def entry_datetime(entry: Any, now: datetime | None = None) -> tuple[datetime | None, str]:
    """Parse an entry's date. Returns (datetime, "") or (None, reason).

    DATE VALIDITY GUARD. This used to fall back to `now` for an entry with no
    parseable date, which is the worst possible default: an undated item is
    handed age 0 and therefore the maximum recency factor, so the items we know
    least about outrank the ones we know most about. An item we cannot date is
    now rejected outright.

    The same reasoning rules out fetched_at as a fallback for a bad date —
    fetched_at is approximately `now`, which is the identical bug wearing a
    different name.

    Future dates are rejected for the same reason from the other direction:
    ranker.recency_factor clamps age at 0, so an item dated next month scores a
    perfect 1.0 every run until the date arrives.

    This is a DATE-VALIDITY guard, not a content filter. It currently also
    removes Finextra's webinar promos, but only as a side effect of that
    publisher dating them at air time. Do not lean on it to keep event listings
    out of the newsletter — a publisher who dates the same promos in the past
    would sail straight through. Content filtering belongs in ranker's noise
    patterns.
    """
    now = now or datetime.now(timezone.utc)
    for field in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, field, None)
        if parsed:
            try:
                dt = datetime(*parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                continue
            if dt > now + FUTURE_DATE_GRACE:
                return None, "future_date"
            return dt, ""
    return None, "no_date"


def yaml_str(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


# --------------------------------------------------------------------------- #
# State
# --------------------------------------------------------------------------- #


def load_seen() -> dict[str, dict[str, Any]]:
    """Read seen.json, upgrading the legacy flat shape in memory.

    v1 was {key: "iso-date"}. v2 is {key: {"date": ..., "category": ...}},
    because retention is now a per-category decision and a bare date cannot be
    looked up against a policy. Legacy entries keep a null category and are
    pruned at SEEN_RETENTION_DAYS, exactly as they are today.
    """
    if not SEEN_FILE.exists():
        return {}
    try:
        data = json.loads(SEEN_FILE.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("could not read state file (%s) — starting fresh", exc)
        return {}
    if not isinstance(data, dict):
        return {}

    out: dict[str, dict[str, Any]] = {}
    legacy = 0
    for key, val in data.items():
        if isinstance(val, dict):
            out[key] = {"date": str(val.get("date", "")), "category": val.get("category")}
        else:
            out[key] = {"date": str(val), "category": None}
            legacy += 1
    if legacy:
        log.info("seen.json: %d legacy entry(ies) without a category", legacy)
    return out


def save_seen(seen: dict[str, dict[str, Any]], policies: dict[str, dict[str, Any]]) -> None:
    """Prune per category, then write atomically.

    `retention_days: null` means KEEP FOREVER, and it is the point of the
    evergreen categories. 45 days is a memory bound for news — it stops us
    re-publishing today's story next month. Applied to deep_dives it becomes an
    editorial instruction to re-run Brendan Gregg's best post every six weeks,
    which is precisely the repetition the seen-store exists to prevent.
    """
    now = datetime.now(timezone.utc)
    kept: dict[str, dict[str, Any]] = {}
    dropped_by_cat: dict[str, int] = {}
    for key, rec in seen.items():
        cat = rec.get("category")
        if cat is None:
            days: float | None = SEEN_RETENTION_DAYS
        else:
            days = policy_for(policies, str(cat)).get("retention_days", SEEN_RETENTION_DAYS)
        if days is None:                       # forever
            kept[key] = rec
            continue
        cutoff = (now - timedelta(days=float(days))).isoformat()
        if rec.get("date", "") >= cutoff:
            kept[key] = rec
        else:
            label = str(cat) if cat else "legacy"
            dropped_by_cat[label] = dropped_by_cat.get(label, 0) + 1

    if dropped_by_cat:
        log.info("seen.json: expired %s", dict(sorted(dropped_by_cat.items())))
    METRICS["seen_total"] = len(kept)
    METRICS["seen_expired"] = dict(sorted(dropped_by_cat.items()))

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SEEN_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(kept, indent=2, sort_keys=True))
    tmp.replace(SEEN_FILE)


# --------------------------------------------------------------------------- #
# Scoring policy
# --------------------------------------------------------------------------- #

# Fallbacks for a category with no `scoring.categories` entry. Deliberately
# news-shaped: an unconfigured category behaves the way the whole site did
# before the pivot, rather than silently inheriting an evergreen curve.
POLICY_DEFAULTS: dict[str, Any] = {
    "half_life_hours": ranker.DEFAULT_HALF_LIFE_HOURS,
    "ingest_days": 3.0,
    "retention_days": SEEN_RETENTION_DAYS,
    "cap": 6,
    "fetch": 15,
}


def resolve_policies(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Per-category policy from the `scoring:` block in feeds.yml.

    One config file, one template, one deploy path — the scoring block lives in
    feeds.yml next to the feeds it governs rather than in a second file that
    would need its own Jinja template and its own line in the playbook.
    """
    scoring = config.get("scoring") or {}
    declared = scoring.get("categories") or {}
    out: dict[str, dict[str, Any]] = {}
    for cat, raw in declared.items():
        pol = dict(POLICY_DEFAULTS)
        pol.update({k: v for k, v in (raw or {}).items() if v is not None or k == "retention_days"})
        # retention_days is the one key where an explicit null is MEANINGFUL:
        # it means keep forever, not "unset, use the default".
        if (raw or {}).get("retention_days", "missing") is None:
            pol["retention_days"] = None
        out[str(cat)] = pol
    return out


def policy_for(policies: dict[str, dict[str, Any]], category: str) -> dict[str, Any]:
    return policies.get(category, POLICY_DEFAULTS)


def feed_policy(feed: dict[str, Any], policies: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """A source's effective policy: its category's, with per-source overrides.

    Per-source `ingest_days` is not decoration, it is what makes per-source
    `half_life_hours` usable at all. Stripe sits in fintech (ingest 3d) but its
    newest post measured 21.8 days old — give it a deep-dives CURVE without also
    giving it a deep-dives WINDOW and it is still discarded at fetch time,
    before the curve is ever consulted.
    """
    pol = dict(policy_for(policies, str(feed.get("category", "uncategorised"))))
    for key in ("half_life_hours", "ingest_days", "fetch"):
        if feed.get(key) is not None:
            pol[key] = feed[key]
    return pol


# --------------------------------------------------------------------------- #
# Stage 1 — collect
# --------------------------------------------------------------------------- #


def fetch_feed(feed: dict[str, Any], policy: dict[str, Any]) -> list[dict[str, Any]]:
    name, url = feed["name"], feed["url"]
    category = str(feed.get("category", "uncategorised"))
    # `fetch` is how many entries to pull; `weight` is the ranking multiplier.
    # These were the same field, so compressing weights to the 0.85-1.30 band
    # would have silently cut every feed's contribution to ~7 entries.
    #
    # Depth is per SOURCE because the archives differ by two orders of
    # magnitude (measured 2026-09-10): Marc Brooker exposes 163 items and Dan
    # Luu 128, while Brendan Gregg, Netflix Tech and Stripe expose 10 each.
    # entries[:take] makes item 17 unreachable no matter how deep the feed is.
    take = max(4, int(policy.get("fetch", 15)))
    max_age = timedelta(days=float(policy["ingest_days"]))
    half_life = float(policy["half_life_hours"])
    try:
        parsed = feedparser.parse(
            url,
            agent="signal.log-curator/2.0 (+https://github.com/gsbm369)",
            request_headers={"Cache-Control": "no-cache"},
        )
    except Exception as exc:
        log.warning("[%s] fetch failed: %s", name, exc)
        METRICS["feeds_failed"] += 1
        return []

    if getattr(parsed, "bozo", 0) and not parsed.entries:
        log.warning("[%s] unreadable feed: %s", name, getattr(parsed, "bozo_exception", "?"))
        METRICS["feeds_failed"] += 1
        return []

    now = datetime.now(timezone.utc)
    out: list[dict[str, Any]] = []
    for entry in parsed.entries[:take]:
        link = getattr(entry, "link", "")
        title = strip_html(getattr(entry, "title", ""), 250)
        if not link or not title:
            continue
        published, reason = entry_datetime(entry, now)
        if reason:
            _reject(reason, name, category, entry_raw_date(entry))
            continue
        # INGEST WINDOW — "how far back do we bother parsing", nothing more.
        # This is not a freshness policy: editorial freshness is the decay curve
        # in the ranker, which can demote a stale item without deleting it. The
        # window exists so a ten-year archive does not have to be parsed every
        # four hours, and so an outage of a few days still catches up.
        if now - published > max_age:
            _reject("too_old", name, category, entry_raw_date(entry))
            continue
        # In-feed image only here — no network. The og:image fallback is a
        # network call per article, so it runs later for the handful of stories
        # that are actually selected, not for every candidate fetched.
        img, alt = images.extract(entry, link, allow_network=False)
        out.append({
            "source": name,
            "category": category,
            "_half_life_hours": half_life,
            "title": title,
            "url": link,
            "published": published,
            "summary": strip_html(
                getattr(entry, "summary", "") or getattr(entry, "description", ""), 900
            ),
            "image": img,
            "imageAlt": alt,
            "_entry": entry,
        })
    log.info("[%s] %d candidates", name, len(out))
    METRICS["feeds_ok"] += 1
    return out


def collect(
    feeds: list[dict[str, Any]], policies: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    with ThreadPoolExecutor(max_workers=min(8, len(feeds))) as pool:
        batches = pool.map(lambda f: fetch_feed(f, feed_policy(f, policies)), feeds)

    articles: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    for batch in batches:
        for art in batch:
            key = url_key(art["url"])
            if key in seen_urls:
                continue
            seen_urls.add(key)
            art["key"] = key
            articles.append(art)

    articles.sort(key=lambda a: a["published"], reverse=True)

    # Report what the ingest gate REFUSED. A counter nobody prints is a counter
    # nobody checks, and this gate is the one that silently emptied the
    # evergreen sources for the whole life of the news version.
    for reason in ("too_old", "no_date", "future_date"):
        by_src = REJECTS[reason]
        if not by_src:
            continue
        detail = ", ".join(f"{k}={v}" for k, v in sorted(by_src.items(), key=lambda kv: -kv[1]))
        log.info("ingest gate rejected %3d for %-11s | %s", sum(by_src.values()), reason, detail)
        for label, samples in sorted(REJECT_SAMPLES.items()):
            if label.startswith(f"{reason}:"):
                log.info("    %-28s e.g. %s", label.split(":", 1)[1], "; ".join(samples))

    METRICS["rejected_by_reason"] = {k: sum(v.values()) for k, v in REJECTS.items()}
    METRICS["rejected_by_source"] = {k: dict(sorted(v.items())) for k, v in REJECTS.items() if v}
    METRICS["rejected_by_category"] = {
        k: dict(sorted(v.items())) for k, v in REJECTS_BY_CAT.items() if v
    }
    return articles


# --------------------------------------------------------------------------- #
# Stage 3 — write Markdown
# --------------------------------------------------------------------------- #


def write_post(summary: summarizers.Summary) -> Path:
    src = summary.source_article
    published = src["published"]
    body = summary.body.strip()

    tags = [slugify(str(t), 24) for t in summary.tags][:4]
    read_minutes = max(1, round(len(body.split()) / 210))
    heat = max(0, min(100, int(summary.heat)))

    slug = f"{published.strftime('%Y-%m-%d')}-{slugify(summary.title)}"
    path = CONTENT_DIR / f"{slug}.md"

    front_lines = [
        "---",
        f"title: {yaml_str(summary.title)}",
        f"description: {yaml_str(summary.description)}",
        f"pubDate: {published.isoformat()}",
        # WHEN THIS SITE PUBLISHED IT, as distinct from when the author did.
        # prune_posts needs the first and every layout needs the second, and
        # conflating them deletes the newsletter's best content — see below.
        f"addedAt: {datetime.now(timezone.utc).isoformat()}",
        f"source: {yaml_str(src['source'])}",
        f"category: {src.get('category', 'uncategorised')}",
        f"sourceUrl: {yaml_str(src['url'])}",
        f"tags: [{', '.join(yaml_str(t) for t in tags)}]",
        f"heat: {heat}",
        f"score: {summary.score}",
        f"readMinutes: {read_minutes}",
    ]
    # Optional. Absent rather than empty when the story has no picture — the
    # schema marks these optional and the layout is built for their absence.
    if src.get("image"):
        front_lines.append(f"image: {yaml_str(src['image'])}")
        if src.get("imageAlt"):
            front_lines.append(f"imageAlt: {yaml_str(src['imageAlt'])}")
    front_lines.append("---")
    front = "\n".join(front_lines)

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{front}\n\n{body}\n", encoding="utf-8")
    return path


def _added_at(path: Path) -> str:
    """Prune key: when THIS SITE published the post.

    LEGACY ORDERING, stated explicitly because it covers most of the site today.
    A post written before `addedAt` existed has no such field, and is keyed
    "0" + filename. A post that has one is keyed "A" + the timestamp. So:

      * every legacy post sorts BEFORE every addedAt post, and is pruned first;
      * legacy posts sort among themselves by FILENAME, which begins with the
        article's own pubDate — the old behaviour, unchanged.

    That is a deliberate ordering, not a fallback that happens to work. Legacy
    posts are all from the news taxonomy, all dated within days of when they
    were published here, and all destined to age out; pruning them ahead of the
    newsletter's content is exactly what should happen.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            first = fh.readline()
            if first.startswith("---"):
                for _ in range(30):
                    line = fh.readline()
                    if not line or line.startswith("---"):
                        break
                    if line.startswith("addedAt:"):
                        return "A" + line.split(":", 1)[1].strip()
    except OSError:
        pass
    return "0" + path.name


def record_published(
    seen: dict[str, dict[str, Any]],
    ranked: list[dict[str, Any]],
    stories: list[Any],
    now: datetime | None = None,
) -> int:
    """Record ONLY what was published. Returns how many entries were added.

    This used to record every candidate the run considered, which is defensible
    while retention is 45 days and a feed exposes only this week's output: the
    entries expire long before the archive matters.

    It is catastrophic the moment a category remembers forever. Measured: one
    run took 85 deep_dives candidates, published the 6 the cap allowed, and
    marked all 85 seen permanently — Brendan Gregg's ten posts, jvns's twenty
    and Dan Luu's forty burned in a single cycle to publish six, unreachable
    ever after.

    It also contradicts the model the evergreen categories are built on: an item
    surfaces once, is recorded, and the NEXT run reaches for the next-best
    UNPUBLISHED item from that archive. A backlog can only be worked through if
    we remember what we published, not what we looked at.
    """
    stamped = (now or datetime.now(timezone.utc)).isoformat()
    published = {getattr(s, "source_article", {}).get("key") for s in stories}
    published.discard(None)
    added = 0
    for art in ranked:
        if art.get("key") in published and art["key"] not in seen:
            seen[art["key"]] = {"date": stamped, "category": art.get("category")}
            added += 1
    return added


def prune_posts(max_posts: int) -> int:
    """Keep the most recently PUBLISHED HERE posts, not the most recently written.

    This sorted by filename, and a filename begins with the article's own
    pubDate. For a news site those are the same thing to within a day. For this
    one they are not remotely the same: a Brendan Gregg post is dated 216 days
    ago and a Marc Brooker post 44, so under a filename sort the evergreen
    stories are ALWAYS the first deleted — the pruner ran straight over exactly
    the content the newsletter exists to surface.

    Measured: the 22:18 cycle published 6 deep_dives posts and the next run
    pruned all 6, while every legacy news post dated that week survived. The
    category had a 100% publish rate and a 0% survival rate, and nothing in the
    metrics said so, because publishing and pruning are counted separately.

    The "0"/"A" prefixes keep legacy filename keys sorting before every addedAt
    key, so posts that predate the field are pruned first — which is what we
    want while the news taxonomy ages out.
    """
    posts = sorted(CONTENT_DIR.glob("*.md"), key=_added_at)
    excess = len(posts) - max_posts
    if excess <= 0:
        return 0
    for path in posts[:excess]:
        path.unlink()
    return excess


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def _run() -> int:
    ap = argparse.ArgumentParser(description="Curate tech RSS into Markdown posts.")
    ap.add_argument("--dry-run", action="store_true", help="rank and summarise but write nothing")
    ap.add_argument("--count", type=int, help="override how many stories to publish")
    ap.add_argument("--backend", choices=sorted(summarizers.BACKENDS), help="override the summarizer backend")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s  %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    if not FEEDS_FILE.exists():
        log.error("feeds file not found: %s", FEEDS_FILE)
        METRICS["curator_status"] = "error"
        METRICS["error"] = f"feeds file not found: {FEEDS_FILE}"
        return 2

    config = yaml.safe_load(FEEDS_FILE.read_text()) or {}
    feeds = config.get("feeds") or []
    settings = config.get("settings") or {}
    if not feeds:
        log.error("no feeds configured in %s", FEEDS_FILE)
        METRICS["curator_status"] = "error"
        METRICS["error"] = "no feeds configured"
        return 2

    want = args.count or int(settings.get("publish_count", 5))
    max_candidates = int(settings.get("max_candidates", 40))
    max_posts = int(settings.get("max_posts", 60))
    per_source_cap = int(settings.get("per_source_cap", ranker.PER_SOURCE_CAP))
    policies = resolve_policies(config)
    if not policies:
        log.warning("no scoring.categories in %s — every category falls back to "
                    "the news-shaped defaults", FEEDS_FILE)
    for cat, pol in sorted(policies.items()):
        ret = "forever" if pol["retention_days"] is None else f"{pol['retention_days']}d"
        log.info("policy %-14s half-life %7.0fh | ingest %6.0fd | retention %-8s | cap %d",
                 cat, pol["half_life_hours"], pol["ingest_days"], ret, pol["cap"])

    backend_name = (
        args.backend
        or os.environ.get("SUMMARIZER_BACKEND")
        or settings.get("summarizer", "none")
    )

    try:
        backend = summarizers.build(
            backend_name,
            model=os.environ.get("CURATOR_MODEL", ""),
            url=os.environ.get("OLLAMA_URL", ""),
        )
    except ValueError as exc:
        log.error("%s", exc)
        METRICS["curator_status"] = "error"
        METRICS["error"] = str(exc)
        return 2

    METRICS["backend"] = backend.name
    ok, detail = backend.health()
    log.info("summarizer backend: %s — %s", backend.name, detail)
    if not ok:
        log.error("backend %s is not usable: %s", backend.name, detail)
        METRICS["curator_status"] = "backend_unavailable"
        METRICS["error"] = f"{backend.name}: {detail}"
        return 3

    started = time.monotonic()
    log.info("=== signal.log curator (backend=%s) ===", backend.name)

    # --- collect ---
    articles = collect(feeds, policies)
    METRICS["articles_fetched"] = len(articles)
    log.info("collected %d unique articles", len(articles))
    if not articles:
        log.warning("nothing collected — every feed was empty or unreachable")
        METRICS["curator_status"] = "no_articles"
        METRICS["error"] = "all feeds empty or unreachable"
        return 1

    # --- drop what we have already published ---
    seen = load_seen()
    fresh = [a for a in articles if a["key"] not in seen]
    METRICS["articles_new"] = len(fresh)
    log.info("%d new since the last run", len(fresh))
    if not fresh:
        log.info("no new articles; nothing to do")
        METRICS["curator_status"] = "no_new"
        return 0

    # --- rank (deterministic, no model), PER CATEGORY ---
    #
    # Categories are ranked separately rather than pooled and sliced. As one
    # pool, tech's volume crowds the shelves out entirely — a world story should
    # compete with world stories for its four slots, not with Hacker News.
    #
    # The category is DECLARED ON THE FEED and never inferred from the text. A
    # gaming site covering NVIDIA earnings is gaming; a markets site covering a
    # game studio is markets. Keyword classification gets both wrong.
    weights = {f["name"]: float(f.get("weight", ranker.DEFAULT_SOURCE_WEIGHT)) for f in feeds}
    caps = dict(settings.get("category_caps") or {})
    extra_noise = bool(settings.get("extra_noise_filter", True))

    by_cat: dict[str, list[dict[str, Any]]] = {}
    for art in fresh:
        by_cat.setdefault(art.get("category", "uncategorised"), []).append(art)

    # max_candidates is applied PER CATEGORY, after the split. Applied to the
    # pooled list it truncates by recency across all feeds: with 182 articles
    # collected, the newest 40 were world- and gaming-heavy and tech — the spine
    # of the site — published nothing at all.
    #
    # The cut is by SCORE, not by publication date. Sorting by date here
    # re-imposed recency after the split — the exact axis the per-category
    # half-life exists to remove — and it did so where nothing logs it: an
    # evergreen item could survive the ingest gate and the decay curve and still
    # be discarded by a truncation that never looked at its score.
    #
    # Applied to every category rather than only the evergreen ones. Under a
    # tight half-life the score ordering already IS the date ordering, so the
    # special case would buy a branch and no behaviour.
    now_dt = datetime.now(timezone.utc)
    cut_report: dict[str, dict[str, Any]] = {}
    for cat in by_cat:
        pol = policy_for(policies, cat)
        items = [
            ranker.score_article(
                a, float(weights.get(a.get("source", ""), ranker.DEFAULT_SOURCE_WEIGHT)),
                now_dt, float(pol["half_life_hours"]),
            )
            for a in by_cat[cat]
        ]
        items.sort(key=lambda a: a["_score"], reverse=True)
        by_date = sorted(by_cat[cat], key=lambda a: a["published"], reverse=True)
        cut_report[cat] = {
            "candidates": len(items),
            "by_score": [a["source"] for a in items[:max_candidates]],
            "by_date": [a["source"] for a in by_date[:max_candidates]],
        }
        by_cat[cat] = items[:max_candidates]
    METRICS["candidate_cut"] = {
        c: r["candidates"] for c, r in sorted(cut_report.items())
    }

    ranked: list[dict[str, Any]] = []
    rstats = {"in": 0, "noise": 0, "stub": 0, "dupe_url": 0, "dupe_title": 0, "capped": 0}
    per_cat: dict[str, int] = {}

    for cat in sorted(by_cat):
        pol = policy_for(policies, cat)
        # The old taxonomy had one spine category ("tech") that took
        # publish_count and three small shelves that took a fixed 4. Seven peer
        # categories have no spine, so the cap is a per-category policy value
        # and `caps`/publish_count remain only as a fallback for a category the
        # scoring block does not mention.
        limit = int(caps.get(cat, pol.get("cap", want)))
        picked, st = ranker.rank(
            by_cat[cat], weights, limit=limit,
            per_source_cap=per_source_cap, extra_noise=extra_noise,
            half_life_hours=float(pol["half_life_hours"]), now=now_dt,
        )
        ranked.extend(picked)
        per_cat[cat] = len(picked)
        for k in rstats:
            rstats[k] += st.get(k, 0)
        log.info("category %-8s %3d candidate(s) -> %d published (cap %d)",
                 cat, len(by_cat[cat]), len(picked), limit)

    METRICS["per_category"] = per_cat
    METRICS["articles_ranked"] = rstats["in"]
    METRICS["dropped_noise"] = rstats["noise"] + rstats["stub"]
    METRICS["dropped_dupe"] = rstats["dupe_url"] + rstats["dupe_title"]
    METRICS["dropped_capped"] = rstats["capped"]
    log.info(
        "ranked %d -> %d  (noise %d, stub %d, dupe %d, capped %d)",
        rstats["in"], len(ranked), rstats["noise"], rstats["stub"],
        rstats["dupe_url"] + rstats["dupe_title"], rstats["capped"],
    )
    if not ranked:
        log.warning("everything was filtered out this run")
        METRICS["curator_status"] = "nothing_selected"
        return 0

    for a in ranked:
        log.info("  [%-7s %.4f rel %.1f] %-20s %s",
                 a.get("category", "uncategorised"), a["_score"], a["_relevance"],
                 a["source"][:20], a["title"][:60])

    # --- resolve images for the selected stories only ---
    # Every candidate already carries an in-feed image if its feed shipped one.
    # This fills the gaps with an og:image fetch, capped to the published set so
    # a slow publisher costs seconds, not minutes. Failure is normal and silent:
    # the layout is designed for a story with no picture.
    need = [a for a in ranked if not a.get("image")]
    if need:
        log.info("resolving og:image for %d story(ies) without one", len(need))
        for art in need:
            img, alt = images.extract(art.get("_entry"), art.get("url", ""), allow_network=True)
            if img:
                art["image"], art["imageAlt"] = img, alt
    METRICS["with_image"] = sum(1 for a in ranked if a.get("image"))
    METRICS["without_image"] = len(ranked) - METRICS["with_image"]
    log.info("images: %d/%d story(ies) have one", METRICS["with_image"], len(ranked))

    # --- summarise ---
    stories = backend.summarize(ranked)
    METRICS["articles_kept"] = len(stories)
    METRICS["model"] = backend.usage.get("model", "")
    METRICS["input_tokens"] = backend.usage.get("input_tokens", 0)
    METRICS["output_tokens"] = backend.usage.get("output_tokens", 0)
    METRICS["cost_usd"] = backend.usage.get("cost_usd", 0.0)
    log.info("summarised %d story(ies) via %s — ~$%.4f",
             len(stories), backend.name, METRICS["cost_usd"])

    if args.dry_run:
        log.info("--dry-run: no files written")
        METRICS["curator_status"] = "dry_run"
        return 0

    written = [write_post(s) for s in stories]
    for path in written:
        log.info("wrote %s", path.name)

    # SEEN MEANS PUBLISHED, not considered.
    #
    # This marked every `fresh` candidate, which is defensible when retention is
    # 45 days and a feed only exposes what it published this week: the entries
    # expire before the archive matters. It is catastrophic the moment a
    # category holds retention_days: null and its sources expose an archive.
    #
    # Measured: one run took 85 deep_dives candidates, published the 6 the cap
    # allowed, and marked all 85 seen forever. Brendan Gregg's ten posts, jvns's
    # twenty and Dan Luu's forty were burned in a single cycle to publish six —
    # and being permanent, they could never be reached again.
    #
    # It also contradicts the design the evergreen categories are built on: an
    # item surfaces once, is recorded, and the next run reaches for the
    # NEXT-BEST UNPUBLISHED item from that archive. Working gradually through a
    # backlog of good writing requires remembering what we published, not what
    # we looked at.
    METRICS["seen_added"] = record_published(seen, ranked, stories)
    save_seen(seen, policies)

    removed = prune_posts(max_posts)
    if removed:
        log.info("pruned %d old post(s)", removed)

    # PUBLICATION AND SURVIVAL, MEASURED SEPARATELY AND REPORTED TOGETHER.
    #
    # The pruner bug hid here for a whole taxonomy: deep_dives published 6 of 6
    # every cycle and survived 0, and neither number was wrong on its own. Only
    # the PAIR says anything. A category that publishes at its cap and holds no
    # posts is being deleted by something downstream of the ranker.
    live: dict[str, int] = {}
    for path in CONTENT_DIR.glob("*.md"):
        m = re.search(r"^category:\s*(\S+)\s*$", path.read_text(encoding="utf-8")[:800], re.M)
        live[m.group(1) if m else "unknown"] = live.get(m.group(1) if m else "unknown", 0) + 1
    METRICS["per_category_live"] = dict(sorted(live.items()))
    METRICS["posts_live"] = sum(live.values())
    for cat in sorted(set(per_cat) | set(live)):
        pub, alive = per_cat.get(cat, 0), live.get(cat, 0)
        flag = "  <-- PUBLISHED BUT NOT SURVIVING" if pub and not alive else ""
        log.info("survival %-14s published %2d | live %2d%s", cat, pub, alive, flag)

    METRICS["curator_status"] = "ok"
    log.info("done in %.1fs — %d new post(s)", time.monotonic() - started, len(written))
    return 0


def main() -> int:
    """Wrapper that guarantees metrics.json is written on every path."""
    started = time.monotonic()
    try:
        return _run()
    except Exception as exc:
        METRICS["curator_status"] = "error"
        METRICS["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        METRICS["duration_s"] = round(time.monotonic() - started, 2)
        write_metrics()


if __name__ == "__main__":
    sys.exit(main())
