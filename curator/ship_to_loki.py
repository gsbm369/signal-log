#!/usr/bin/env python3
"""
Ships one publish-cycle record to Loki (and to stdout for the local log file).

Reads $STATE_DIR/metrics.json written by curate.py, merges in the build/publish
outcome passed on the command line, and pushes a single JSON log line.

Never fails the cycle: if Loki is unreachable the record still goes to stdout and
this exits 0.

Usage: ship_to_loki.py --build-status ok --publish-status ok --exit-code 0 --duration 62.4
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

STATE_DIR = Path(os.environ.get("STATE_DIR", "/data/state"))
LOKI_URL = os.environ.get("LOKI_URL", "").strip()
LOKI_TIMEOUT = float(os.environ.get("LOKI_TIMEOUT", "5"))
JOB_NAME = os.environ.get("LOKI_JOB", "signal-log")
HOSTNAME = os.environ.get("LOKI_HOST_LABEL") or socket.gethostname()


def _read(name: str) -> dict:
    try:
        return json.loads((STATE_DIR / name).read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def load_metrics() -> dict:
    """Merge the container's curation metrics with its build outcome. The
    container writes both; the host adds push/deploy status on top."""
    m = _read("metrics.json")
    if not m:
        m = {"curator_status": "unknown", "error": "metrics.json missing or unreadable"}
    m.update({k: v for k, v in _read("build.json").items()
              if k in ("posts_live", "build_duration_s")})
    return m


def push(record: dict, level: str, m: dict | None = None) -> str:
    """Push one line to Loki. Returns a short status string; never raises."""
    if not LOKI_URL:
        return "disabled (LOKI_URL unset)"

    m = m or {}
    payload = {
        "streams": [
            {
                # Labels stay low-cardinality — numbers live in the line, not here.
                "stream": {
                    "job": JOB_NAME,
                    "service": "curator",
                    "host": HOSTNAME,
                    "level": level,
                    "status": str(record.get("cycle_status", "unknown")),
                    "backend": str(m.get("backend") or "none"),
                },
                "values": [[str(time.time_ns()), json.dumps(record, separators=(",", ":"))]],
            }
        ]
    }

    req = urllib.request.Request(
        LOKI_URL.rstrip("/") + "/loki/api/v1/push",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    tenant = os.environ.get("LOKI_TENANT_ID")
    if tenant:
        req.add_header("X-Scope-OrgID", tenant)

    try:
        with urllib.request.urlopen(req, timeout=LOKI_TIMEOUT) as resp:
            return f"ok (HTTP {resp.status})"
    except urllib.error.HTTPError as exc:
        return f"FAILED (HTTP {exc.code}: {exc.read()[:200].decode(errors='replace')})"
    except (urllib.error.URLError, OSError, socket.timeout) as exc:
        return f"FAILED ({exc})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-status", default="unknown")
    ap.add_argument("--publish-status", default="unknown")
    ap.add_argument("--push-status", default="unknown")
    ap.add_argument("--deploy-status", default="unknown")
    ap.add_argument("--exit-code", type=int, default=0)
    ap.add_argument("--duration", type=float, default=0.0)
    ap.add_argument("--posts-live", type=int, default=-1)
    args = ap.parse_args()

    m = load_metrics()
    curator_status = m.get("curator_status", "unknown")

    # publish_failed is its own terminal state, distinct from a build failure.
    # It means the site built fine HERE and never reached production — the one
    # outcome most easily mistaken for success.
    if args.push_status == "failed" or args.deploy_status in ("failed", "timeout", "not_reached"):
        level, cycle_status = "error", "publish_failed"
    elif args.exit_code != 0:
        level, cycle_status = "error", "failed"
    elif curator_status in ("error", "refused", "no_articles", "backend_unavailable") \
            or args.build_status != "ok" or args.deploy_status == "unverified":
        level, cycle_status = "warn", "degraded"
    else:
        level, cycle_status = "info", "ok"

    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": "publish_cycle",
        "cycle_status": cycle_status,
        "curator_status": curator_status,
        "build_status": args.build_status,
        "publish_status": args.publish_status,
        "push_status": args.push_status,
        "deploy_status": args.deploy_status,
        # The single field an alert should watch: did content reach production
        # this cycle, or was there legitimately nothing to publish?
        "reached_production": args.deploy_status in ("ok", "not_needed", "skipped"),
        "exit_code": args.exit_code,
        "duration_s": round(args.duration, 1),
        "curator_duration_s": m.get("duration_s", 0.0),
        "articles_fetched": m.get("articles_fetched", 0),
        "articles_new": m.get("articles_new", 0),
        "articles_kept": m.get("articles_kept", 0),
        "articles_ranked": m.get("articles_ranked", 0),
        "dropped_noise": m.get("dropped_noise", 0),
        "dropped_dupe": m.get("dropped_dupe", 0),
        "dropped_capped": m.get("dropped_capped", 0),
        "backend": m.get("backend", ""),
        "feeds_ok": m.get("feeds_ok", 0),
        "feeds_failed": m.get("feeds_failed", 0),
        "model": m.get("model", ""),
        "input_tokens": m.get("input_tokens", 0),
        "output_tokens": m.get("output_tokens", 0),
        "cache_read_tokens": m.get("cache_read_tokens", 0),
        "cost_usd": m.get("cost_usd", 0.0),
        "posts_live": args.posts_live if args.posts_live >= 0 else m.get("posts_live", -1),
        "error": m.get("error"),
    }

    # Local log file (cron redirects stdout here) always gets the record.
    print("METRIC " + json.dumps(record, separators=(",", ":")), flush=True)
    print(f"loki push: {push(record, level, m)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
