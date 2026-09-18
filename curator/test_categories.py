#!/usr/bin/env python3
"""The curator's category list and the site's schema enum must not drift.

Widening the enum without this test only moves the trap. The enum is CLOSED and
it fails the Astro build, which means a category added on the curator side and
forgotten on the site side does not degrade gracefully — it stops the site
building, on a timer, hours later, from a file nobody was editing that day. The
symptom appears nowhere near the change.

This is the same shape as the other silent controls this project keeps finding:
the failure is invisible at the point of the edit and expensive at the point of
discovery. So the two lists get compared explicitly, in a test that runs before
the build.

Checked in BOTH directions, and against the feeds themselves — a feed pointed at
a category the scoring block never declares would silently inherit the
news-shaped POLICY_DEFAULTS, which is the quiet half of the same bug.

No network, no model, no API key.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
FEEDS_FILE = Path(__import__("os").environ.get("FEEDS_FILE", HERE / "feeds.yml"))
CATEGORIES_TS = HERE.parent / "site/src/categories.ts"

FAILURES: list[str] = []


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}\n          got : {got}\n          want: {want}")


def ts_list(source: str, name: str) -> set[str]:
    """Pull a `export const NAME = [ 'a', 'b' ]` array out of the TypeScript.

    Deliberately a regex and not a parser: the alternative is running node from
    a Python test to read one array, and this file is the only thing that would
    ever need it. If the shape of categories.ts changes, this test fails loudly
    with an empty set rather than silently passing — which is the correct
    failure direction for a drift test.
    """
    m = re.search(rf"export const {name}\s*=\s*\[(.*?)\]", source, re.S)
    if not m:
        return set()
    return set(re.findall(r"['\"]([A-Za-z0-9_]+)['\"]", m.group(1)))


def main() -> int:
    cfg = yaml.safe_load(FEEDS_FILE.read_text()) or {}
    declared = set((cfg.get("scoring") or {}).get("categories") or {})
    used = {str(f.get("category")) for f in (cfg.get("feeds") or []) if f.get("category")}

    ts_src = CATEGORIES_TS.read_text()
    site = ts_list(ts_src, "CATEGORIES")
    legacy = ts_list(ts_src, "LEGACY_CATEGORIES")
    default_m = re.search(r"DEFAULT_CATEGORY\s*:\s*Category\s*=\s*['\"]([A-Za-z0-9_]+)['\"]", ts_src)
    default = default_m.group(1) if default_m else "<unparseable>"

    print(f"\n-- {FEEDS_FILE} vs {CATEGORIES_TS.name} --")
    print(f"     curator scoring.categories : {sorted(declared)}")
    print(f"     categories used by feeds   : {sorted(used)}")
    print(f"     site CATEGORIES            : {sorted(site)}")
    print(f"     site LEGACY_CATEGORIES     : {sorted(legacy)}  (ignored by the contract)")
    print(f"     site DEFAULT_CATEGORY      : {default}\n")

    check("site enum is not empty (categories.ts still parseable)", bool(site), True)
    check("every curator category exists in the site enum", sorted(declared - site), [])
    check("every site category exists in the curator config", sorted(site - declared), [])
    check("every feed's category is declared in the scoring block", sorted(used - declared), [])
    check("DEFAULT_CATEGORY is one of the site categories", default in site, True)
    # Legacy exists only so posts already on disk still build. If one of them
    # reappears in the curator config it is live again, not legacy, and leaving
    # it in both lists would exempt it from every check above.
    check("no category is both live and legacy", sorted(site & legacy), [])

    # The global cap must never be the thing that evicts. The per-category
    # ceiling decides what each category keeps; if max_posts is smaller than
    # ceiling x categories, the global cap prunes oldest-added across the
    # whole site and a QUIET category loses posts to make room for BUSY ones.
    # Measured 2026-09-18: 9 categories x 10 against max_posts 60 cut
    # devops_linux from 6 to 4 while four categories sat at their ceiling.
    # Asserted as a relationship, so adding a tenth category fails here, not
    # in production.
    cur = (HERE / "curate.py").read_text()
    cm = re.search(r'CATEGORY_CEILING\s*=\s*int\(os\.environ\.get\("CATEGORY_CEILING",\s*"(\d+)"\)\)', cur)
    ceiling = int(__import__("os").environ.get("CATEGORY_CEILING", cm.group(1) if cm else "0"))
    max_posts = int(((cfg.get("settings") or {}).get("max_posts")) or 0)
    print(f"     max_posts {max_posts} vs ceiling {ceiling} x {len(declared)} categories = {ceiling * len(declared)}")
    check("CATEGORY_CEILING is readable from curate.py", ceiling > 0, True)
    check("max_posts >= ceiling x categories (the global cap never evicts)",
          max_posts >= ceiling * len(declared), True)

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        print("The curator and the site disagree about which categories exist.")
        print("Fix ansible/deploy.yml (scoring_categories + blog_feeds), re-run the")
        print("playbook, then update site/src/categories.ts to match.")
        return 1
    print("Category lists agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
