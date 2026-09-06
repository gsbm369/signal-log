#!/usr/bin/env bash
# Production entry point for one publish cycle. Runs on the HOST.
#
#   1. take the lock (an overlapping run is recorded, not silently dropped)
#   2. run the builder container: curate -> rank -> summarise -> build ->
#      validate -> publish the local preview
#   3. push CONTENT to GitHub  (production is GitHub Pages, not this machine)
#   4. wait for the Actions run to conclude
#   5. ship exactly one record for the cycle to Loki
#
# The push and the deploy check live here rather than in the container because
# the git repo is on the host. A green container build is NOT a successful
# publish, and this script is what knows the difference.
set -uo pipefail

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"'\r'; }

LOKI_URL="$(env_get LOKI_URL_HOST)"; [ -z "$LOKI_URL" ] && LOKI_URL="$(env_get LOKI_URL)"
LOKI_JOB="$(env_get LOKI_JOB)"; LOKI_JOB="${LOKI_JOB:-signal-log}"
LOKI_HOST_LABEL="$(env_get LOKI_HOST_LABEL)"; LOKI_HOST_LABEL="${LOKI_HOST_LABEL:-$(hostname)}"
LOCK_FILE="$(env_get LOCK_FILE)"; LOCK_FILE="${LOCK_FILE:-/tmp/aiblog-cycle.lock}"
DOCKER_BIN="$(env_get DOCKER_BIN)"; DOCKER_BIN="${DOCKER_BIN:-$(command -v docker || true)}"
FLOCK_BIN="$(env_get FLOCK_BIN)";  FLOCK_BIN="${FLOCK_BIN:-$(command -v flock || true)}"
STATE_DIR="${ROOT}/curator/state"

for b in DOCKER_BIN FLOCK_BIN; do
  if [ -z "${!b}" ] || [ ! -x "${!b}" ]; then
    log "FATAL: ${b} could not be resolved (looked on PATH and in .env)"; exit 127
  fi
done

BUILD_STATUS="not_run"; PUBLISH_STATUS="not_run"
PUSH_STATUS="not_run";  DEPLOY_STATUS="not_run"
EXIT_CODE=0
CYCLE_START=$(date +%s)

ship() {
  local dur=$(( $(date +%s) - CYCLE_START ))
  STATE_DIR="$STATE_DIR" LOKI_URL="$LOKI_URL" LOKI_JOB="$LOKI_JOB" \
  LOKI_HOST_LABEL="$LOKI_HOST_LABEL" \
  CYCLE_TRIGGER="${CYCLE_TRIGGER:-$([ "${SKIP_PUSH:-0}" = "1" ] && echo test || echo cron)}" \
  python3 "${ROOT}/curator/ship_to_loki.py" \
    --build-status   "$BUILD_STATUS" \
    --publish-status "$PUBLISH_STATUS" \
    --push-status    "$PUSH_STATUS" \
    --deploy-status  "$DEPLOY_STATUS" \
    --exit-code      "$EXIT_CODE" \
    --duration       "$dur" || log "WARN: metric shipping failed"
  log "=== cycle finished: build=$BUILD_STATUS publish=$PUBLISH_STATUS push=$PUSH_STATUS deploy=$DEPLOY_STATUS exit=$EXIT_CODE in ${dur}s ==="
}

ship_skip() {
  local line payload code
  line=$(printf '{"ts":"%s","event":"publish_cycle","cycle_status":"skipped","curator_status":"not_run","build_status":"not_run","publish_status":"not_run","push_status":"not_run","deploy_status":"not_run","reached_production":true,"exit_code":0,"reason":"%s"}' \
    "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$1")
  log "METRIC ${line}"
  [ -z "$LOKI_URL" ] && { log "loki push: disabled"; return 0; }
  payload=$(printf '{"streams":[{"stream":{"job":"%s","service":"curator","host":"%s","level":"warn","status":"skipped"},"values":[["%s",%s]]}]}' \
    "$LOKI_JOB" "$LOKI_HOST_LABEL" "$(date +%s)000000000" \
    "$(printf '%s' "$line" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")
  code=$(printf '%s' "$payload" | curl -s -o /dev/null -w '%{http_code}' -m 5 \
    -X POST -H 'Content-Type: application/json' --data-binary @- \
    "${LOKI_URL%/}/loki/api/v1/push" 2>/dev/null)
  case "${code:-000}" in 2*) log "loki push: ok (HTTP ${code})";; *) log "loki push: FAILED (HTTP ${code:-000})";; esac
}

exec 9>"$LOCK_FILE" || { log "FATAL: cannot open ${LOCK_FILE}"; exit 1; }
if ! "$FLOCK_BIN" -n 9; then
  log "=== cycle skipped: a previous run still holds ${LOCK_FILE} ==="
  ship_skip "overlapping_run_lock_held"
  exit 0
fi
trap ship EXIT

# ------------------------------------------------------------------ 1. build
log "=== cycle starting (docker=${DOCKER_BIN}) ==="
"$DOCKER_BIN" compose --project-directory "$ROOT" run --rm builder
BUILD_RC=$?

if [ -s "${STATE_DIR}/build.json" ]; then
  read -r BUILD_STATUS PUBLISH_STATUS <<<"$(python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print(d.get("build_status","unknown"), d.get("publish_status","unknown"))
' "${STATE_DIR}/build.json")"
fi

if [ "$BUILD_RC" -ne 0 ] || [ "$PUBLISH_STATUS" != "ok" ]; then
  log "FATAL: build/publish failed (rc=${BUILD_RC}) — not pushing anything"
  PUSH_STATUS="not_attempted"; DEPLOY_STATUS="not_reached"; EXIT_CODE=1
  exit 1
fi

# ----------------------------------------------------------- 2. push content
if [ "${SKIP_PUSH:-0}" = "1" ]; then
  log "SKIP_PUSH=1 — not publishing to GitHub"
  PUSH_STATUS="skipped"; DEPLOY_STATUS="skipped"
  exit 0
fi

log "pushing content to GitHub"
"${ROOT}/scripts/push-content.sh"
case $? in
  0)  PUSH_STATUS="ok" ;;
  10) PUSH_STATUS="nothing_to_push"; DEPLOY_STATUS="not_needed"
      log "nothing new to publish this cycle"; exit 0 ;;
  *)  PUSH_STATUS="failed"; DEPLOY_STATUS="not_reached"; EXIT_CODE=1
      log "FATAL: content did not reach production"; exit 1 ;;
esac

# ------------------------------------------------------ 3. verify the deploy
SHA="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo '')"
if [ -z "$SHA" ]; then
  DEPLOY_STATUS="unverified"; exit 0
fi

"${ROOT}/scripts/wait-for-deploy.sh" "$SHA"
case $? in
  0)  DEPLOY_STATUS="ok" ;;
  1)  DEPLOY_STATUS="failed";  EXIT_CODE=1 ;;
  2)  DEPLOY_STATUS="timeout"; EXIT_CODE=1 ;;
  *)  DEPLOY_STATUS="unverified" ;;
esac
exit "$EXIT_CODE"
