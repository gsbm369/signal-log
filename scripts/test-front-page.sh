#!/usr/bin/env bash
# The front page's selection rules, asserted on a REAL Astro build of a fixture
# whose correct answer is known in advance.
#
#   scripts/test-front-page.sh
#
# The fixture is shaped so that each rule changes the outcome — a rule that did
# not take would render a different page, not the same one:
#
#   company_eng   AWS has the four highest-scoring stories of the day. Without
#                 the one-per-source fold rule, AWS takes four fold slots.
#   today tier    only three distinct sources, so the fold MUST fill from
#                 "this week" to reach five.
#   devops_linux  exactly one fresh story, and it is in the fold. The section is
#                 empty and must say so truthfully: "Today's ... in the headlines
#                 above", never "No new posts this week."
#   fintech       only a stale (9-day) story: zero fresh -> "No new posts this week."
#
# Also runs curator/check_selection.py — the independent implementation — against
# the same build, so the page and the check are held to the same fixture.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
CLOCK="2026-09-18T12:00:00Z"
mkdir -p "$WORK/posts" "$WORK/dist"

python3 - "$WORK/posts" <<'PY'
import sys
from datetime import datetime, timedelta, timezone
out = sys.argv[1]
clock = datetime(2026, 9, 18, 12, tzinfo=timezone.utc)
#        id    category       source            age_h  score
rows = [("a1", "company_eng",  "AWS Architecture", 2,  5.0),
        ("a2", "company_eng",  "AWS Architecture", 3,  4.9),
        ("a3", "company_eng",  "AWS Architecture", 4,  4.8),
        ("a4", "company_eng",  "AWS Architecture", 5,  4.7),
        ("s1", "system_design", "InfoQ",           6,  4.0),
        ("s2", "system_design", "InfoQ",           7,  3.9),
        ("d1", "devops_linux", "LWN.net",          8,  3.5),
        ("f1", "fintech",      "Finextra",         9 * 24, 9.9),
        ("g1", "gaming",       "Polygon",          48, 9.0),
        ("j1", "deep_dives",   "jvns.ca",          72, 1.0)]
for pid, cat, src, age, score in rows:
    pub = (clock - timedelta(hours=age)).isoformat()
    open(f"{out}/{pid}.md", "w").write(
        f'---\ntitle: "fixture {pid}"\ndescription: "fixture {pid}"\npubDate: {pub}\n'
        f'addedAt: {pub}\nsource: "{src}"\ncategory: {cat}\nsourceUrl: "https://example.com/{pid}"\n'
        f'heat: 50\nscore: {score}\nreadMinutes: 1\n---\n\nfixture {pid}\n')
PY

docker run --rm -e CYCLE_START_UTC="$CLOCK" \
  -v "$ROOT/site/src:/app/site/src:ro" -v "$WORK/posts:/app/site/src/content/posts:ro" \
  -v "$WORK/dist:/dist" -w /app/site --entrypoint sh aiblog-builder:latest \
  -c 'npm run build >/tmp/b.log 2>&1 || { tail -15 /tmp/b.log; exit 1; }; cp -r /app/site/dist/. /dist/' \
  || { echo "build failed"; exit 2; }

python3 - "$WORK/dist/index.html" <<'PY'
import re, sys
from html import unescape
html = open(sys.argv[1], encoding="utf-8").read()
secs = dict(re.findall(r'<section[^>]*data-section="([a-z_]+)"[^>]*>(.*?)</section>', html, re.S))
fold = re.findall(r'<article\b[^>]*data-section="fold"[^>]*>.*?href="/posts/([^"/]+)/?"', html, re.S)
text = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()
fails = 0
def check(name, ok, detail=""):
    global fails
    fails += not ok
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"\n          {detail}" if detail and not ok else ""))

src = {"a": "AWS Architecture", "s": "InfoQ", "d": "LWN.net", "g": "Polygon", "j": "jvns.ca", "f": "Finextra"}
check("fold is exactly a1 s1 d1 g1 j1 (today by score, one per source, then week)",
      fold == ["a1", "s1", "d1", "g1", "j1"], f"rendered {fold}")
check("fold holds 5 distinct sources", len({src[p[0]] for p in fold}) == 5 == len(fold),
      f"sources {[src[p[0]] for p in fold]}")

dev = secs.get("devops_linux", "")
check("devops_linux (fresh, all in fold) says its stories are in the headlines above",
      "Today's DevOps & Linux stories are in the headlines above." in unescape(text(dev)), text(dev)[:160])
check("  ... and links to the fold", re.search(r'<a[^>]*href="#feed"', dev) is not None, text(dev)[:160])
check("  ... and does NOT claim there are no new posts", "No new posts this week." not in dev)

fin = secs.get("fintech", "")
check("fintech (zero fresh) says 'No new posts this week.'", "No new posts this week." in fin, text(fin)[:160])
check("  ... and does NOT point at the headlines", "headlines above" not in fin)

# The property, independent of which category the fixture happens to empty:
# a section may say "No new posts this week." only if none of its category's
# stories is in the fold.
fold_cats = set(re.findall(r'<article\b[^>]*data-cat="([a-z_]+)"[^>]*data-section="fold"', html))
liars = [k for k, body in secs.items() if "No new posts this week." in body and k in fold_cats]
check("no section says 'No new posts this week.' while its stories are in the fold",
      not liars, f"lying: {liars}")

gam = secs.get("gaming", "")
check("gaming (week story promoted by fill) does not claim it is today's",
      "Today's" not in unescape(gam) and "No new posts this week." not in gam and "headlines above" in gam, text(gam)[:160])
sys.exit(1 if fails else 0)
PY
RC=$?

echo
CONTENT_DIR="$WORK/posts" BUILT_INDEX="$WORK/dist/index.html" CYCLE_START_UTC="$CLOCK" \
  python3 "$ROOT/curator/check_selection.py" > "$WORK/check.out"
CHK=$?
tail -n 20 "$WORK/check.out"
echo "  check_selection.py exit $CHK on the fixture"

[ "$RC" -eq 0 ] && [ "$CHK" -eq 0 ] && { echo "front page: PASS"; exit 0; }
echo "front page: FAIL"; exit 1
