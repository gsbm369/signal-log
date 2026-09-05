#!/usr/bin/env bash
# Cron entrypoint for one publish cycle.
#
# Owns the lock itself rather than being wrapped in `flock -n`, so that an
# overlapping run is *recorded* as a skipped cycle instead of vanishing silently.
# Binary paths are resolved, not assumed: DOCKER_BIN/FLOCK_BIN from .env if the
# deploy wrote them, otherwise looked up on PATH.
set -uo pipefail

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }

# Read only the observability settings — not the whole .env, so the API key
# never enters this shell's environment.
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

# The container reaches Loki by container name; this script runs on the HOST,
# where that name does not resolve. Prefer the host-reachable URL when set.
LOKI_URL="$(env_get LOKI_URL_HOST)"
[ -z "$LOKI_URL" ] && LOKI_URL="$(env_get LOKI_URL)"
LOKI_JOB="$(env_get LOKI_JOB)"; LOKI_JOB="${LOKI_JOB:-signal-log}"
LOKI_HOST_LABEL="$(env_get LOKI_HOST_LABEL)"; LOKI_HOST_LABEL="${LOKI_HOST_LABEL:-$(hostname)}"
LOCK_FILE="$(env_get LOCK_FILE)"; LOCK_FILE="${LOCK_FILE:-/tmp/aiblog-cycle.lock}"

DOCKER_BIN="$(env_get DOCKER_BIN)"; DOCKER_BIN="${DOCKER_BIN:-$(command -v docker || true)}"
FLOCK_BIN="$(env_get FLOCK_BIN)";  FLOCK_BIN="${FLOCK_BIN:-$(command -v flock || true)}"

for b in DOCKER_BIN FLOCK_BIN; do
  if [ -z "${!b}" ] || [ ! -x "${!b}" ]; then
    log "FATAL: ${b} could not be resolved (looked on PATH and in .env)"
    exit 127
  fi
done

# Ship a one-off record for outcomes that never reach the container.
ship_skip() {
  local reason="$1"
  local line
  line=$(printf '{"ts":"%s","event":"publish_cycle","cycle_status":"skipped","curator_status":"not_run","build_status":"not_run","publish_status":"not_run","exit_code":0,"reason":"%s"}' \
    "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$reason")
  log "METRIC ${line}"
  [ -z "$LOKI_URL" ] && { log "loki push: disabled (LOKI_URL unset)"; return 0; }
  local payload
  payload=$(printf '{"streams":[{"stream":{"job":"%s","service":"curator","host":"%s","level":"warn","status":"skipped"},"values":[["%s",%s]]}]}' \
    "$LOKI_JOB" "$LOKI_HOST_LABEL" "$(date +%s)000000000" "$(printf '%s' "$line" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")
  local code
  code=$(printf '%s' "$payload" | curl -s -o /dev/null -w '%{http_code}' -m 5 \
    -X POST -H 'Content-Type: application/json' --data-binary @- \
    "${LOKI_URL%/}/loki/api/v1/push" 2>/dev/null)
  case "${code:-000}" in
    2*) log "loki push: ok (HTTP ${code})" ;;
    *)  log "loki push: FAILED (HTTP ${code:-000} to ${LOKI_URL}) — record above is still in this log" ;;
  esac
}

exec 9>"$LOCK_FILE" || { log "FATAL: cannot open lock file ${LOCK_FILE}"; exit 1; }
if ! "$FLOCK_BIN" -n 9; then
  log "=== cycle skipped: a previous run still holds ${LOCK_FILE} ==="
  ship_skip "overlapping_run_lock_held"
  exit 0
fi

log "=== cron cycle starting (docker=${DOCKER_BIN} flock=${FLOCK_BIN}) ==="
"$DOCKER_BIN" compose --project-directory "$ROOT" run --rm builder
rc=$?
log "=== cron cycle exited ${rc} ==="
exit "$rc"
