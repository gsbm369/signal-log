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

  # METRIC COVERAGE — here, on the host, AFTER the record exists. It used to run
  # inside the builder container during the cycle, where this cycle's record
  # had not been written yet and the previous one was on the other side of the
  # mount. It skipped every cycle for a week, and the wrapper logged a reason it
  # had invented ("no metrics.json yet") instead of the one the check printed.
  # So: run it where the artifact is, and log the check's OWN last line.
  cov_out=$(STATE_DIR="$STATE_DIR" python3 "${ROOT}/curator/test_metric_coverage.py" 2>&1); cov_rc=$?
  cov_why=$(printf '%s\n' "$cov_out" | grep -v '^\s*$' | tail -1 | sed 's/^ *//')
  case $cov_rc in
    0) log "metric coverage: ${cov_why}" ;;
    2) log "metric coverage: NOT CHECKED — ${cov_why}" ;;
    *) log "WARN: metric coverage FAILED — ${cov_why}"
       printf '%s\n' "$cov_out" | grep -E 'FAIL|missing' | head -5 | while read -r l; do log "      $l"; done ;;
  esac
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

# ------------------------------------------------------------ 0. network gate
# The unit says After=network-online.target, but it is a USER unit, and the
# user manager has no such target — the ordering is silently a no-op. With
# Persistent=true the timer's catch-up fires the moment the user manager starts,
# which after a reboot is before the network is up. Measured 2026-09-18: fired
# one second after boot, 33/33 feeds unreachable, git fetch failed, and the
# cycle still ended exit 0 as a "healthy no-op".
#
# So the script waits for the network itself: DNS plus a real HTTPS round trip
# to the host every cycle depends on. If it never comes, that is a failed cycle
# with its own status, not an empty one.
net_ready() { curl -s -o /dev/null -m 5 --head https://github.com; }
NET_WAIT="${NETWORK_WAIT_S:-300}"; waited=0
until net_ready; do
  if [ "$waited" -ge "$NET_WAIT" ]; then
    log "FATAL: no network after ${NET_WAIT}s (github.com unreachable) — not curating from nothing"
    BUILD_STATUS="no_network"; EXIT_CODE=1
    exit 1
  fi
  [ "$waited" -eq 0 ] && log "network not ready — waiting up to ${NET_WAIT}s"
  sleep 5; waited=$((waited + 5))
done
[ "$waited" -gt 0 ] && log "network ready after ${waited}s"

# ------------------------------------------------------------------ 1. build
log "=== cycle starting (docker=${DOCKER_BIN}) ==="
# Bounded at 20 minutes. The builder curates 28 feeds and then runs an Astro
# build; either can stall on something outside this estate. Without a ceiling
# here the only bound is systemd's TimeoutStartSec, and a unit sitting at its
# ceiling looks identical to a unit doing work.
# FORCE_PUBLISH and SKIP_CURATE are read INSIDE the container by run-cycle.sh,
# and `docker compose run` does not forward arbitrary host environment. Setting
# FORCE_PUBLISH=1 on the host therefore did nothing at all — a documented
# override, printed by the guard's own error message, that could never work.
# Found by lowering max_posts 200 -> 60 and being correctly refused, then being
# refused again by the override.
timeout --signal=TERM --kill-after=60 "${CYCLE_TIMEOUT:-1200}" \
  "$DOCKER_BIN" compose --project-directory "$ROOT" run --rm \
    -e "FORCE_PUBLISH=${FORCE_PUBLISH:-0}" -e "SKIP_CURATE=${SKIP_CURATE:-0}" \
    -e "CYCLE_TRIGGER=${CYCLE_TRIGGER:-cron}" \
    builder
BUILD_RC=$?

if [ -s "${STATE_DIR}/build.json" ]; then
  read -r BUILD_STATUS PUBLISH_STATUS <<<"$(python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print(d.get("build_status","unknown"), d.get("publish_status","unknown"))
' "${STATE_DIR}/build.json")"
fi

# HARD RULE (owner, 2026-09-19): a cycle that reached ZERO feeds failed —
# never exit 0. The record already says so (ship_to_loki.py); this makes the
# PROCESS say so too. run-cycle.sh deliberately continues past a curator
# failure to rebuild what it has, so the builder can exit 0 here while having
# fetched nothing at all.
#
# metrics.json is overwritten, not per-cycle: a copy from before this cycle is
# the PREVIOUS cycle's counts. "This cycle's" is judged by the curator's own
# stamp, curated_at_epoch — not the file's mtime, which check_freshness.py
# refreshes after every build (so a curator killed before writing left stale
# counts with a fresh mtime). The mtime is used only when the stamp is absent,
# i.e. a curator from an image built before the stamp existed.
# Stale or missing counts as zero.
METRICS="${STATE_DIR}/metrics.json"
read -r FEEDS_OK WRITTEN <<<"$(python3 - "$METRICS" <<'PY2' 2>/dev/null || echo "0 0"
import json, os, sys
p = sys.argv[1]
try:
    m = json.load(open(p))
except (OSError, ValueError):
    print("0 0"); sys.exit()
stamp = m.get("curated_at_epoch")
print(int(m.get("feeds_ok", 0) or 0), int(float(stamp if stamp is not None else os.stat(p).st_mtime)))
PY2
)"
if [ "${WRITTEN:-0}" -lt "$CYCLE_START" ]; then
  log "metrics.json is not from this cycle (curator stamp ${WRITTEN:-none} < cycle start ${CYCLE_START}) — treating as zero feeds"
  FEEDS_OK=0
