#!/usr/bin/env bash
# Polls the GitHub Actions run for a pushed commit until it concludes.
#
# Without this, a successful `git push` looks like a successful publish even
# when the workflow then fails and nothing reaches production.
#
# Usage: wait-for-deploy.sh <commit-sha>
# Exit:  0 success   1 workflow failed   2 timed out   10 cannot check
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
SHA="${1:-}"
[ -n "$SHA" ] || { echo "usage: $0 <commit-sha>"; exit 10; }

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

GH_REPO="$(env_get GITHUB_REPO)"; GH_REPO="${GH_REPO:-gsbm369/signal-log}"
GH_TOKEN="$(env_get GITHUB_TOKEN)"
TIMEOUT="${DEPLOY_TIMEOUT:-900}"
INTERVAL="${DEPLOY_POLL_INTERVAL:-20}"

[ -n "$GH_TOKEN" ] || { log "no GITHUB_TOKEN — cannot verify the deploy"; exit 10; }

api() {
  curl -sS -m 20 -H "Authorization: Bearer ${GH_TOKEN}" \
       -H "Accept: application/vnd.github+json" \
       -H "X-GitHub-Api-Version: 2022-11-28" "$1" 2>/dev/null
}

log "waiting for the Actions run on ${SHA:0:8} (timeout ${TIMEOUT}s)"
waited=0
while [ "$waited" -lt "$TIMEOUT" ]; do
  body="$(api "https://api.github.com/repos/${GH_REPO}/actions/runs?head_sha=${SHA}&per_page=5")"
  read -r status conclusion url <<<"$(printf '%s' "$body" | python3 -c '
import json, sys
try:
    runs = json.load(sys.stdin).get("workflow_runs", [])
except Exception:
    print("unknown unknown -"); raise SystemExit
if not runs:
    print("pending none -"); raise SystemExit
r = runs[0]
print(r.get("status") or "unknown", r.get("conclusion") or "none", r.get("html_url") or "-")
')"

  case "$status" in
    completed)
      if [ "$conclusion" = "success" ]; then
        log "deploy succeeded — ${url}"
        exit 0
      fi
      log "FATAL: workflow concluded '${conclusion}' — ${url}"
      exit 1
      ;;
    queued|in_progress|pending)
      : ;;
    *)
      log "could not read run status (got '${status}') — treating as unverified"
      exit 10
      ;;
  esac

  sleep "$INTERVAL"
  waited=$((waited + INTERVAL))
  [ $((waited % 120)) -eq 0 ] && log "  still ${status} after ${waited}s"
done

log "FATAL: workflow did not conclude within ${TIMEOUT}s"
exit 2
