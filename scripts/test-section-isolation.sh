#!/usr/bin/env bash
# Deleting every post of one category must leave every OTHER section's rendered
# HTML byte-identical. The policy says never borrow across categories — an empty
# slot stays empty — and this is the test that proves it on the real build.
#
#   scripts/test-section-isolation.sh <category>
#
# Builds twice with the same frozen clock: once with the live posts, once with
# <category> removed, then diffs each other <section data-section=…> block.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAT="${1:?category to delete}"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
CLOCK="${CYCLE_START_UTC:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"

build() {  # build <posts-dir> <out-dir>
  mkdir -p "$2"
  docker run --rm -e CYCLE_START_UTC="$CLOCK" \
    -v "$ROOT/site/src:/app/site/src" -v "$1:/app/site/src/content/posts" -v "$2:/dist" \
    -w /app/site --entrypoint sh aiblog-builder:latest \
    -c 'npm run build >/tmp/b.log 2>&1 || { tail -5 /tmp/b.log; exit 1; }; cp -r /app/site/dist/. /dist/'
}

cp -r "$ROOT/site/src/content/posts" "$WORK/full"
cp -r "$ROOT/site/src/content/posts" "$WORK/cut"
REMOVED=$(grep -l "^category: ${CAT}\$" "$WORK/cut"/*.md 2>/dev/null | wc -l)
grep -l "^category: ${CAT}\$" "$WORK/cut"/*.md 2>/dev/null | xargs -r rm -f
build "$WORK/full" "$WORK/a" && build "$WORK/cut" "$WORK/b" || { echo "build failed"; exit 2; }

python3 - "$WORK/a/index.html" "$WORK/b/index.html" "$CAT" "$REMOVED" <<'PY'
import re, sys
a, b, cat, removed = open(sys.argv[1]).read(), open(sys.argv[2]).read(), sys.argv[3], sys.argv[4]
sec = lambda h: dict(re.findall(r'<section[^>]*data-section="([a-z_]+)"[^>]*>(.*?)</section>', h, re.S))
fold = lambda h: set(re.findall(r'<article\b[^>]*data-cat="([a-z_]+)"[^>]*data-section="fold"', h))
sa, sb = sec(a), sec(b)
print(f"\n-- deleted {removed} {cat} post(s); fold categories before: {sorted(fold(a))} after: {sorted(fold(b))}")
bad = 0
for k in sorted(sa):
    if k == cat:
        print(f"   {k:<15} (the deleted category) -> {'empty-state line' if 'no new posts this week' in sb.get(k,'') else 'NOT empty-state'}")
        continue
    same = sa[k] == sb.get(k)
    bad += not same
    print(f"   {k:<15} {'byte-identical' if same else 'CHANGED'}")
# The property the policy actually states: never borrow across categories.
# Checked separately from byte-identity, because a section can change for a
# DIFFERENT reason — the fold — without borrowing anything.
borrowed = 0
for h, label in ((a, "before"), (b, "after")):
    for k, body in sec(h).items():
        cats = set(re.findall(r'<article\b[^>]*data-cat="([a-z_]+)"', body))
        n = len(re.findall(r"<article\b", body))
        if cats - {k}:
            borrowed += 1
            print(f"   BORROW: section {k} ({label}) holds {sorted(cats - {k})}")
        if n > 6:
            borrowed += 1
            print(f"   OVER QUOTA: section {k} ({label}) has {n} cards")
print(f"\n   no-borrow + quota: {'PASS' if not borrowed else 'FAIL'} "
      f"(every section holds only its own category, at most 6 cards, before and after)")
for k in sorted(sa):
    if k != cat and sa[k] != sb.get(k):
        ga = re.findall(r'href="/posts/([^"/]+)', sa[k]); gb = re.findall(r'href="/posts/([^"/]+)', sb.get(k, ""))
        print(f"\n   why {k} changed:")
        for x in ga:
            if x not in gb: print(f"     - left the section : {x[:60]}")
        for x in gb:
            if x not in ga: print(f"     + entered          : {x[:60]}")
        moved = [x for x in ga if x not in gb and f'/posts/{x}/' in b and 'data-section="fold"' in b.split(f'/posts/{x}/')[0][-600:]]
        for x in moved: print(f"     (it went to the fold: {x[:50]})")
print(f"\n   byte-identity: {'PASS' if not bad else 'FAIL'}: {len(sa)-1-bad} of {len(sa)-1} other sections unchanged")
sys.exit(1 if (bad or borrowed) else 0)
PY
