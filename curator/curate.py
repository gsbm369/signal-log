#!/usr/bin/env python3
"""
signal.log curator
==================

Pulls RSS from the major tech feeds, asks Claude which stories actually matter,
and writes the survivors into the Astro content directory as Markdown.

Run:  python curate.py [--dry-run] [--count N]
Env:  ANTHROPIC_API_KEY (required), CONTENT_DIR, STATE_DIR, FEEDS_FILE
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
from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    NotFoundError,
    RateLimitError,
)

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

HERE = Path(__file__).resolve().parent

FEEDS_FILE = Path(os.environ.get("FEEDS_FILE", HERE / "feeds.yml"))
CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", HERE.parent / "site/src/content/posts"))
STATE_DIR = Path(os.environ.get("STATE_DIR", HERE / "state"))
SEEN_FILE = STATE_DIR / "seen.json"

MODEL = os.environ.get("CURATOR_MODEL", "claude-opus-5")
SEEN_RETENTION_DAYS = 45
FETCH_TIMEOUT = 20

# USD per million tokens, for the per-run cost estimate written to metrics.json.
# Update alongside any model change.
PRICING: dict[str, dict[str, float]] = {
    "claude-opus-5":    {"input": 5.00, "output": 25.00, "cache_read": 0.50},
    "claude-sonnet-5":  {"input": 2.00, "output": 10.00, "cache_read": 0.20},
    "claude-haiku-4-5": {"input": 1.00, "output":  5.00, "cache_read": 0.10},
}

# Written to $STATE_DIR/metrics.json every run — run-cycle.sh ships this to Loki.
METRICS: dict[str, Any] = {
    "articles_fetched": 0,
    "articles_new": 0,
    "articles_kept": 0,
    "feeds_ok": 0,
    "feeds_failed": 0,
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_read_tokens": 0,
    "model": MODEL,
    "cost_usd": 0.0,
    "curator_status": "not_run",
    "error": None,
    "duration_s": 0.0,
}

log = logging.getLogger("curator")


def estimate_cost(model: str, in_tok: int, out_tok: int, cache_tok: int = 0) -> float:
    """Rough USD cost of one curation call. Unknown models price as 0."""
    price = PRICING.get(model)
    if not price:
        return 0.0
    return round(
        (in_tok * price["input"] + out_tok * price["output"] + cache_tok * price["cache_read"])
        / 1_000_000,
        6,
    )


def write_metrics() -> None:
    """Persist run metrics where the cycle script can find them. Never raises."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        (STATE_DIR / "metrics.json").write_text(json.dumps(METRICS, indent=2))
    except OSError as exc:
        log.warning("could not write metrics.json: %s", exc)


# --------------------------------------------------------------------------- #
# Output contract — Claude must return exactly this shape
# --------------------------------------------------------------------------- #

