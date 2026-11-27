#!/usr/bin/env bash
# push-content.sh against a throwaway origin. No network, no credentials.
#
# The case this file exists for (2026-11-25): GitHub answered a push with HTTP
# 500. push-content.sh had already committed, left the commit in place "so the
# next cycle retries it" — and then every later cycle refused to push it,
# because the unreviewed-commit guard counted the curator's own stranded
# content commit as somebody else's work. Production froze for ~42 hours,
# eight cycles, each one reporting refused_local_commits.
#
# The guard must still refuse everything it was written to refuse:
#   - any commit touching a path outside the content directory
#   - a content-only commit by anyone other than the curator
#   - a curator-authored commit that also touches code
#
# Usage: scripts/test-push-content.sh [path/to/push-content.sh]
set -uo pipefail

SCRIPT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/push-content.sh}"
FAILS=0
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

ok()   { printf '  PASS  %s\n' "$1"; }
bad()  { printf '  FAIL  %s\n' "$1"; FAILS=$((FAILS+1)); }
want() { [ "$2" = "$3" ] && ok "$1" || bad "$1 (got $2, want $3)"; }

# A fresh origin with one commit, and a work clone wired like the homelab.
setup() {
  rm -rf "$TMP/origin.git" "$TMP/work"
  git init -q --bare -b main "$TMP/origin.git"
  git init -q -b main "$TMP/work"
  cd "$TMP/work" || exit 1
  git config user.name "owner"; git config user.email "owner@example.test"
  git config --local credential.helper "store --file=$TMP/none"
  mkdir -p scripts site/src/content/posts
  cp "$SCRIPT" scripts/push-content.sh
  echo seed > site/src/content/posts/seed.md; echo code > app.py
  git add -A; git commit -qm seed
  git remote add origin "$TMP/origin.git"; git push -q origin main
}
curator_commit() {  # a content commit exactly as push-content.sh makes one
  git -c user.name="signal.log curator" -c user.email="curator@gs-bm.com" \
    commit -qm "content: +1 ~0 -0 (test)"
}
run()    { scripts/push-content.sh >"$TMP/log" 2>&1; echo $?; }
remote() { git --git-dir="$TMP/origin.git" rev-parse main; }

echo "-- the 2026-11-25 failure: push fails, next cycle must retry --"
setup
echo a > site/src/content/posts/a.md
git remote set-url origin "$TMP/nowhere.git"          # GitHub's 500
want "a failed push exits 1" "$(run)" 1
want "  ... and leaves its commit on HEAD" "$(git log -1 --format=%ae)" curator@gs-bm.com
git remote set-url origin "$TMP/origin.git"            # GitHub is back
echo b > site/src/content/posts/b.md
want "the next cycle pushes the stranded commit with its own" "$(run)" 0
want "  ... origin now holds both" "$(remote)" "$(git rev-parse HEAD)"
want "  ... the stranded one included" "$(git --git-dir="$TMP/origin.git" log --format=%s main | grep -c '^content:')" 2

echo "-- stranded commit, nothing new this cycle --"
setup
echo a > site/src/content/posts/a.md; git add -A; curator_commit
want "a stranded commit alone is still pushed (not 'nothing to push')" "$(run)" 0
want "  ... origin has it" "$(remote)" "$(git rev-parse HEAD)"

echo "-- what the guard exists to refuse --"
setup
echo x >> app.py; git commit -qam "fix: something"
echo a > site/src/content/posts/a.md
want "an owner's code commit is refused" "$(run)" 11
want "  ... nothing reached origin" "$(remote)" "$(git rev-parse HEAD~1)"
grep -q "fix: something" "$TMP/log" && ok "  ... and the refusal names it" || bad "  ... and the refusal names it"

setup
echo hand > site/src/content/posts/hand.md; git add -A; git commit -qm "content: hand edit"
want "a content-only commit by someone else is refused" "$(run)" 11

setup
echo a > site/src/content/posts/a.md; echo x >> app.py; git add -A; curator_commit
want "a curator-authored commit that also touches code is refused" "$(run)" 11

setup
echo a > site/src/content/posts/a.md; git add -A; curator_commit
echo x >> app.py; git commit -qam "feat: unrelated"
want "a stranded content commit under a foreign one is refused" "$(run)" 11
grep -q "feat: unrelated" "$TMP/log" && ! grep -q "         .*content: +1" "$TMP/log" \
  && ok "  ... the refusal lists the foreign commit, not the curator's" \
  || bad "  ... the refusal lists the foreign commit, not the curator's"

setup
echo x >> app.py; git commit -qam "feat: deliberate"
echo a > site/src/content/posts/a.md
want "PUSH_LOCAL_COMMITS=1 still ships a foreign commit deliberately" \
  "$(PUSH_LOCAL_COMMITS=1 scripts/push-content.sh >"$TMP/log" 2>&1; echo $?)" 0

echo "-- unchanged behaviour --"
setup
want "nothing staged, nothing stranded: exit 10" "$(run)" 10

echo
[ "$FAILS" -eq 0 ] && { echo "All push-content tests passed."; exit 0; }
echo "FAILED: $FAILS"; exit 1
