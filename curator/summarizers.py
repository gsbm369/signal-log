#!/usr/bin/env python3
"""
Pluggable summarizer backends.

Ranking and selection are done deterministically by ranker.py in every mode — no
backend is asked to choose what matters. A backend's only job is to turn an
already-selected article into prose.

    none       feed's own <description>, cleaned up. No model, no key, $0.
    ollama     a local model over HTTP. Free, self-hosted, no key.
    anthropic  claude-haiku-4-5 via the Batch API (50% off, not latency-bound).

All three satisfy the same interface:

    backend.name                       -> str
    backend.health()                   -> (ok: bool, detail: str)
    backend.summarize(articles)        -> list[Summary]
    backend.usage                      -> dict   (tokens/cost, zeroes if free)

`summarize` is given the ranked, capped list and returns one Summary per input,
in the same order, skipping nothing. A backend that fails on an individual
article must fall back to the feed description rather than drop the story.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

log = logging.getLogger("curator.summarizer")

# USD per million tokens. Only consulted by the anthropic backend.
PRICING: dict[str, dict[str, float]] = {
    "claude-opus-5":    {"input": 5.00, "output": 25.00, "cache_read": 0.50},
    "claude-sonnet-5":  {"input": 2.00, "output": 10.00, "cache_read": 0.20},
    "claude-haiku-4-5": {"input": 1.00, "output":  5.00, "cache_read": 0.10},
}
BATCH_DISCOUNT = 0.5  # Batch API is half price


@dataclass
class Summary:
    """One finished post, ready to be written to Markdown."""
    title: str
    description: str
    body: str
    tags: list[str]
    heat: int
    source_article: dict[str, Any] = field(default_factory=dict)


class Summarizer(Protocol):
    name: str
    usage: dict[str, Any]

    def health(self) -> tuple[bool, str]: ...
    def summarize(self, articles: list[dict[str, Any]]) -> list[Summary]: ...


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def _clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"&nbsp;?|&#160;?", " ", text)
    text = re.sub(r"&amp;?", "&", text)
    text = re.sub(r"&(?:quot|#34);", '"', text)
    text = re.sub(r"&(?:apos|#39);", "'", text)
    text = re.sub(r"&(?:lt|#60);", "<", text)
    text = re.sub(r"&(?:gt|#62);", ">", text)
    text = re.sub(r"&[a-z]+;|&#\d+;", " ", text)
    text = re.sub(r"\[\s*[.…]+\s*\]\s*$", "", text)   # feedparser's "[ ... ]" truncation marker
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _sentences(text: str, n: int) -> str:
    parts = [p.strip() for p in _SENTENCE_END.split(text) if p.strip()]
    return " ".join(parts[:n])


def _tags_from(article: dict[str, Any]) -> list[str]:
    """Tags come from the ranker's own keyword matches — already free."""
    matched = [m.strip().replace(" ", "-") for m in article.get("_matched", []) if m.strip()]
    seen, out = set(), []
    for m in matched:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out[:4] or ["tech"]


def _heat_from(article: dict[str, Any], pool_best: float) -> int:
    """Map the ranker's score onto the 0-100 heat scale, relative to the best
    story in this run so the meter stays meaningful on a quiet day."""
    score = float(article.get("_score", 0.0))
    if pool_best <= 0:
        return 50
    return max(5, min(100, round(100.0 * (score / pool_best) ** 0.6)))


def _fallback_summary(article: dict[str, Any], pool_best: float) -> Summary:
    """The `none` backend's output, and every other backend's safety net."""
    blurb = _clean(article.get("summary", ""))
    title = _clean(article.get("title", "")).rstrip(".")
    if not blurb:
        blurb = f"{article.get('source', 'The source')} published this without a summary."
    desc = _sentences(blurb, 2)[:220] or title[:220]
    body_parts = [blurb]
    body_parts.append(
        f"\n\n*Reproduced from the {article.get('source', 'source')} feed. "
        f"No model was used to write this entry — follow the link for the full article.*"
    )
    return Summary(
        title=title[:120],
        description=desc,
        body="".join(body_parts),
        tags=_tags_from(article),
        heat=_heat_from(article, pool_best),
        source_article=article,
    )


# --------------------------------------------------------------------------- #
# Backend: none
# --------------------------------------------------------------------------- #


