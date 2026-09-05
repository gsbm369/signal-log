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


def load_metrics() -> dict:
    path = STATE_DIR / "metrics.json"
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {"curator_status": "unknown", "error": "metrics.json missing or unreadable"}


def push(record: dict, level: str) -> str:
    """Push one line to Loki. Returns a short status string; never raises."""
    if not LOKI_URL:
        return "disabled (LOKI_URL unset)"

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
    ap.add_argument("--exit-code", type=int, default=0)
    ap.add_argument("--duration", type=float, default=0.0)
    ap.add_argument("--posts-live", type=int, default=-1)
    args = ap.parse_args()

    m = load_metrics()
    curator_status = m.get("curator_status", "unknown")

    if args.exit_code != 0:
        level, cycle_status = "error", "failed"
    elif curator_status in ("error", "refused", "no_articles") or args.build_status != "ok":
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
        "exit_code": args.exit_code,
        "duration_s": round(args.duration, 1),
        "curator_duration_s": m.get("duration_s", 0.0),
        "articles_fetched": m.get("articles_fetched", 0),
        "articles_new": m.get("articles_new", 0),
        "articles_kept": m.get("articles_kept", 0),
        "feeds_ok": m.get("feeds_ok", 0),
        "feeds_failed": m.get("feeds_failed", 0),
        "model": m.get("model", ""),
        "input_tokens": m.get("input_tokens", 0),
        "output_tokens": m.get("output_tokens", 0),
        "cache_read_tokens": m.get("cache_read_tokens", 0),
        "cost_usd": m.get("cost_usd", 0.0),
        "posts_live": args.posts_live,
        "error": m.get("error"),
    }

    # Local log file (cron redirects stdout here) always gets the record.
    print("METRIC " + json.dumps(record, separators=(",", ":")), flush=True)
    print(f"loki push: {push(record, level)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
