#!/usr/bin/env python3
"""Every metric the curator records either ships to Loki or is deliberately not.

ship_to_loki.py builds its record from an EXPLICIT WHITELIST. That is the right
design — it keeps the log line stable and stops incidental state leaking into
observability — but it has now cost twice:

  feeds_zero          was in METRICS, not in the record, so the alert that
                      queried it evaluated `or vector(0)` for ever. Configured,
                      visible, and structurally incapable of firing.
  per_category_live   was in METRICS, not in the record, so the category balance
                      existed only in metrics.json, which is overwritten every
                      cycle. Any question about how the balance moved over a
                      week was unanswerable — and would have stayed unanswerable
                      while looking like it was being recorded.

Both were found by applying a rule, not by noticing. This is that rule as a
test: a new METRICS key must be shipped, or named here as intentionally local.
Adding a key and forgetting the record is the easy mistake; this makes it loud
at the point of the edit rather than months later.

No network, no model, no API key.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHIPPER = HERE / "ship_to_loki.py"
STATE = Path(os.environ.get("STATE_DIR", HERE / "state")) / "metrics.json"

# Keys that stay on the box on purpose. Each needs a reason, because "we did not
# get round to it" and "this does not belong in Loki" look identical otherwise.
LOCAL_ONLY = {
    "error":                "shipped, but under its own key after status mapping",
    "per_category":         "shipped flattened as published_<category>",
    "per_category_live":    "shipped flattened as live_<category>",
    "per_source_candidates": "one key per source would be unbounded label churn; "
                             "feeds_zero and feeds_zero_names carry the signal",
    "rejected_by_source":   "same — bounded summaries ship instead",
    "rejected_by_category": "nested; rejected_by_reason carries the totals",
    "rejected_by_reason":   "TODO: worth shipping, no alert queries it yet",
    "seen_expired":         "nested per category; seen_total carries the size",
    "candidate_cut":        "diagnostic, per run, not a time series",
    "duration_s":           "shipped as curator_duration_s",
    "deferred_total":       "TODO: worth shipping once the store has a steady state",
    "deferred_probed":      "TODO: same",
    "deferred_ripened":     "TODO: same",
    "deferred_gave_up":     "TODO: same",
}

FAILURES: list[str] = []


def check(name, ok):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        FAILURES.append(name)


def shipped_keys(src: str) -> set[str]:
    """Literal keys in the record, plus the f-string prefixes it expands."""
    body = src[src.index("record = {"):]
    keys = set(re.findall(r'^\s*"([a-z_]+)":', body, re.M))
    keys |= {m.group(1) for m in re.finditer(r'f"([a-z_]+)_\{k\}"', body)}
    return keys


def main() -> int:
    if not STATE.exists():
        print(f"  no metrics.json at {STATE} — run a cycle first")
        return 2

    recorded = set(json.loads(STATE.read_text()))
    shipped = shipped_keys(SHIPPER.read_text())

    missing = sorted(k for k in recorded if k not in shipped and k not in LOCAL_ONLY)
    stale = sorted(k for k in LOCAL_ONLY if k not in recorded)

    print(f"\n-- METRICS keys vs the Loki whitelist --")
    print(f"     recorded by the curator : {len(recorded)}")
    print(f"     shipped to Loki         : {len(shipped & recorded)}")
    print(f"     deliberately local      : {len(LOCAL_ONLY) - len(stale)}")

    check("every recorded metric is shipped or declared local", not missing)
    if missing:
        print("\n  These are recorded and go nowhere:")
        for k in missing:
            print(f"    {k}")
        print("\n  Either add them to the record in ship_to_loki.py, or add them to")
        print("  LOCAL_ONLY here WITH A REASON. A metric nobody ships is a question")
        print("  nobody can answer later.")

    check("LOCAL_ONLY has no entries for metrics that no longer exist", not stale)
    if stale:
        print(f"    stale exemptions: {stale}")

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("Metric coverage is accounted for.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
