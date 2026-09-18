#!/usr/bin/env python3
"""The publish gate must refuse every way a stale card can reach the page.

check_freshness.py parses the BUILT index.html. These fixtures are minimal
pages carrying the same attributes PostCard emits. Each violation is its own
page, so a pass cannot come from one fixture masking another.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOW = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)
FAILURES: list[str] = []


def card(slug, age_days, section="gaming", label=None, published=True):
    iso = (NOW - timedelta(days=age_days)).isoformat()
    lab = (age_days > 1) if label is None else label
    pub = f' data-published="{iso}"' if published else ""
    return (f'<article class="row" data-cat="gaming"{pub} data-section="{section}">'
            f'<a href="/posts/{slug}/"></a><h3>{slug}</h3>'
            + ('<span class="chip chip--week" data-label="this-week">this week</span>' if lab else "")
            + "</article>")


def run(html: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as td:
        idx = Path(td) / "index.html"
        idx.write_text(f"<html><body>{html}</body></html>")
        env = dict(os.environ, BUILT_INDEX=str(idx), STATE_DIR=td,
                   CYCLE_START_UTC=NOW.isoformat())
        r = subprocess.run([sys.executable, str(HERE / "check_freshness.py")],
                           env=env, capture_output=True, text=True)
        return r.returncode, r.stdout


def check(name, rc, want):
    ok = rc == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}  (exit {rc})")
    if not ok:
        FAILURES.append(name)


def main() -> int:
    clean = card("a", 0.2, "fold") + card("b", 3, "gaming") + card("c", 6.9, "tail")
    check("a clean page passes", run(clean)[0], 0)
    check("a PLANTED 8-DAY card is refused", run(clean + card("stale", 8))[0], 1)
    check("a 110-day card is refused", run(clean + card("luu", 110, "deep_dives"))[0], 1)
    check("a week-old card WITHOUT its label is refused",
          run(clean + card("unlabelled", 3, label=False))[0], 1)
    check("a card with no data-published cannot hide from the gate",
          run(clean + card("anon", 0.1, published=False))[0], 1)
    check("the same post URL rendered twice is refused",
          run(clean + card("a", 0.2, "system_design"))[0], 1)
    check("a today card needs no label", run(card("fresh", 0.5, label=False))[0], 0)
    rc, out = run(clean + card("stale", 8))
    check("the refusal names the offending card", 0 if "stale" in out and "8.0 days" in out else 1, 0)

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All freshness-gate tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
