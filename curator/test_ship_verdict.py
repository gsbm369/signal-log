#!/usr/bin/env python3
"""The cycle verdict ship_to_loki.py records — the field every alert reads.

  - a cycle that reached ZERO feeds is "failed", whatever else happened. The
    2026-09-18 18:15 cycle (0/33 feeds, build ok, nothing to push, exit 0) was
    recorded "degraded", which no rule alerts on.
  - a cycle that never reached the curator must not ship the PREVIOUS cycle's
    metrics.json. A no_network cycle was recorded curator_status "ok".
  - a healthy cycle is still "ok": a rule that fails everything looks the same
    as one that works.

Loki is pointed at a closed port; the record is read from the METRIC line.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAILURES: list[str] = []


def ship(metrics: dict, age_s: float = 0, *, build="ok", push="ok", deploy="ok",
         exit_code=0, duration=90.0) -> dict:
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "metrics.json"
        f.write_text(json.dumps(metrics))
        if age_s:
            t = time.time() - age_s
            os.utime(f, (t, t))
        env = dict(os.environ, STATE_DIR=td, LOKI_URL="http://127.0.0.1:9", CYCLE_TRIGGER="test")
        r = subprocess.run([sys.executable, str(HERE / "ship_to_loki.py"),
                            "--build-status", build, "--publish-status", "ok",
                            "--push-status", push, "--deploy-status", deploy,
                            "--exit-code", str(exit_code), "--duration", str(duration)],
                           env=env, capture_output=True, text=True, timeout=60)
        line = next((l for l in r.stdout.splitlines() if l.startswith("METRIC ")), None)
        return json.loads(line[7:]) if line else {"_stdout": r.stdout + r.stderr}


def check(name, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}  (got {got!r})")
    if not ok:
        FAILURES.append(name)


def main() -> int:
    healthy = {"curator_status": "ok", "feeds_ok": 47, "feeds_failed": 0}
    zero = {"curator_status": "no_articles", "feeds_ok": 0, "feeds_failed": 33,
            "error": "all feeds empty or unreachable"}

    check("a healthy cycle is ok", ship(healthy).get("cycle_status"), "ok")
    check("the 2026-09-18 18:15 cycle (0 feeds, nothing to push, exit 0) is failed",
          ship(zero, push="nothing_to_push", deploy="not_needed").get("cycle_status"), "failed")
    check("0 feeds is failed even when push and deploy succeeded",
          ship(zero).get("cycle_status"), "failed")
    r = ship({"curator_status": "ok", "feeds_ok": 0})
    check("0 feeds is failed even when the curator said ok", r.get("cycle_status"), "failed")
    r = ship(healthy, age_s=3600, build="no_network", push="not_run", deploy="not_run",
             exit_code=1, duration=15)
    check("a cycle that never reached the curator does not ship the last cycle's status",
          r.get("curator_status"), "not_run")
    check("  ... nor its feed count", r.get("feeds_ok"), 0)
    for st in ("never_triggered", "bad_sha"):
        check(f"deploy_status {st} (content pushed, no build ran) is publish_failed",
              ship(healthy, deploy=st, exit_code=1).get("cycle_status"), "publish_failed")
    check("a metrics.json written during this cycle is used",
          ship(healthy, age_s=30, duration=90).get("curator_status"), "ok")

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All verdict tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
