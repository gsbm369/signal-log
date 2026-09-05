#!/usr/bin/env bash
# One publish cycle: curate -> build -> validate -> atomically publish -> report.
#
# Publishing is atomic. The build lands in $OUT_DIR/releases/<timestamp>/ and only
# once it passes validation is the $OUT_DIR/current symlink swapped via rename(2).
# Any failure before that swap leaves the live site exactly as it was.
set -uo pipefail

CONTENT_DIR="${CONTENT_DIR:-/app/site/src/content/posts}"
STATE_DIR="${STATE_DIR:-/data/state}"
OUT_DIR="${OUT_DIR:-/out}"
KEEP_RELEASES="${KEEP_RELEASES:-5}"
MIN_INDEX_BYTES="${MIN_INDEX_BYTES:-500}"

RELEASES="${OUT_DIR}/releases"
CURRENT="${OUT_DIR}/current"
STAMP="$(date -u '+%Y%m%dT%H%M%SZ')"
NEW_RELEASE="${RELEASES}/${STAMP}"

CYCLE_START=$(date +%s)
BUILD_STATUS="not_run"
PUBLISH_STATUS="not_run"
EXIT_CODE=0

log() { printf '[%s] %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "$*"; }

# Leave a machine-readable outcome for the host orchestrator, which owns the
# push, the deploy verification and the single Loki record for the cycle. This
# container has no git repo and cannot know whether content reached production,
# so it must not claim to.
report() {
  local dur=$(( $(date +%s) - CYCLE_START ))
  local live=-1
  [ -d "${CURRENT}" ] && live=$(find -L "${CURRENT}/posts" -name index.html 2>/dev/null | wc -l)
  python3 - "$BUILD_STATUS" "$PUBLISH_STATUS" "$EXIT_CODE" "$dur" "$live" <<'PY' || log "WARN: could not write build.json"
import json, os, sys
p = os.path.join(os.environ.get("STATE_DIR", "/data/state"), "build.json")
b, pub, rc, dur, live = sys.argv[1:6]
json.dump({"build_status": b, "publish_status": pub, "exit_code": int(rc),
           "build_duration_s": float(dur), "posts_live": int(live)}, open(p, "w"), indent=2)
PY
  log "=== build finished: build=${BUILD_STATUS} publish=${PUBLISH_STATUS} exit=${EXIT_CODE} in ${dur}s ==="
}
trap report EXIT

mkdir -p "$CONTENT_DIR" "$STATE_DIR" "$RELEASES"

log "=== publish cycle starting (${STAMP}) ==="

# ---------------------------------------------------------------- 1. curate
# The default backend is `none`, which needs no API key and costs nothing, so
# curation runs unconditionally. curate.py refuses cleanly if the configured
# backend is unusable, and that is reported rather than skipped silently.
if [ "${SKIP_CURATE:-0}" = "1" ]; then
  log "step 1/3: SKIP_CURATE=1 — building from existing posts only"
  printf '{"curator_status":"skipped_flag","backend":"","model":"","cost_usd":0}' > "${STATE_DIR}/metrics.json"
else
  log "step 1/3: curating feeds (backend=${SUMMARIZER_BACKEND:-none})"
  # A curator failure is survivable: we still rebuild and republish what we have.
  if python3 /app/curator/curate.py; then
    log "curation complete"
  else
    log "WARN: curator exited $? — continuing with the posts already on disk"
  fi
fi

# ----------------------------------------------------------------- 2. build
log "step 2/3: building Astro site"
cd /app/site || { log "FATAL: /app/site missing"; BUILD_STATUS="missing_source"; EXIT_CODE=1; exit 1; }

rm -rf /app/site/dist
if npm run build; then
  BUILD_STATUS="ok"
else
  log "FATAL: astro build failed — live site left untouched"
  BUILD_STATUS="failed"
  PUBLISH_STATUS="skipped_build_failed"
  EXIT_CODE=1
  exit 1
fi

# -------------------------------------------------------------- 3. validate
log "step 3/3: validating build output"
if [ ! -s /app/site/dist/index.html ]; then
  log "FATAL: dist/index.html missing or empty — refusing to publish"
  BUILD_STATUS="invalid_no_index"; PUBLISH_STATUS="refused"; EXIT_CODE=1; exit 1
fi

INDEX_BYTES=$(stat -c%s /app/site/dist/index.html)
if [ "$INDEX_BYTES" -lt "$MIN_INDEX_BYTES" ]; then
  log "FATAL: dist/index.html is only ${INDEX_BYTES}B (min ${MIN_INDEX_BYTES}) — refusing to publish"
  BUILD_STATUS="invalid_tiny_index"; PUBLISH_STATUS="refused"; EXIT_CODE=1; exit 1
fi

NEW_POSTS=$(find /app/site/dist/posts -name index.html 2>/dev/null | wc -l)
OLD_POSTS=0
[ -d "${CURRENT}" ] && OLD_POSTS=$(find -L "${CURRENT}/posts" -name index.html 2>/dev/null | wc -l)

# Guard against catastrophic content loss (e.g. the posts mount vanished).
if [ "$OLD_POSTS" -gt 0 ] && [ "$NEW_POSTS" -lt $(( (OLD_POSTS + 1) / 2 )) ] && [ "${FORCE_PUBLISH:-0}" != "1" ]; then
  log "FATAL: new build has ${NEW_POSTS} posts vs ${OLD_POSTS} live — looks like data loss, refusing."
  log "       set FORCE_PUBLISH=1 to override if this shrink is intentional."
  BUILD_STATUS="invalid_post_drop"; PUBLISH_STATUS="refused"; EXIT_CODE=1; exit 1
fi
log "validated: index ${INDEX_BYTES}B, ${NEW_POSTS} post page(s) (was ${OLD_POSTS})"

# --------------------------------------------------------------- 4. publish
log "publishing release ${STAMP}"
mkdir -p "${NEW_RELEASE}"
if ! rsync -a --delete /app/site/dist/ "${NEW_RELEASE}/"; then
  log "FATAL: could not stage release — live site untouched"
  rm -rf "${NEW_RELEASE}"
  PUBLISH_STATUS="stage_failed"; EXIT_CODE=1; exit 1
fi

# Atomic swap: build the new symlink beside the old one, then rename over it.
if ln -sfn "releases/${STAMP}" "${CURRENT}.tmp" && mv -Tf "${CURRENT}.tmp" "${CURRENT}"; then
  PUBLISH_STATUS="ok"
  log "published — ${CURRENT} -> releases/${STAMP}"
else
  log "FATAL: symlink swap failed — live site untouched"
  rm -f "${CURRENT}.tmp"; rm -rf "${NEW_RELEASE}"
  PUBLISH_STATUS="swap_failed"; EXIT_CODE=1; exit 1
fi

# Keep the last N releases so a rollback is one symlink away.
mapfile -t OLD < <(ls -1d "${RELEASES}"/*/ 2>/dev/null | sort -r | tail -n +$((KEEP_RELEASES + 1)))
for d in "${OLD[@]:-}"; do
  [ -n "$d" ] && [ "$(readlink -f "$d")" != "$(readlink -f "$CURRENT")" ] && rm -rf "$d" && log "pruned old release $(basename "$d")"
done

log "local preview updated — ${NEW_POSTS} post(s), $(find "$CONTENT_DIR" -name '*.md' | wc -l) markdown source(s) on disk"
log "(production publishing is the host orchestrator's job — see scripts/cron-cycle.sh)"
