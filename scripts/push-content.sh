#!/usr/bin/env bash
# Pushes curated Markdown to GitHub. CONTENT ONLY — never dist/.
#
# GitHub Actions builds and deploys; this script's job ends at `git push`.
# Pushing built HTML would make the homelab a single point of failure for the
# published artifact and remove the only reproducible build in the system.
#
# Exit codes:  0 pushed   10 nothing to push   1 push failed
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }

env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

GIT_BIN="$(command -v git || true)"
[ -x "$GIT_BIN" ] || { log "FATAL: git not found on PATH"; exit 1; }

GH_REPO="$(env_get GITHUB_REPO)";     GH_REPO="${GH_REPO:-gsbm369/signal-log}"
GH_BRANCH="$(env_get GITHUB_BRANCH)"; GH_BRANCH="${GH_BRANCH:-main}"
GH_TOKEN="$(env_get GITHUB_TOKEN)"
CONTENT_PATH="site/src/content/posts"

if [ -z "$GH_TOKEN" ]; then
  log "GITHUB_TOKEN not set — skipping push (set it in .env to publish)"
  exit 10
fi

# No empty commits. An unconditional 6-hourly commit turns both the git history
# and the Actions log into noise inside a week, and triggers a pointless deploy.
"$GIT_BIN" add -- "$CONTENT_PATH"
if "$GIT_BIN" diff --cached --quiet -- "$CONTENT_PATH"; then
  log "no content changes — nothing to push"
  exit 10
fi

ADDED=$("$GIT_BIN" diff --cached --name-status -- "$CONTENT_PATH" | grep -c '^A' || true)
DELETED=$("$GIT_BIN" diff --cached --name-status -- "$CONTENT_PATH" | grep -c '^D' || true)
MODIFIED=$("$GIT_BIN" diff --cached --name-status -- "$CONTENT_PATH" | grep -c '^M' || true)
log "staged: +${ADDED} ~${MODIFIED} -${DELETED}"

"$GIT_BIN" -c user.name="signal.log curator" \
           -c user.email="curator@gs-bm.com" \
           commit -q -m "content: +${ADDED} ~${MODIFIED} -${DELETED} ($(date -u '+%Y-%m-%d %H:%M UTC'))" \
  || { log "FATAL: commit failed"; exit 1; }

# The token never reaches the remote URL stored on disk.
REMOTE="https://x-access-token:${GH_TOKEN}@github.com/${GH_REPO}.git"
if "$GIT_BIN" push --quiet "$REMOTE" "HEAD:${GH_BRANCH}" 2>&1 | sed "s|${GH_TOKEN}|***|g"; then
  log "pushed to ${GH_REPO}@${GH_BRANCH} — GitHub Actions will build and deploy"
  exit 0
fi

log "FATAL: push to ${GH_REPO} failed"
# Leave the commit in place so the next cycle retries it rather than losing it.
exit 1
