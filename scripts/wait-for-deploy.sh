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
# Exit:  0 success   1 workflow failed   2 timed out   10 cannot check
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
SHA="${1:-}"
[ -n "$SHA" ] || { echo "usage: $0 <commit-sha>"; exit 10; }

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

GH_REPO="$(env_get GITHUB_REPO)"; GH_REPO="${GH_REPO:-gsbm369/signal-log}"
CRED_FILE="$(git config --local --get credential.helper 2>/dev/null | sed -n 's/.*--file=\([^ ]*\).*/\1/p')"
TIMEOUT="${DEPLOY_TIMEOUT:-900}"
INTERVAL="${DEPLOY_POLL_INTERVAL:-20}"

[ -n "$CRED_FILE" ] && [ -r "$CRED_FILE" ] || {
  log "no readable credential file — cannot verify the deploy"; exit 10; }

log "waiting for the Actions run on ${SHA:0:8} (timeout ${TIMEOUT}s)"

GH_REPO="$GH_REPO" SHA="$SHA" CRED_FILE="$CRED_FILE" \
TIMEOUT="$TIMEOUT" INTERVAL="$INTERVAL" python3 <<'PY'
import json, os, re, sys, time, urllib.error, urllib.request

repo     = os.environ["GH_REPO"]
sha      = os.environ["SHA"]
timeout  = float(os.environ["TIMEOUT"])
interval = float(os.environ["INTERVAL"])

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
        f"https://api.github.com/repos/{repo}/actions/runs?head_sha={sha}&per_page=5",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "signal-log-curator",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        runs = json.load(resp).get("workflow_runs", [])
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
        status, conclusion, url = "pending", None, "-"
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
