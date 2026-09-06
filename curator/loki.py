#!/usr/bin/env python3
"""Shared Loki push. Used by the publish cycle and the weekly digest.

Kept in one place so both emit the same stream labels and both fail the same
way: a shipping failure is reported and never raised, because losing a metric
must not take down the thing being measured.
"""

from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
import urllib.request
from typing import Any


def url() -> str:
    """Host-reachable URL wins: scripts run on the host, where the container
    name `loki` does not resolve."""
    return (os.environ.get("LOKI_URL_HOST") or os.environ.get("LOKI_URL") or "").strip()


def push(record: dict[str, Any], *, level: str, status: str,
         service: str = "curator", extra_labels: dict[str, str] | None = None) -> str:
    """Push one JSON line. Returns a short status string; never raises."""
    target = url()
    if not target:
        return "disabled (LOKI_URL unset)"

    labels = {
        "job": os.environ.get("LOKI_JOB", "signal-log"),
        "service": service,
        "host": os.environ.get("LOKI_HOST_LABEL") or socket.gethostname(),
        "level": level,
        "status": status,
    }
    labels.update(extra_labels or {})

    payload = {"streams": [{
        "stream": labels,
        "values": [[str(time.time_ns()), json.dumps(record, separators=(",", ":"))]],
    }]}

    req = urllib.request.Request(
        target.rstrip("/") + "/loki/api/v1/push",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    tenant = os.environ.get("LOKI_TENANT_ID")
    if tenant:
        req.add_header("X-Scope-OrgID", tenant)

    try:
        with urllib.request.urlopen(req, timeout=float(os.environ.get("LOKI_TIMEOUT", "5"))) as resp:
            return f"ok (HTTP {resp.status})"
    except urllib.error.HTTPError as exc:
        return f"FAILED (HTTP {exc.code}: {exc.read()[:200].decode(errors='replace')})"
    except (urllib.error.URLError, OSError, socket.timeout) as exc:
        return f"FAILED ({exc})"
