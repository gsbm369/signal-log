#!/usr/bin/env python3
"""check_selection.py must refuse a page whose IDs are right but whose RENDERED
cards are wrong.

The IDs-only version passed every one of these: QA planted an unlabelled
"this week" card and a changed source on a fold card, and it exited 0. Each
fixture below is the clean page with one defect planted, so a pass cannot come
from one fixture masking another — and the clean page must pass, because a
gate that refuses everything looks identical to one that works.
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

#        id    category  source  age_h  score
POSTS = [("f1", "gaming", "A", 2, 5.0), ("f2", "gaming", "B", 3, 4.0),
         ("f3", "gaming", "C", 4, 3.0), ("f4", "gaming", "D", 5, 2.0),
         ("f5", "gaming", "E", 6, 1.0),
         ("g1", "gaming", "F", 48, 0.9), ("g2", "gaming", "G", 60, 0.8),
         ("g3", "gaming", "H", 72, 0.7)]


def card(pid, section, src, week, label=None):
    lab = week if label is None else label
    return (f'<article class="row" data-cat="gaming" data-section="{section}">'
            f'<a href="/posts/{pid}/"></a><span class="src">{src}</span>'
            + ('<span class="chip chip--week" data-label="this-week">this week</span>' if lab else "")
            + "</article>")


def page(overrides=None):
    """The clean page, with per-card overrides {id: dict(src=..., label=...)}."""
    o = overrides or {}
    fold = "".join(card(p, "fold", o.get(p, {}).get("src", s), a > 24, o.get(p, {}).get("label"))
                   for p, _, s, a, _ in POSTS[:5])
    sec = "".join(card(p, "gaming", o.get(p, {}).get("src", s), a > 24, o.get(p, {}).get("label"))
                  for p, _, s, a, _ in POSTS[5:])
    return f'<html><body>{fold}<section id="gaming" data-section="gaming">{sec}</section></body></html>'


def run(html: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as td:
        posts = Path(td) / "posts"
        posts.mkdir()
        for pid, cat, src, age, score in POSTS:
            pub = (NOW - timedelta(hours=age)).isoformat()
            (posts / f"{pid}.md").write_text(
                f'---\ntitle: "{pid}"\npubDate: {pub}\nsource: "{src}"\ncategory: {cat}\n'
                f"score: {score}\n---\n")
        idx = Path(td) / "index.html"
        idx.write_text(html)
        env = dict(os.environ, CONTENT_DIR=str(posts), BUILT_INDEX=str(idx),
                   CYCLE_START_UTC=NOW.isoformat())
        r = subprocess.run([sys.executable, str(HERE / "check_selection.py")],
                           env=env, capture_output=True, text=True)
        return r.returncode, r.stdout


def check(name, rc, want, out=""):
    ok = rc == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}  (exit {rc})")
    if not ok:
        FAILURES.append(name)
        print("\n".join("        " + l for l in out.strip().splitlines()[-6:]))


def main() -> int:
    rc, out = run(page())
    check("the clean page passes", rc, 0, out)
    rc, out = run(page({"g1": {"label": False}}))
    check("a 'this week' card with no visible label is refused", rc, 1, out)
    rc, out = run(page({"f2": {"src": "A"}}))
    check("a fold card rendering another fold card's source is refused", rc, 1, out)
    check("  ... named as a repeated fold source", 0 if "distinct rendered sources" in out else 1, 0)
    rc, out = run(page({"f2": {"src": "Planted Source"}}))
    check("a fold card rendering a source that is not its post's is refused", rc, 1, out)
    rc, out = run(page({"g2": {"src": "F"}, "g3": {"src": "F"}}))
    check("a section rendering 3 cards from one source is refused", rc, 1, out)
    check("  ... named as over the per-source limit", 0 if "limit 2" in out else 1, 0)

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All selection-gate tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
