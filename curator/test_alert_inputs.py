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

This reads EVERY rule file in grafana/alerting/ and checks both backends:

  Loki        every field a rule unwraps OR filters on (`| exit_code = 0`,
              `| deploy_status =~ "..."`, numeric or quoted) must appear in
              records Loki actually holds for that stream; every stream label
              a non-signal-log selector names must exist in Loki.
  Prometheus  every selector a rule queries (`up`,
              `node_filesystem_avail_bytes{mountpoint="/",...}`) must return
              at least one live series. A misspelt metric or a label value
              that never matches is an empty result, and `or vector(0)` turns
              an empty result into a healthy-looking number.

Until 2026-09-19 it read one file, matched only quoted filter values (so
`exit_code = 0`, which both stalled rules depend on, was never checked) and
skipped Prometheus rules entirely.

Run by run-cycle.sh; also runnable by hand.

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
RULES_DIR = Path(os.environ.get("ALERT_RULES_DIR", HERE.parent / "grafana/alerting"))
LOKI = os.environ.get("LOKI_URL", "http://127.0.0.1:3100").rstrip("/")
PROM = os.environ.get("PROM_URL", "http://127.0.0.1:9090").rstrip("/")
JOB = os.environ.get("LOKI_JOB", "signal-log")
LOOKBACK_H = int(os.environ.get("ALERT_INPUT_LOOKBACK_H", "72"))

FAILURES: list[str] = []


def check(name, ok):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        FAILURES.append(name)


FILTER = re.compile(r"\|\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:=~|!~|!=|==|>=|<=|=|>|<)")
UNWRAP = re.compile(r"\|\s*unwrap\s+([A-Za-z_][A-Za-z0-9_]*)")
STREAM = re.compile(r"\{([^}]*)\}")
LABEL = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:=~|!~|!=|=)")
PROMQL_WORDS = {"sum", "min", "max", "avg", "count", "or", "and", "unless", "by",
                "without", "on", "ignoring", "vector", "rate", "irate", "increase",
                "offset", "bool", "group_left", "group_right", "abs", "time",
                "count_over_time", "min_over_time", "max_over_time", "avg_over_time",
                "sum_over_time", "last_over_time", "absent", "topk", "bottomk",
                "histogram_quantile", "label_replace", "clamp_min", "clamp_max"}


def rules(docs):
    for doc in docs:
        for group in doc.get("groups") or []:
            for rule in group.get("rules") or []:
                yield rule


def backend(q) -> str:
    """Which datasource a query runs on. Uids are pinned constants."""
    uid = q.get("datasourceUid", "")
    typ = ((q.get("model") or {}).get("datasource") or {}).get("type", "")
    return typ or uid


def queried_fields(docs) -> dict[str, set[str]]:
    """Loki json field -> {rule uids}: everything unwrapped or filtered on in a
    {job="<JOB>"} query."""
    out: dict[str, set[str]] = {}
    for rule in rules(docs):
        for q in rule.get("data") or []:
            expr = (q.get("model") or {}).get("expr", "") or ""
            if backend(q) != "loki" or f'job="{JOB}"' not in expr:
                continue
            pipeline = STREAM.sub("", expr)      # drop the {…} selector itself
            for field in UNWRAP.findall(pipeline) + FILTER.findall(pipeline):
                if field not in ("json", "logfmt", "line_format", "label_format", "unwrap"):
                    out.setdefault(field, set()).add(rule.get("uid", "?"))
    return out


def stream_labels(docs) -> dict[str, set[str]]:
    """Loki stream label -> {rule uids}, for selectors other than the job."""
    out: dict[str, set[str]] = {}
    for rule in rules(docs):
        for q in rule.get("data") or []:
            expr = (q.get("model") or {}).get("expr", "") or ""
            if backend(q) != "loki":
                continue
            for sel in STREAM.findall(expr):
                for lab in LABEL.findall(sel):
                    if lab != "job":
                        out.setdefault(lab, set()).add(rule.get("uid", "?"))
    return out


