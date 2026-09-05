#!/usr/bin/env bash
# Pushes curated Markdown to GitHub. CONTENT ONLY — never dist/.
#
# GitHub Actions builds and deploys; this script's job ends at `git push`.
# Pushing built HTML would make the homelab a single point of failure for the
# published artifact and remove the only reproducible build in the system.
#
# CREDENTIALS: this script never handles the token. Authentication is the
# credential helper's job, configured once as a local repo setting:
#
#   git config --local credential.helper \
#       'store --file=/home/nikita/.config/signal-log/git-credentials'
#
# Only that path is written to .git/config. The token is never embedded in the
# remote URL (which would leak it through `git remote -v` and any diagnostic
# dump) and never passed as an argument (visible in `ps` to every process).
#
# Exit codes:  0 pushed   10 nothing to push   1 push failed
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

GIT_BIN="$(command -v git || true)"
[ -x "$GIT_BIN" ] || { log "FATAL: git not found on PATH"; exit 1; }

GH_BRANCH="$(env_get GITHUB_BRANCH)"; GH_BRANCH="${GH_BRANCH:-main}"
CONTENT_PATH="site/src/content/posts"

"$GIT_BIN" remote get-url origin >/dev/null 2>&1 || {
  log "FATAL: no 'origin' remote configured"; exit 1; }

if ! "$GIT_BIN" config --local --get credential.helper >/dev/null 2>&1; then
  log "FATAL: no local credential.helper configured — refusing to push."
  log "       Set one so the token never enters .git/config or argv:"
  log "       git config --local credential.helper 'store --file=<path>'"
  exit 1
fi

# No empty commits. An unconditional 6-hourly commit turns both the git history
# and the Actions log into noise inside a week, and triggers a pointless deploy.
"$GIT_BIN" add -- "$CONTENT_PATH"
if "$GIT_BIN" diff --cached --quiet -- "$CONTENT_PATH"; then
  log "no content changes — nothing to push"
  exit 10
fi

STAT="$("$GIT_BIN" diff --cached --name-status -- "$CONTENT_PATH")"
ADDED=$(printf '%s\n'   "$STAT" | grep -c '^A' || true)
DELETED=$(printf '%s\n' "$STAT" | grep -c '^D' || true)
MODIFIED=$(printf '%s\n' "$STAT" | grep -c '^M' || true)
log "staged: +${ADDED} ~${MODIFIED} -${DELETED}"

"$GIT_BIN" -c user.name="signal.log curator" \
           -c user.email="curator@gs-bm.com" \
           commit -q -m "content: +${ADDED} ~${MODIFIED} -${DELETED} ($(date -u '+%Y-%m-%d %H:%M UTC'))" \
  || { log "FATAL: commit failed"; exit 1; }

# Push by remote NAME. The helper supplies credentials; nothing secret is in
# this command line, this script, or the repo config.
if "$GIT_BIN" push --quiet origin "HEAD:${GH_BRANCH}"; then
  log "pushed to origin/${GH_BRANCH} — GitHub Actions will build and deploy"
  exit 0
fi

log "FATAL: push to origin/${GH_BRANCH} failed"
# Leave the commit in place so the next cycle retries it rather than losing it.
exit 1
