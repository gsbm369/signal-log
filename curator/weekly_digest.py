#!/usr/bin/env python3
"""
Weekly digest — the week's top stories, emailed through the homelab's existing
Postfix relay.

Three deliberate constraints, matching the rest of the project:

  * Reuses the relay. Postfix already runs on this host and already relays
    outbound; this adds no mail dependency, no API key, no second sender identity.
  * Reuses the ranker's output. It does NOT re-rank. `heat` in each post's front
    matter is the ranker's own score for that story, normalised against the best
    in its run, so ordering here is the ordering the site already published.
  * A send failure is a metric, not a swallowed exception. It ships
    `event: weekly_digest, status: failed` to Loki and exits non-zero, the same
    contract as a failed publish.

Run:  python3 curator/weekly_digest.py [--dry-run] [--days 7] [--count 10]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import smtplib
import socket
import sys
import time
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from loki import push  # noqa: E402

CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", HERE.parent / "site/src/content/posts"))
CNAME_FILE = Path(os.environ.get("CNAME_FILE", HERE.parent / "site/public/CNAME"))

SMTP_HOST = os.environ.get("DIGEST_SMTP_HOST", "127.0.0.1")
SMTP_PORT = int(os.environ.get("DIGEST_SMTP_PORT", "25"))
MAIL_TO = os.environ.get("DIGEST_TO", "nikita@gs-bm.com")
MAIL_FROM = os.environ.get("DIGEST_FROM", "signal.log <alerts@gs-bm.com>")

log = logging.getLogger("digest")

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def site_url() -> str:
    """Same single source as astro.config.mjs: public/CNAME."""
    if os.environ.get("SITE_URL"):
        return os.environ["SITE_URL"].rstrip("/")
    try:
        cname = CNAME_FILE.read_text().strip()
        if cname:
            return f"https://{cname}"
    except OSError:
        pass
    return "http://localhost:8080"


def load_posts() -> list[dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    for path in sorted(CONTENT_DIR.glob("*.md")):
        try:
            m = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
            if not m:
                continue
            fm = yaml.safe_load(m.group(1)) or {}
        except (OSError, yaml.YAMLError) as exc:
            log.warning("skipping %s: %s", path.name, exc)
            continue
        pub = fm.get("pubDate")
        if isinstance(pub, str):
            pub = datetime.fromisoformat(pub)
        if not isinstance(pub, datetime):
            continue
        if pub.tzinfo is None:
            pub = pub.replace(tzinfo=timezone.utc)
        fm["_pub"] = pub
        fm["_slug"] = path.stem
        posts.append(fm)
    return posts


def select(posts: list[dict[str, Any]], days: int, count: int) -> list[dict[str, Any]]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    recent = [p for p in posts if p["_pub"] >= cutoff]
    # Ordering comes from the ranker, not from a second ranking pass here.
    #
    # Sort on the RAW score, not on `heat`. heat is normalised against the best
    # story in its own run, so every run's leader is 100 and a week's worth of
    # posts is a wall of ties — the digest surfaced that immediately. Posts
    # written before `score` existed fall back to heat.
    recent.sort(key=lambda p: (float(p.get("score", 0.0)) or int(p.get("heat", 0)) / 100.0,
                               p["_pub"]), reverse=True)
    return recent[:count]


def render(picks: list[dict[str, Any]], base: str, days: int) -> tuple[str, str]:
    span = f"{(datetime.now(timezone.utc) - timedelta(days=days)).strftime('%d %b')}" \
           f" – {datetime.now(timezone.utc).strftime('%d %b %Y')}"

    lines = [f"signal.log — the week in tech", span, "=" * 46, ""]
    for i, p in enumerate(picks, 1):
        url = f"{base}/posts/{p['_slug']}/"
        bars = "█" * max(1, round(int(p.get("heat", 0)) / 20)) or "█"
        lines += [
            f"{i:2}. {p.get('title', '(untitled)')}",
            f"    {p.get('description', '').strip()}",
            f"    {p.get('source', '?')} · heat {p.get('heat', 0)} {bars}",
            f"    {url}",
            "",
        ]
    lines += ["-" * 46,
              f"All {len(picks)} stories: {base}/",
              f"Feed: {base}/rss.xml",
              "",
              "Ranked by a deterministic heuristic — recency, source weight and topic",
              "relevance read from the headline. No model decides what appears."]
    text = "\n".join(lines)

    rows = []
    for i, p in enumerate(picks, 1):
        url = f"{base}/posts/{p['_slug']}/"
        heat = int(p.get("heat", 0))
        tags = " ".join(
            f'<span style="font:11px ui-monospace,monospace;color:#8a8d8f;border:1px solid #2a2c2f;'
            f'border-radius:99px;padding:1px 7px;margin-right:4px">{t}</span>'
            for t in (p.get("tags") or [])[:3])
        rows.append(f"""
      <tr><td style="padding:0 0 22px">
        <div style="font:11px ui-monospace,monospace;color:#d6ff3f">{i:02d}</div>
        <a href="{url}" style="font:600 17px/1.35 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;
           color:#f2f1ea;text-decoration:none">{p.get('title','(untitled)')}</a>
        <div style="font:14px/1.6 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;
             color:#8a8d8f;margin:6px 0 8px">{p.get('description','')}</div>
        <div>{tags}<span style="font:11px ui-monospace,monospace;color:#46484b">
             {p.get('source','?')} · heat {heat}</span></div>
      </td></tr>""")

    html = f"""<!doctype html><html><body style="margin:0;background:#08090a;padding:28px 0">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
    <table role="presentation" width="600" cellpadding="0" cellspacing="0"
           style="max-width:600px;background:#0d0f11;border:1px solid rgba(255,255,255,.09);
                  border-radius:16px;padding:30px 32px">
      <tr><td style="padding-bottom:6px">
        <span style="font:600 20px ui-monospace,monospace;color:#f2f1ea">signal<span
              style="color:#d6ff3f">.</span>log</span>
      </td></tr>
      <tr><td style="font:12px ui-monospace,monospace;color:#8a8d8f;padding-bottom:22px">
        the week in tech · {span}</td></tr>
      <tr><td style="border-top:1px dashed rgba(255,255,255,.09);padding-top:22px"></td></tr>
      {''.join(rows)}
      <tr><td style="border-top:1px dashed rgba(255,255,255,.09);padding-top:16px;
                     font:12px ui-monospace,monospace;color:#46484b">
        <a href="{base}/" style="color:#d6ff3f;text-decoration:none">all stories</a> ·
        <a href="{base}/rss.xml" style="color:#d6ff3f;text-decoration:none">rss</a><br><br>
        Ranked by a deterministic heuristic — recency, source weight and topic relevance
        read from the headline. No model decides what appears.
      </td></tr>
    </table>
  </td></tr></table></body></html>"""
    return text, html


def deferred_for(sender: str) -> tuple[int, str]:
    """How many messages from `sender` are stuck in the local mail queue.

    smtplib succeeding means Postfix ACCEPTED the message, not that anyone
    received it. Relay auth can fail minutes later and the mail sits deferred
    while the sender reports success — the same shape as `git push` succeeding
    while the deploy fails, which this project already learned to distrust once.
    """
    import subprocess
    for cmd in (["mailq"], ["postqueue", "-p"]):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        addr = sender.split("<")[-1].strip("> ")
        n = sum(1 for ln in out.splitlines()
                if ln[:1].isalnum() and ln[:1].isupper() and addr in ln)
        reason = ""
        for ln in out.splitlines():
            if "(" in ln and any(w in ln.lower() for w in ("refused", "fail", "unauthor", "timeout")):
                reason = ln.strip().strip("()")[:180]
                break
        return n, reason
    return -1, "queue not inspectable"


def send(subject: str, text: str, html: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=MAIL_FROM.split("@")[-1].strip("> "))
    msg["List-Id"] = "signal.log weekly <digest.signal-log>"
    msg["Auto-Submitted"] = "auto-generated"
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.send_message(msg)


def main() -> int:
    ap = argparse.ArgumentParser(description="Email the week's top stories.")
    ap.add_argument("--days", type=int, default=int(os.environ.get("DIGEST_DAYS", "7")))
    ap.add_argument("--count", type=int, default=int(os.environ.get("DIGEST_COUNT", "10")))
    ap.add_argument("--dry-run", action="store_true", help="render and print, send nothing")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-7s %(message)s",
                        datefmt="%H:%M:%S")

    started = time.monotonic()
    base = site_url()
    picks = select(load_posts(), args.days, args.count)
    subject = f"signal.log — {len(picks)} stories this week"

    record: dict[str, Any] = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": "weekly_digest",
        "stories": len(picks),
        "window_days": args.days,
        "site": base,
        "recipient": MAIL_TO,
        "relay": f"{SMTP_HOST}:{SMTP_PORT}",
        "dry_run": args.dry_run,
        "status": "ok",
        "error": None,
        "duration_s": 0.0,
    }

    if not picks:
        # Not an error: a genuinely quiet week. Recorded so a digest that stops
        # arriving is distinguishable from one that had nothing to say.
        record["status"] = "empty"
        record["duration_s"] = round(time.monotonic() - started, 2)
        log.warning("no posts in the last %d days — not sending", args.days)
        print("METRIC " + str(record), flush=True)
        print("loki push: " + push(record, level="warn", status="empty", service="digest"))
        return 0

    text, html = render(picks, base, args.days)
    log.info("%s -> %s via %s:%s", subject, MAIL_TO, SMTP_HOST, SMTP_PORT)
    for i, p in enumerate(picks, 1):
        log.info("  %2d. [heat %3d] %s", i, p.get("heat", 0), str(p.get("title"))[:64])

    if args.dry_run:
        print("\n" + "=" * 60 + "\n" + text + "\n" + "=" * 60)
        record["status"] = "dry_run"
        record["duration_s"] = round(time.monotonic() - started, 2)
        print("loki push: " + push(record, level="info", status="dry_run", service="digest"))
        return 0

    rc = 0
    try:
        send(subject, text, html)
        log.info("accepted by %s:%s", SMTP_HOST, SMTP_PORT)
    except (smtplib.SMTPException, OSError, socket.timeout) as exc:
        # Same contract as a failed publish: a metric, not a swallowed exception.
        record["status"] = "failed"
        record["error"] = f"{type(exc).__name__}: {exc}"
        log.error("send failed: %s", record["error"])
        rc = 1

    if rc == 0:
        # Acceptance is not delivery. Give the relay a moment, then look.
        time.sleep(float(os.environ.get("DIGEST_QUEUE_WAIT", "8")))
        n, reason = deferred_for(MAIL_FROM)
        record["queue_deferred"] = n
        if n > 0:
            record["status"] = "queued_deferred"
            record["error"] = reason or "message deferred in the local mail queue"
            log.error("ACCEPTED BUT NOT DELIVERED — %d message(s) deferred: %s", n, reason)
            rc = 1
        elif n == 0:
            record["status"] = "delivered"
            log.info("queue clear — relay accepted and forwarded it")

    record["duration_s"] = round(time.monotonic() - started, 2)
    print("METRIC " + json.dumps(record, separators=(",", ":")), flush=True)
    print("loki push: " + push(record,
                               level="error" if rc else "info",
                               status=record["status"], service="digest"), flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
