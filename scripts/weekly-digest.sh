#!/usr/bin/env bash
# Sunday entry point for the weekly digest. Runs on the HOST, because that is
# where Postfix listens — the same relay the rest of the homelab already uses.
#
# It reuses the ranker's published output (post front matter) rather than
# re-ranking, and reports a send failure to Loki rather than swallowing it.
set -uo pipefail

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

# Only the settings the digest needs; the API token is never read here.
# Caller-supplied environment WINS over .env — otherwise an override passed on
# the command line is silently discarded, which is how a failure-path test
# quietly became a real send.
for k in LOKI_URL_HOST LOKI_URL LOKI_JOB LOKI_HOST_LABEL DIGEST_TO DIGEST_FROM \
         DIGEST_SMTP_HOST DIGEST_SMTP_PORT DIGEST_COUNT DIGEST_DAYS; do
  [ -n "${!k:-}" ] && continue          # already set by the caller
  v="$(env_get "$k")"; [ -n "$v" ] && export "$k=$v"
done

LOCK="${ROOT}/curator/state/.digest.lock"
exec 8>"$LOCK" || { log "FATAL: cannot open ${LOCK}"; exit 1; }
if ! flock -n 8; then log "digest already running — skipping"; exit 0; fi

log "=== weekly digest ==="
python3 "${ROOT}/curator/weekly_digest.py" "$@"
rc=$?
log "=== digest exited ${rc} ==="
exit "$rc"