fi
if [ "$FEEDS_OK" = "0" ]; then
  log "FATAL: zero feeds reached this cycle — failed, whatever the build did"
  BUILD_STATUS="zero_feeds"; PUSH_STATUS="not_attempted"; DEPLOY_STATUS="not_reached"; EXIT_CODE=1
  exit 1
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
  # A refusal is a real failure — content did NOT reach production — but it is
  # a distinct one, and it is the operator's to clear rather than a fault to
  # retry. It gets its own status so the alert says what to do.
  11) PUSH_STATUS="refused_local_commits"; DEPLOY_STATUS="not_reached"; EXIT_CODE=1
      log "FATAL: push refused — unreviewed local commits on HEAD"; exit 1 ;;
  *)  PUSH_STATUS="failed"; DEPLOY_STATUS="not_reached"; EXIT_CODE=1
      log "FATAL: content did not reach production"; exit 1 ;;
esac

# ------------------------------------------------------ 3. verify the deploy
SHA="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo '')"
if [ -z "$SHA" ]; then
  DEPLOY_STATUS="unverified"; exit 0
fi

"${ROOT}/scripts/wait-for-deploy.sh" "$SHA"
WAIT_RC=$?
case $WAIT_RC in
  0)  DEPLOY_STATUS="ok" ;;
  1)  DEPLOY_STATUS="failed";  EXIT_CODE=1 ;;
  2)  DEPLOY_STATUS="timeout"; EXIT_CODE=1 ;;   # a run exists, did not conclude
  3)  DEPLOY_STATUS="not_needed" ;;             # commit touches nothing deployable
  # Not a commit. Reaching here means HEAD did not resolve after a successful
  # push — a bug in this script, not in the deploy.
  4)  PUSH_STATUS="bad_sha"; DEPLOY_STATUS="bad_sha"; EXIT_CODE=1
      log "FATAL: wait-for-deploy says ${SHA:-<empty>} is not a commit" ;;
  # Content WAS pushed (step 2 succeeded) but no Pages build ever started, so
  # nothing reached production and the live site is stale.
  5)  DEPLOY_STATUS="never_triggered"; EXIT_CODE=1
      log "FATAL: content pushed but no workflow run was triggered for ${SHA}" ;;
  10) DEPLOY_STATUS="unverified" ;;             # no credential / API unreachable
  # ANY OTHER CODE IS A FAILURE. This used to be `*) unverified` with exit 0,
  # which is why each new wait-for-deploy code (4 and 5) passed silently until
  # someone remembered to map it. An exit code this script does not understand
  # is not evidence the deploy worked.
  *)  DEPLOY_STATUS="unknown_exit_${WAIT_RC}"; EXIT_CODE=1
      log "FATAL: wait-for-deploy.sh exited ${WAIT_RC}, which this script does not know — treating as a failed deploy" ;;
esac
exit "$EXIT_CODE"