class NoneSummarizer:
    """Uses each feed's own <description>. No model, no API key, no spend."""

    name = "none"

    def __init__(self, **_: Any) -> None:
        self.usage = {"model": "", "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}

    def health(self) -> tuple[bool, str]:
        return True, "no external dependency"

    def summarize(self, articles: list[dict[str, Any]]) -> list[Summary]:
        best = max((float(a.get("_score", 0.0)) for a in articles), default=0.0)
        return [_fallback_summary(a, best) for a in articles]


# --------------------------------------------------------------------------- #
# Backend: ollama
# --------------------------------------------------------------------------- #

_PROMPT = """You are writing a short entry for a technology briefing read by engineers.

Headline: {title}
Source:   {source}
Feed blurb: {blurb}

Write 120-200 words of plain Markdown summarising this story.

Rules:
- You have ONLY the headline and blurb above. You have not read the article.
- Do not invent quotes, figures, benchmark numbers, dates, or named sources.
- If the blurb is thin, say what is known and what remains unclear. That is fine.
- Plain declarative prose. No hype, no rhetorical questions, no second person.
- Do not repeat the headline as a heading. Do not add front matter.

Write only the summary."""


class OllamaSummarizer:
    """A local model served by Ollama on the Docker host. Free, no key.

    RAM is the constraint, not CPU — see the README. `llama3.2:3b` needs roughly
    3-4 GB resident and is adequate for compressing a feed blurb.
    """

    name = "ollama"

    def __init__(self, url: str = "", model: str = "", timeout: float = 120.0, **_: Any) -> None:
        self.url = (url or os.environ.get("OLLAMA_URL", "http://ollama:11434")).rstrip("/")
        self.model = model or os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
        self.timeout = timeout
        self.usage = {"model": self.model, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}

    def _post(self, path: str, payload: dict, timeout: float) -> dict:
        import urllib.request

        req = urllib.request.Request(
            f"{self.url}{path}",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())

    def health(self) -> tuple[bool, str]:
        import urllib.error
        import urllib.request

        try:
            with urllib.request.urlopen(f"{self.url}/api/tags", timeout=10) as resp:
                tags = json.loads(resp.read())
            names = [m.get("name", "") for m in tags.get("models", [])]
            if not any(n.split(":")[0] == self.model.split(":")[0] for n in names):
                return False, f"{self.url} reachable but model {self.model!r} not pulled (have: {names or 'none'})"
            return True, f"{self.url} ok, model {self.model}"
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            return False, f"{self.url} unreachable: {exc}"

    def summarize(self, articles: list[dict[str, Any]]) -> list[Summary]:
        best = max((float(a.get("_score", 0.0)) for a in articles), default=0.0)
        out: list[Summary] = []
        for art in articles:
            base = _fallback_summary(art, best)
            prompt = _PROMPT.format(
                title=_clean(art.get("title", "")),
                source=art.get("source", ""),
                blurb=_clean(art.get("summary", "")) or "(none provided)",
            )
            try:
                res = self._post(
                    "/api/generate",
                    {"model": self.model, "prompt": prompt, "stream": False,
                     "options": {"temperature": 0.4, "num_predict": 420}},
                    self.timeout,
                )
                body = (res.get("response") or "").strip()
                self.usage["input_tokens"] += int(res.get("prompt_eval_count", 0) or 0)
                self.usage["output_tokens"] += int(res.get("eval_count", 0) or 0)
                if len(body.split()) >= 40:
                    base.body = body
                else:
                    log.warning("ollama returned %d words for %r — keeping feed blurb",
                                len(body.split()), base.title[:50])
            except Exception as exc:  # a local model failing must not lose the story
                log.warning("ollama failed for %r (%s) — keeping feed blurb", base.title[:50], exc)
            out.append(base)
        return out


# --------------------------------------------------------------------------- #
# Backend: anthropic (Batch API)
# --------------------------------------------------------------------------- #

_SYSTEM = """You write entries for signal.log, a technology briefing read by engineers.

You are given one story that has already been selected. Do not judge whether it \
deserves coverage — that decision is made. Write it up.

- You have only the headline and the feed blurb. You have NOT read the article. Do \
not invent quotes, figures, benchmark numbers, dates, or named sources.
- Where the material is thin, write a shorter piece stating what is known and what \
remains unclear. That is a correct outcome.
- Plain declarative prose. No hype adjectives, no rhetorical questions, no second person.
- Assume the reader knows what a GPU, a container, and a CVE are."""

_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Rewritten headline, no trailing period, max ~80 chars."},
        "description": {"type": "string", "description": "One or two sentences, max ~220 chars."},
        "body": {"type": "string", "description": "120-220 words of Markdown. No front matter, no repeated title heading."},
    },
    "required": ["title", "description", "body"],
    "additionalProperties": False,
}