BRIEFING_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "stories": {
            "type": "array",
            "description": "The selected stories, most significant first.",
            "items": {
                "type": "object",
                "properties": {
                    "candidate_id": {
                        "type": "integer",
                        "description": "The id of the source candidate this story came from.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Rewritten headline. Plain, specific, no clickbait, no trailing period. Max ~80 chars.",
                    },
                    "description": {
                        "type": "string",
                        "description": "One or two sentences stating what happened and why it matters. Max ~220 chars.",
                    },
                    "body": {
                        "type": "string",
                        "description": (
                            "The summary in Markdown, 150-320 words. Use '## ' headings sparingly, "
                            "bullet lists where they help, and bold for key figures. Do not repeat "
                            "the title as a heading. Do not include front matter."
                        ),
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "2-4 lowercase single-word or hyphenated topic tags.",
                    },
                    "heat": {
                        "type": "integer",
                        "description": (
                            "0-100. How much this story actually changes things for people who build "
                            "technology. Reserve 85+ for genuinely consequential news."
                        ),
                    },
                },
                "required": ["candidate_id", "title", "description", "body", "tags", "heat"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["stories"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """You are the editor of signal.log, an automated technology briefing \
read by engineers and technical founders.

Your job each run is to look at a batch of raw RSS headlines and decide which few are \
worth anyone's attention, then write them up.

What earns a slot:
- Something concrete changed: a shipped release, a real acquisition, a measured result, \
a security incident with impact, a regulatory decision that binds someone.
- Technical substance a practitioner could act on or reason about.
- Genuine research results, not a press release about a research result.

What does not:
- Funding-round announcements with no product, personnel churn, conference keynotes.
- Rumour, "sources say", speculation about unannounced products.
- Opinion columns, listicles, "X is dead" takes, engagement bait.
- Near-duplicates of a story you already selected this run — pick the best one and drop the rest.
- Anything where the headline is the entire story.

Writing rules:
- Write from the headline and summary you are given. You have not read the full article, \
so do not invent quotes, figures, benchmark numbers, dates, or named sources. If a detail \
is not in the material you were given, leave it out rather than guessing.
- Where the source material is thin, write a shorter piece that states what is known and \
what remains unclear. That is a correct outcome, not a failure.
- Plain declarative prose. No hype adjectives, no "in a groundbreaking move", no rhetorical \
questions, no second person.
- Assume the reader knows what a GPU, a transformer, and a CVE are. Do not explain the basics.

Score `heat` honestly. A run where nothing scores above 60 is a normal, correct run."""


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:max_len].strip("-") or "untitled"


def url_key(url: str) -> str:
    """Stable identity for an article, ignoring tracking params."""
    clean = re.sub(r"[?#].*$", "", (url or "").strip().lower()).rstrip("/")
    return hashlib.sha256(clean.encode()).hexdigest()[:20]


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
    """Quote a scalar for YAML front matter."""
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
    take = max(4, int(feed.get("weight", 1)) * 8)
    try:
        parsed = feedparser.parse(
            url,
            agent="signal.log-curator/1.0 (+https://github.com/)",
            request_headers={"Cache-Control": "no-cache"},
        )
    except Exception as exc:  # feedparser surfaces transport errors in many shapes
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
        out.append(
            {
                "source": name,
                "title": title,
                "url": link,
                "published": published,
                "summary": strip_html(
                    getattr(entry, "summary", "") or getattr(entry, "description", "")
                ),
            }
        )
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
# Stage 2 — curate with Claude
# --------------------------------------------------------------------------- #


def build_batch_text(candidates: list[dict[str, Any]]) -> str:
    lines = []
    for i, art in enumerate(candidates):
        lines.append(
            f"[{i}] source={art['source']} | {art['published'].strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"    title: {art['title']}\n"
            f"    url: {art['url']}\n"
            f"    blurb: {art['summary'] or '(none provided)'}"
        )
    return "\n\n".join(lines)


def curate(client: Anthropic, candidates: list[dict[str, Any]], want: int) -> list[dict[str, Any]]:
    user_msg = (
        f"Here are {len(candidates)} articles pulled from the tech feeds in the last cycle.\n\n"
        f"{build_batch_text(candidates)}\n\n"
        f"Select the {want} most significant and write them up. If fewer than {want} clear the "
        f"bar, return fewer — publishing filler is worse than publishing less. Reference each "
        f"selection by its bracketed id as `candidate_id`."
    )

    log.info("asking Claude to curate %d candidates -> %d stories", len(candidates), want)

    try:
        with client.beta.messages.stream(
            model=MODEL,
            max_tokens=32000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
            thinking={"type": "adaptive"},
            output_config={
                "effort": "medium",
                "format": {"type": "json_schema", "schema": BRIEFING_SCHEMA},
            },
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        ) as stream:
            response = stream.get_final_message()
    except NotFoundError:
        log.error("model %r not available to this API key", MODEL)
        raise
    except RateLimitError:
        log.error("rate limited — try again later or lower publish_count")
        raise
    except APIStatusError as exc:
        log.error("API returned %s: %s", exc.status_code, exc.message)
        raise
    except APIConnectionError as exc:
        log.error("could not reach the API: %s", exc)
        raise

    if response.stop_reason == "refusal":
        detail = getattr(response, "stop_details", None)
        log.error("request declined by safety classifier (%s) — skipping this run", detail)
        METRICS["curator_status"] = "refused"
        METRICS["error"] = f"refusal: {detail}"
        return []

    usage = response.usage
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    METRICS["input_tokens"] = usage.input_tokens
    METRICS["output_tokens"] = usage.output_tokens
    METRICS["cache_read_tokens"] = cache_read
    METRICS["cost_usd"] = estimate_cost(
        MODEL, usage.input_tokens, usage.output_tokens, cache_read
    )
    log.info(
        "tokens in=%s out=%s cache_read=%s  ->  ~$%.4f on %s",
        usage.input_tokens,
        usage.output_tokens,
        cache_read,
        METRICS["cost_usd"],
        MODEL,
    )

    text = next((b.text for b in response.content if b.type == "text"), None)
    if not text:
        log.error("no text block in response")
        return []

    try:
        stories = json.loads(text).get("stories", [])
    except json.JSONDecodeError as exc:
        log.error("could not parse model output as JSON: %s", exc)
        return []

    # Re-attach the source article to each selection.
    resolved: list[dict[str, Any]] = []
    for story in stories:
        idx = story.get("candidate_id")
        if not isinstance(idx, int) or not 0 <= idx < len(candidates):
            log.warning("dropping story with bad candidate_id %r: %s", idx, story.get("title"))
            continue
        story["_source"] = candidates[idx]
        resolved.append(story)
    return resolved


# --------------------------------------------------------------------------- #
# Stage 3 — write Markdown
# --------------------------------------------------------------------------- #


def write_post(story: dict[str, Any]) -> Path:
    src = story["_source"]
    published = src["published"]
    body = str(story["body"]).strip()

    tags = [slugify(str(t), 24) for t in story.get("tags", [])][:4]
    words = len(body.split())
    read_minutes = max(1, round(words / 210))
    heat = max(0, min(100, int(story.get("heat", 50))))

    slug = f"{published.strftime('%Y-%m-%d')}-{slugify(story['title'])}"
    path = CONTENT_DIR / f"{slug}.md"

    front = "\n".join(
        [
            "---",
            f"title: {yaml_str(story['title'])}",
            f"description: {yaml_str(story['description'])}",
            f"pubDate: {published.isoformat()}",
            f"source: {yaml_str(src['source'])}",
            f"sourceUrl: {yaml_str(src['url'])}",
            f"tags: [{', '.join(yaml_str(t) for t in tags)}]",
            f"heat: {heat}",
            f"readMinutes: {read_minutes}",
            "---",
        ]
    )

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{front}\n\n{body}\n", encoding="utf-8")
    return path


def prune_posts(max_posts: int) -> int:
    posts = sorted(CONTENT_DIR.glob("*.md"))
    excess = len(posts) - max_posts
    if excess <= 0:
        return 0
    for path in posts[:excess]:  # filenames start with the date, so oldest sort first
        path.unlink()
    return excess


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def _run() -> int:
    ap = argparse.ArgumentParser(description="Curate tech RSS into Markdown posts.")
    ap.add_argument("--dry-run", action="store_true", help="fetch and curate but write nothing")
    ap.add_argument("--count", type=int, help="override how many stories to publish")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s  %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY is not set — put it in curator/.env or the environment")
        METRICS["curator_status"] = "skipped_no_key"
        return 2

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

    want = args.count or int(settings.get("publish_count", 6))
    max_candidates = int(settings.get("max_candidates", 70))
    max_posts = int(settings.get("max_posts", 60))
    max_age_hours = int(settings.get("max_age_hours", 36))

    started = time.monotonic()
    log.info("=== signal.log curator ===")

    articles = collect(feeds, max_age_hours)
    METRICS["articles_fetched"] = len(articles)
    log.info("collected %d unique articles", len(articles))
    if not articles:
        log.warning("nothing collected — every feed was empty or unreachable")
        METRICS["curator_status"] = "no_articles"
        METRICS["error"] = "all feeds empty or unreachable"
        return 1

    seen = load_seen()
    fresh = [a for a in articles if a["key"] not in seen][:max_candidates]
    METRICS["articles_new"] = len(fresh)
    log.info("%d new since the last run (capped at %d per run)", len(fresh), max_candidates)
    if not fresh:
        log.info("no new articles; nothing to do")
        METRICS["curator_status"] = "no_new"
        return 0

    client = Anthropic()
    stories = curate(client, fresh, want)
    METRICS["articles_kept"] = len(stories)
    if not stories:
        log.warning("curator selected nothing this run")
        if METRICS["curator_status"] == "not_run":
            METRICS["curator_status"] = "nothing_selected"
        return 0

    log.info("selected %d stories", len(stories))
    for s in stories:
        log.info("  [heat %3d] %s", s.get("heat", 0), s["title"])

    if args.dry_run:
        log.info("--dry-run: no files written")
        METRICS["curator_status"] = "dry_run"
        return 0

    written = [write_post(s) for s in stories]
    for path in written:
        log.info("wrote %s", path.name)

    now = datetime.now(timezone.utc).isoformat()
    for story in stories:
        seen[story["_source"]["key"]] = now
    # Mark everything we showed the model, so rejected items are not re-offered.
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
