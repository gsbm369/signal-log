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
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import feedparser
import yaml

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

SEEN_RETENTION_DAYS = 45

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


def entry_datetime(entry: Any) -> datetime:
    for field in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, field, None)
        if parsed:
            return datetime(*parsed[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def yaml_str(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


# --------------------------------------------------------------------------- #
# State
# --------------------------------------------------------------------------- #


def load_seen() -> dict[str, str]:
    if not SEEN_FILE.exists():
        return {}
    try:
        data = json.loads(SEEN_FILE.read_text())
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("could not read state file (%s) — starting fresh", exc)
        return {}


def save_seen(seen: dict[str, str]) -> None:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=SEEN_RETENTION_DAYS)).isoformat()
    pruned = {k: v for k, v in seen.items() if v >= cutoff}
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SEEN_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(pruned, indent=2))
    tmp.replace(SEEN_FILE)


# --------------------------------------------------------------------------- #
# Stage 1 — collect
# --------------------------------------------------------------------------- #


def fetch_feed(feed: dict[str, Any], max_age: timedelta) -> list[dict[str, Any]]:
    name, url = feed["name"], feed["url"]
    # `fetch` is how many entries to pull; `weight` is the ranking multiplier.
    # These were the same field, so compressing weights to the 0.85-1.30 band
    # would have silently cut every feed's contribution to ~7 entries.
    take = max(4, int(feed.get("fetch", 15)))
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
        published = entry_datetime(entry)
        if now - published > max_age:
            continue
        out.append({
            "source": name,
            "title": title,
            "url": link,
            "published": published,
            "summary": strip_html(
                getattr(entry, "summary", "") or getattr(entry, "description", ""), 900
            ),
        })
    log.info("[%s] %d candidates", name, len(out))
    METRICS["feeds_ok"] += 1
    return out


def collect(feeds: list[dict[str, Any]], max_age_hours: int) -> list[dict[str, Any]]:
    max_age = timedelta(hours=max_age_hours)
    with ThreadPoolExecutor(max_workers=min(8, len(feeds))) as pool:
        batches = pool.map(lambda f: fetch_feed(f, max_age), feeds)

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

    front = "\n".join([
        "---",
        f"title: {yaml_str(summary.title)}",
        f"description: {yaml_str(summary.description)}",
        f"pubDate: {published.isoformat()}",
        f"source: {yaml_str(src['source'])}",
        f"sourceUrl: {yaml_str(src['url'])}",
        f"tags: [{', '.join(yaml_str(t) for t in tags)}]",
        f"heat: {heat}",
        f"score: {summary.score}",
        f"readMinutes: {read_minutes}",
        "---",
    ])

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{front}\n\n{body}\n", encoding="utf-8")
    return path


def prune_posts(max_posts: int) -> int:
    posts = sorted(CONTENT_DIR.glob("*.md"))
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
    max_age_hours = int(settings.get("max_age_hours", 36))
    per_source_cap = int(settings.get("per_source_cap", ranker.PER_SOURCE_CAP))

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
    articles = collect(feeds, max_age_hours)
    METRICS["articles_fetched"] = len(articles)
    log.info("collected %d unique articles", len(articles))
    if not articles:
        log.warning("nothing collected — every feed was empty or unreachable")
        METRICS["curator_status"] = "no_articles"
        METRICS["error"] = "all feeds empty or unreachable"
        return 1

    # --- drop what we have already published ---
    seen = load_seen()
    fresh = [a for a in articles if a["key"] not in seen][:max_candidates]
    METRICS["articles_new"] = len(fresh)
    log.info("%d new since the last run (cap %d)", len(fresh), max_candidates)
    if not fresh:
        log.info("no new articles; nothing to do")
        METRICS["curator_status"] = "no_new"
        return 0

    # --- rank (deterministic, no model) ---
    weights = {f["name"]: float(f.get("weight", ranker.DEFAULT_SOURCE_WEIGHT)) for f in feeds}
    ranked, rstats = ranker.rank(
        fresh, weights, limit=want, per_source_cap=per_source_cap,
        extra_noise=bool(settings.get("extra_noise_filter", True)),
    )
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
        log.info("  [%.4f  rel %.1f] %-22s %s",
                 a["_score"], a["_relevance"], a["source"][:22], a["title"][:70])

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

    now = datetime.now(timezone.utc).isoformat()
    for art in fresh:
        seen.setdefault(art["key"], now)
    save_seen(seen)

    removed = prune_posts(max_posts)
    if removed:
        log.info("pruned %d old post(s)", removed)

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