class AnthropicSummarizer:
    """claude-haiku-4-5 through the Batch API.

    Batch is the right shape here: a nightly cron job is not latency-sensitive,
    and it is half price. Results come back in arbitrary order and are matched by
    custom_id, never by position.
    """

    name = "anthropic"

    def __init__(self, model: str = "", poll_seconds: float = 20.0,
                 max_wait_seconds: float = 3600.0, **_: Any) -> None:
        self.model = model or os.environ.get("CURATOR_MODEL", "claude-haiku-4-5")
        self.poll_seconds = poll_seconds
        self.max_wait_seconds = max_wait_seconds
        self.usage = {"model": self.model, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}

    def health(self) -> tuple[bool, str]:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return False, "ANTHROPIC_API_KEY is not set"
        if self.model not in PRICING:
            return True, f"model {self.model} (no local price table — cost will report 0)"
        return True, f"model {self.model} via Batch API"

    def _cost(self, tin: int, tout: int) -> float:
        p = PRICING.get(self.model)
        if not p:
            return 0.0
        return round((tin * p["input"] + tout * p["output"]) / 1_000_000 * BATCH_DISCOUNT, 6)

    def summarize(self, articles: list[dict[str, Any]]) -> list[Summary]:
        import anthropic
        from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
        from anthropic.types.messages.batch_create_params import Request

        best = max((float(a.get("_score", 0.0)) for a in articles), default=0.0)
        results: dict[str, Summary] = {}
        client = anthropic.Anthropic()

        requests = []
        for i, art in enumerate(articles):
            user = (
                f"Headline: {_clean(art.get('title',''))}\n"
                f"Source: {art.get('source','')}\n"
                f"Feed blurb: {_clean(art.get('summary','')) or '(none provided)'}"
            )
            requests.append(
                Request(
                    custom_id=f"story-{i}",
                    params=MessageCreateParamsNonStreaming(
                        model=self.model,
                        max_tokens=2000,
                        system=_SYSTEM,
                        messages=[{"role": "user", "content": user}],
                        output_config={"format": {"type": "json_schema", "schema": _SCHEMA}},
                    ),
                )
            )

        batch = client.messages.batches.create(requests=requests)
        log.info("batch %s submitted with %d request(s)", batch.id, len(requests))

        waited = 0.0
        while waited < self.max_wait_seconds:
            batch = client.messages.batches.retrieve(batch.id)
            if batch.processing_status == "ended":
                break
            time.sleep(self.poll_seconds)
            waited += self.poll_seconds
            log.info("batch %s: %s (%.0fs)", batch.id, batch.processing_status, waited)
        else:
            log.error("batch %s did not finish within %.0fs — using feed blurbs",
                      batch.id, self.max_wait_seconds)
            return [_fallback_summary(a, best) for a in articles]

        for entry in client.messages.batches.results(batch.id):
            cid = entry.custom_id
            if entry.result.type != "succeeded":
                log.warning("%s: %s — keeping feed blurb", cid, entry.result.type)
                continue
            msg = entry.result.message
            if getattr(msg, "stop_reason", None) == "refusal":
                log.warning("%s: refused by safety classifier — keeping feed blurb", cid)
                continue
            self.usage["input_tokens"] += msg.usage.input_tokens
            self.usage["output_tokens"] += msg.usage.output_tokens
            try:
                text = next(b.text for b in msg.content if b.type == "text")
                data = json.loads(text)
            except (StopIteration, json.JSONDecodeError) as exc:
                log.warning("%s: unparseable output (%s) — keeping feed blurb", cid, exc)
                continue
            idx = int(cid.rsplit("-", 1)[1])
            art = articles[idx]
            results[cid] = Summary(
                title=str(data["title"]).strip().rstrip("."),
                description=str(data["description"]).strip(),
                body=str(data["body"]).strip(),
                tags=_tags_from(art),
                heat=_heat_from(art, best),
                source_article=art,
            )

        self.usage["cost_usd"] = self._cost(self.usage["input_tokens"], self.usage["output_tokens"])

        # Preserve input order; anything the batch did not return falls back.
        return [results.get(f"story-{i}") or _fallback_summary(a, best)
                for i, a in enumerate(articles)]


# --------------------------------------------------------------------------- #
# Factory
# --------------------------------------------------------------------------- #

BACKENDS = {"none": NoneSummarizer, "ollama": OllamaSummarizer, "anthropic": AnthropicSummarizer}


def build(name: str, **kwargs: Any) -> Summarizer:
    key = (name or "none").strip().lower()
    if key not in BACKENDS:
        raise ValueError(f"unknown summarizer backend {name!r}; choose one of {sorted(BACKENDS)}")
    return BACKENDS[key](**kwargs)
