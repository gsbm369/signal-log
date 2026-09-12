#!/usr/bin/env python3
"""Everything the curator records ships to Loki, unless it is exempted with a reason.

ship_to_loki.py used to build its record from a WHITELIST: nothing shipped
unless named. That default cost twice —

  feeds_zero          recorded, not shipped, so the alert querying it evaluated
                      `or vector(0)` for ever. Configured, visible in the UI,
                      and structurally incapable of firing.
  per_category_live   recorded, not shipped, so a week of category history was
                      never kept, while looking exactly like it was.

A test that catches whoever forgets is policing a bad default. The default is
now inverted: everything ships unless EXEMPT names it, which makes both bugs
impossible rather than detectable.

So this no longer hunts for forgotten metrics. It enforces what is left worth
enforcing: that every exemption carries a reason, that no exemption is stale,
and — checked against the RECORD THE CURATOR ACTUALLY EMITTED, not against the
source text — that nothing unexpected went missing.

Exit 0 accounted for, 1 a gap, 2 nothing to compare.
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHIPPER = HERE / "ship_to_loki.py"
STATE = Path(os.environ.get("STATE_DIR", HERE / "state")) / "metrics.json"
CYCLE_LOG = Path(os.environ.get("CYCLE_LOG", HERE.parent / "logs/cycle.log"))

FAILURES: list[str] = []


def check(name, ok):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        FAILURES.append(name)


def exemptions(src: str) -> dict[str, str]:
    """The EXEMPT dict, read from the source rather than duplicated here.

    Parsed with ast, not regex: the whole point of this test is that one list
    exists, and re-typing it in the test would recreate the two-lists problem
    it was written to remove.
    """
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "EXEMPT" for t in node.targets):
            return {ast.literal_eval(k): ast.literal_eval(v)
                    for k, v in zip(node.value.keys, node.value.values)}
    return {}


def emitted_record() -> dict | None:
    """The last record the curator actually shipped."""
    if not CYCLE_LOG.exists():
        return None
    for line in reversed(CYCLE_LOG.read_text(errors="ignore").splitlines()):
        if "METRIC {" in line:
            try:
                return json.loads(line[line.index("METRIC ") + 7:])
            except json.JSONDecodeError:
                continue
    return None


def main() -> int:
    src = SHIPPER.read_text()
    exempt = exemptions(src)

    print("\n-- exemptions --")
    check("the exemption list was found in ship_to_loki.py", bool(exempt))
    for key, reason in sorted(exempt.items()):
        print(f"     {key:<24} {reason}")
    check("every exemption carries a reason",
          all(isinstance(r, str) and r.strip() for r in exempt.values()))

    if not STATE.exists():
        print(f"\n  no metrics.json at {STATE} — cannot compare")
        return 2 if not FAILURES else 1
    recorded = json.loads(STATE.read_text())

    check("no exemption names a metric that no longer exists",
          all(k in recorded for k in exempt))
    for k in exempt:
        if k not in recorded:
            print(f"    stale exemption: {k}")

    record = emitted_record()
    if record is None:
        print("\n  no METRIC line in the cycle log — cannot verify what shipped")
        return 2 if not FAILURES else 1

    # A nested metric ships flattened, so its presence is proven by any key
    # carrying its prefix rather than by its own name.
    prefixes = {"per_category": "published_", "per_category_live": "live_"}
    missing = []
    for key, value in recorded.items():
        if key in exempt:
            continue
        if isinstance(value, dict):
            if not value:
                continue                      # nothing to flatten
            pre = prefixes.get(key, key + "_")
            if not any(k.startswith(pre) for k in record):
                missing.append(f"{key} (expected {pre}*)")
        elif key not in record:
            missing.append(key)

    print(f"\n-- {len(recorded)} recorded, {len(record)} keys in the emitted line --")
    check("everything recorded and not exempt reached the emitted record", not missing)
    for k in missing:
        print(f"    missing: {k}")
    if missing:
        print("\n  Either it should ship — the default — or it belongs in EXEMPT in")
        print("  ship_to_loki.py with a reason. 'We did not get round to it' and")
        print("  'this does not belong in Loki' are indistinguishable otherwise.")

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("Metric coverage is accounted for.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
