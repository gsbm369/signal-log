#!/usr/bin/env bash
# Polls the GitHub Actions run for a pushed commit until it concludes.
#
# Without this, a successful `git push` looks like a successful publish even
# when the workflow then fails and nothing reaches production.
#
# CREDENTIALS: the token is read from the git credential file INSIDE a python
# process and used from memory. It is never passed as a curl argument — argv is
# world-readable through `ps` for the lifetime of the command.
#
# Usage: wait-for-deploy.sh <commit-sha>
# Exit:  0 success   1 workflow failed
#        2 timed out — a run EXISTS but did not conclude within the deadline
#        3 no run expected (commit touches no deploy-triggering path)
#        4 not a commit — the argument does not resolve; nothing is polled
#        5 no workflow run exists for the commit after the grace period —
#          the workflow never triggered. Not a failed deploy and not a
#          timeout: nothing ran at all.
#        10 cannot check
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
SHA="${1:-}"
[ -n "$SHA" ] || { echo "usage: $0 <commit-sha>"; exit 10; }

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }

# The Actions API's head_sha filter matches the FULL hash only. A short hash
# returns zero runs, and zero runs used to read as "pending" for 900s and then
# as a failed deploy. Resolve the argument before anything else, and refuse
# what does not resolve instead of polling for it.
FULL_SHA="$(git -C "$ROOT" rev-parse --verify --quiet "${SHA}^{commit}")" || {
  log "not a commit: ${SHA}"; exit 4; }
SHA="$FULL_SHA"
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

GH_REPO="$(env_get GITHUB_REPO)"; GH_REPO="${GH_REPO:-gsbm369/signal-log}"
CRED_FILE="$(git config --local --get credential.helper 2>/dev/null | sed -n 's/.*--file=\([^ ]*\).*/\1/p')"
TIMEOUT="${DEPLOY_TIMEOUT:-900}"
INTERVAL="${DEPLOY_POLL_INTERVAL:-20}"
# How long a pushed commit may have NO run at all before we conclude the
# workflow never triggered. GitHub normally registers a run within seconds.
GRACE="${DEPLOY_NO_RUN_GRACE:-120}"

[ -n "$CRED_FILE" ] && [ -r "$CRED_FILE" ] || {
  log "no readable credential file — cannot verify the deploy"; exit 10; }

# The workflow only triggers on paths: site/** and the workflow file itself.
# A commit that touches neither produces no run, and waiting 900s for one that
# was never going to exist reports a false publish failure. Distinguish "no run
# needed" from "run never appeared" before polling.
WATCHED_RE="${DEPLOY_WATCHED_PATHS:-^(site/|\.github/workflows/)}"
if git -C "$ROOT" rev-parse --verify "${SHA}^" >/dev/null 2>&1; then
  CHANGED="$(git -C "$ROOT" diff --name-only "${SHA}^" "$SHA" 2>/dev/null || true)"
  if [ -n "$CHANGED" ] && ! printf '%s\n' "$CHANGED" | grep -qE "$WATCHED_RE"; then
    log "commit ${SHA:0:8} touches no deploy-triggering path — no Actions run expected"
    log "  changed: $(printf '%s' "$CHANGED" | tr '\n' ' ' | cut -c1-160)"
    exit 3
  fi
fi

log "waiting for the Actions run on ${SHA:0:8} (timeout ${TIMEOUT}s)"

GH_REPO="$GH_REPO" SHA="$SHA" CRED_FILE="$CRED_FILE" \
TIMEOUT="$TIMEOUT" INTERVAL="$INTERVAL" GRACE="$GRACE" python3 <<'PY'
import json, os, re, sys, time, urllib.error, urllib.request

repo     = os.environ["GH_REPO"]
sha      = os.environ["SHA"]
timeout  = float(os.environ["TIMEOUT"])
interval = float(os.environ["INTERVAL"])
grace    = float(os.environ["GRACE"])
WORKFLOW = ".github/workflows/deploy.yml"

# Read the token from the credential store; never touches argv or the environment
# of any child process.
token = ""
try:
    with open(os.environ["CRED_FILE"]) as fh:
        for line in fh:
            m = re.match(r"https://[^:]+:([^@]+)@github\.com", line.strip())
            if m:
                token = m.group(1)
                break
except OSError:
    pass

if not token:
    print("  could not read a token from the credential file", flush=True)
    sys.exit(10)


def stamp(msg):
    print(time.strftime("[%Y-%m-%d %H:%M:%S UTC] ", time.gmtime()) + msg, flush=True)


def latest_run():
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/actions/runs?head_sha={sha}&event=push&per_page=20",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "signal-log-curator",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        runs = json.load(resp).get("workflow_runs", [])
    # Only the DEPLOY workflow's run for this push answers the question. Other
    # runs share the head_sha — Dependabot's "Graph Update" was runs[0] for
    # 646a1cd, so its success was reported as the deploy's — and so will the
    # hourly scheduled rebuilds once they exist.
    runs = [r for r in runs if r.get("path") == WORKFLOW and r.get("event") == "push"]
    return runs[0] if runs else None


waited = 0.0
while waited < timeout:
    try:
        run = latest_run()
    except urllib.error.HTTPError as exc:
        stamp(f"could not read run status (HTTP {exc.code}) — treating as unverified")
        sys.exit(10)
    except (urllib.error.URLError, OSError) as exc:
        stamp(f"could not reach the GitHub API ({exc}) — treating as unverified")
        sys.exit(10)

    if run is None:
        # Zero runs is not "pending". Pending is a run that exists and has
        # not finished; this is the absence of a run, and after the grace
        # period it is its own answer.
        if waited >= grace:
            stamp(f"no workflow run exists for {sha[:12]} after {int(waited)}s — "
                  f"the workflow never triggered (paths filter, or a disabled workflow)")
            sys.exit(5)
        status, conclusion, url = "not yet registered", None, "-"
    else:
        status = run.get("status") or "unknown"
        conclusion = run.get("conclusion")
        url = run.get("html_url") or "-"

    if status == "completed":
        if conclusion == "success":
            stamp(f"deploy succeeded — {url}")
            sys.exit(0)
        stamp(f"FATAL: workflow concluded '{conclusion}' — {url}")
        sys.exit(1)

    time.sleep(interval)
    waited += interval
    if waited % 120 == 0:
        stamp(f"  still {status} after {int(waited)}s")

stamp(f"FATAL: workflow did not conclude within {int(timeout)}s")
sys.exit(2)
PY
