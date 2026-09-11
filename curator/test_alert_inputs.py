#!/usr/bin/env python3
"""Every field an alert queries must actually arrive in Loki.

THE TENSION THIS EXISTS FOR, and it is not a mistake anyone will stop making:

    `or vector(0)` protects a rule against no-data AND hides an absent field,
    and you cannot get the first property without the second.

One construct cannot distinguish "the value is genuinely zero" from "nothing
ever wrote this field". Instance #3 in the README needed the fallback — without
it, total silence returned an empty result and the rule depended on
noDataState. The feeds_zero rule was defeated by the same fallback: the field
was in METRICS, ship_to_loki.py builds its record from an explicit whitelist and
did not forward it, and the rule evaluated `or vector(0)` for ever. Configured,
visible in the UI, structurally incapable of firing.

So the check cannot live in the alert. The alert cannot be the thing that
proves its own inputs exist.

This reads the alert definitions, extracts every field they unwrap, and asserts
each one appears in records Loki actually holds. Run by run-cycle.sh; also
runnable by hand.

Exit 0 all present, 1 a queried field is missing, 2 could not check.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
RULES = Path(os.environ.get(
    "ALERT_RULES_FILE", HERE.parent / "grafana/alerting/signal-log-alerts.yaml"))
LOKI = os.environ.get("LOKI_URL", "http://127.0.0.1:3100").rstrip("/")
JOB = os.environ.get("LOKI_JOB", "signal-log")
LOOKBACK_H = int(os.environ.get("ALERT_INPUT_LOOKBACK_H", "72"))

FAILURES: list[str] = []


def check(name, ok):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        FAILURES.append(name)


def queried_fields(doc: dict) -> dict[str, set[str]]:
    """field -> {rule uids that unwrap it}, for Loki-backed rules only."""
    out: dict[str, set[str]] = {}
    for group in doc.get("groups") or []:
        for rule in group.get("rules") or []:
            for q in rule.get("data") or []:
                expr = (q.get("model") or {}).get("expr", "") or ""
                if f'job="{JOB}"' not in expr:
                    continue          # prometheus rules have no Loki fields
                for field in re.findall(r"\|\s*unwrap\s+([A-Za-z_][A-Za-z0-9_]*)", expr):
                    out.setdefault(field, set()).add(rule.get("uid", "?"))
                # `| field = "x"` style label filters are inputs too.
                for field in re.findall(r"\|\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:=~?|!=)\s*[\"']", expr):
                    if field not in ("json", "line_format", "label_format"):
                        out.setdefault(field, set()).add(rule.get("uid", "?"))
    return out


def recent_records() -> list[dict]:
    end = int(time.time() * 1e9)
    start = end - LOOKBACK_H * 3600 * 10**9
    url = (f"{LOKI}/loki/api/v1/query_range?query="
           + urllib.parse.quote(f'{{job="{JOB}"}}')
           + f"&start={start}&end={end}&limit=200")
    with urllib.request.urlopen(url, timeout=15) as resp:
        payload = json.load(resp)
    records = []
    for stream in payload.get("data", {}).get("result", []):
        for _, line in stream.get("values", []):
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def main() -> int:
    if not RULES.exists():
        # Distinguished from "a field is missing" on purpose: the two have
        # completely different fixes and the caller logs a different line.
        print(f"\n  alert rules not found at {RULES} — cannot check")
        print("  SKIPPING. If this is the builder container, the image needs")
        print("  COPY grafana/alerting /app/grafana/alerting.")
        return 2

    doc = yaml.safe_load(RULES.read_text())
    fields = queried_fields(doc)
    print(f"\n-- fields queried by Loki-backed alert rules --")
    for f, uids in sorted(fields.items()):
        print(f"     {f:<22} {', '.join(sorted(uids))}")
    if not fields:
        print("  no Loki-backed rules found — nothing to check")
        return 0

    try:
        records = recent_records()
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        print(f"\n  could not reach Loki at {LOKI}: {exc}")
        print("  SKIPPING (this is a check, not a gate on the cycle)")
        return 2

    print(f"\n-- against {len(records)} record(s) from the last {LOOKBACK_H}h --")
    if not records:
        print("  Loki holds no records for this job — cannot verify. Not a failure:")
        print("  the stalled-cycle rules already cover the curator not reporting.")
        return 2

    present = set()
    for r in records:
        present |= set(r.keys())

    for field, uids in sorted(fields.items()):
        check(f"{field} appears in shipped records ({', '.join(sorted(uids))})",
              field in present)

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        print("A rule queries a field that never arrives. Its `or vector(0)` fallback")
        print("makes this look identical to a healthy zero, so the rule can never fire.")
        print("Add the field to the record in curator/ship_to_loki.py — that record is")
        print("an explicit WHITELIST, and a field in METRICS does not reach Loki without it.")
        return 1
    print("Every field the alerts query is present in shipped records.")
    return 0


if __name__ == "__main__":
    import urllib.parse  # noqa: E402  (used in recent_records)
    sys.exit(main())