def prom_selectors(docs) -> dict[str, set[str]]:
    """PromQL instant selector (metric plus its {matchers}) -> {rule uids}."""
    out: dict[str, set[str]] = {}
    for rule in rules(docs):
        for q in rule.get("data") or []:
            expr = (q.get("model") or {}).get("expr", "") or ""
            if backend(q) != "prometheus":
                continue
            bare = re.sub(r'"[^"]*"', '""', expr)
            for m in re.finditer(r"([A-Za-z_:][A-Za-z0-9_:]*)\s*(\{[^}]*\})?", bare):
                name = m.group(1)
                prev = bare[:m.start()].rstrip()
                if name in PROMQL_WORDS or re.match(r"\s*\(", bare[m.end():]) or prev.endswith(("by", "without")):
                    continue
                if prev.endswith("(") and re.search(r"\b(by|without|on|ignoring)\s*\($", prev):
                    continue
                if re.fullmatch(r"\d.*", name):
                    continue
                # Recover the ORIGINAL matchers (with their quoted values).
                orig = re.search(re.escape(name) + r"\s*(\{[^}]*\})?", expr[m.start():])
                sel = name + ((orig.group(1) or "") if orig else "")
                out.setdefault(sel, set()).add(rule.get("uid", "?"))
    return out


def prom_count(selector: str) -> int:
    url = f"{PROM}/api/v1/query?query=" + urllib.parse.quote(f"count({selector})")
    with urllib.request.urlopen(url, timeout=15) as resp:
        res = json.load(resp).get("data", {}).get("result", [])
    return int(float(res[0]["value"][1])) if res else 0


def loki_labels() -> set[str]:
    with urllib.request.urlopen(f"{LOKI}/loki/api/v1/labels", timeout=15) as resp:
        return set(json.load(resp).get("data") or [])


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
    files = sorted(RULES_DIR.glob("*.y*ml"))
    if not files:
        # Distinguished from "a field is missing" on purpose: the two have
        # completely different fixes and the caller logs a different line.
        print(f"\n  no alert rule files in {RULES_DIR} — cannot check")
        print("  SKIPPING. If this is the builder container, the image needs")
        print("  COPY grafana/alerting /app/grafana/alerting.")
        return 2

    docs = [yaml.safe_load(f.read_text()) or {} for f in files]
    paused = {r.get("uid") for r in rules(docs) if r.get("isPaused")}
    tag = lambda uids: ", ".join(sorted(u + (" [paused]" if u in paused else "") for u in uids))
    fields, labels, selectors = queried_fields(docs), stream_labels(docs), prom_selectors(docs)
    unchecked = 0

    print(f"\n-- Loki: fields filtered or unwrapped by {{job=\"{JOB}\"}} rules --")
    for f, uids in sorted(fields.items()):
        print(f"     {f:<22} {tag(uids)}")
    if fields:
        try:
            records = recent_records()
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            print(f"  could not reach Loki at {LOKI}: {exc} — SKIPPED")
            records, unchecked = None, unchecked + 1
        if records == []:
            print("  Loki holds no records for this job — cannot verify.")
            unchecked += 1
        elif records:
            print(f"  against {len(records)} record(s) from the last {LOOKBACK_H}h:")
            present = set().union(*(r.keys() for r in records))
            for field, uids in sorted(fields.items()):
                check(f"field {field} arrives in Loki ({tag(uids)})", field in present)

    if labels:
        print(f"\n-- Loki: stream labels named by other selectors --")
        try:
            known = loki_labels()
            for lab, uids in sorted(labels.items()):
                ok = lab in known
                if not ok and uids <= paused:
                    print(f"  WARN  stream label {lab} absent, but only paused rules use it ({tag(uids)})")
                else:
                    check(f"stream label {lab} exists in Loki ({tag(uids)})", ok)
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            print(f"  could not reach Loki at {LOKI}: {exc} — SKIPPED")
            unchecked += 1

    if selectors:
        print(f"\n-- Prometheus: every selector must return a live series --")
        try:
            for sel, uids in sorted(selectors.items()):
                n = prom_count(sel)
                check(f"{sel} -> {n} series ({tag(uids)})", n > 0)
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            print(f"  could not reach Prometheus at {PROM}: {exc} — SKIPPED")
            unchecked += 1

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        print("A rule queries an input that never arrives. Its `or vector(0)` fallback")
        print("makes this look identical to a healthy value, so the rule can never fire.")
        print("Loki field: add it to the record in curator/ship_to_loki.py (an explicit")
        print("WHITELIST). Prometheus: fix the metric name or matcher in the rule.")
        return 1
    if unchecked:
        print(f"{unchecked} backend(s) could not be checked — not a pass.")
        return 2
    print("Every field, label and series the alerts query is present.")
    return 0


if __name__ == "__main__":
    import urllib.parse  # noqa: E402  (used in recent_records)
    sys.exit(main())
