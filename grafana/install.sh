#!/usr/bin/env bash
# The ONE way alerting reaches Grafana: copy this directory into Grafana's file
# provisioning, validated first. Grafana loads it on its next start.
#
#   grafana/install.sh --check     validate only, write nothing
#   grafana/install.sh             validate, then install (does not restart Grafana)
#
# Replaces two paths that disagreed: the Ansible API push (needed an admin
# credential, so it was skipped on every ordinary deploy, and never substituted
# the Prometheus uid) and ~/backup/bin/provision-alerts.sh (looked both uids up
# in grafana.db and sed-substituted them). Datasource uids are now constants
# pinned in provisioning/datasources, so nothing is looked up or substituted.
#
# The installed directory MIRRORS this one: a rule file removed here is removed
# there. Rules are deleted from Grafana only via zz-delete.yaml, because
# removing a file does not remove the rules it created.
#
# Exit 0 ok, 1 refused (nothing written), 2 cannot check.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STACK="${PROXY_STACK_DIR:-/home/nikita/server-lab/proxy-stack}"
ENV_FILE="${SECRETS_ENV:-/home/nikita/ai-blog/.env}"
CHECK=0; [ "${1:-}" = "--check" ] && CHECK=1

command -v python3 >/dev/null || { echo "cannot check: no python3"; exit 2; }

# VALIDATE BEFORE WRITING. Grafana's file provisioning is FAIL-CLOSED: a file it
# cannot parse, a rule naming a receiver that does not exist, or a file it
# cannot read stops the whole server from starting. The alerting must not be
# able to kill the thing it runs inside.
python3 - "$HERE" "$ENV_FILE" <<'PY' || { echo "REFUSING: nothing installed" >&2; exit 1; }
import pathlib, re, sys, yaml
here, env_file = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
problems = []

def load(p):
    try:
        return yaml.safe_load(p.read_text()) or {}
    except yaml.YAMLError as exc:
        problems.append(f"{p.name}: invalid YAML: {exc}")
        return {}

ds = {}
for p in sorted((here / "provisioning/datasources").glob("*.y*ml")):
    for d in load(p).get("datasources") or []:
        if not d.get("uid"):
            problems.append(f"{p.name}: datasource {d.get('name')!r} has no pinned uid")
        ds[d.get("uid")] = d.get("type")
if not ds:
    problems.append("no pinned datasources in provisioning/datasources")

alerting = sorted((here / "alerting").glob("*.y*ml"))
docs = {p: load(p) for p in alerting}
points = {cp.get("name") for d in docs.values() for cp in d.get("contactPoints") or []}

env = {}
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")

for p, doc in docs.items():
    text = p.read_text()
    if re.search(r"[A-Z]+_DATASOURCE_UID", text):
        problems.append(f"{p.name}: still carries a datasource placeholder")
    # Every ${VAR} must resolve, or Grafana expands it to "" and, for the ntfy
    # URL, posts to https://ntfy.sh/ — a failure that looks like a delivery.
    for var in sorted(set(re.findall(r"\$\{([A-Z0-9_]+)\}", text))):
        if not env.get(var):
            problems.append(f"{p.name}: ${{{var}}} is not set in {env_file}")
    for g in doc.get("groups") or []:
        for r in g.get("rules") or []:
            uid = r.get("uid")
            want = (r.get("notification_settings") or {}).get("receiver")
            if want and want not in points:
                problems.append(f"rule {uid!r} routes to {want!r}, not a contact point name {sorted(points)}")
            for q in r.get("data") or []:
                dsu = q.get("datasourceUid")
                if dsu != "__expr__" and dsu not in ds:
                    problems.append(f"rule {uid!r} names datasource {dsu!r}, not pinned ({sorted(ds)})")
                expr = (q.get("model") or {}).get("expr", "")
                # `or on() vector(0)` is accepted too: a per-series rule (one
                # alert per target) needs on(), because a bare `or vector(0)`
                # always adds a label-less 0 series and fires for ever.
                fallback = re.search(r"\bor\s+(on\s*\(\s*\)\s*)?vector\(\s*0\s*\)", expr)
                if expr and not fallback and dsu != "__expr__" and not r.get("isPaused"):
                    problems.append(f"rule {uid!r}: query has no `or vector(0)` / `or on() vector(0)` — silence would depend on noDataState")

for p in problems:
    print("INVALID: " + p, file=sys.stderr)
n = sum(len(g.get("rules") or []) for d in docs.values() for g in d.get("groups") or [])
print(f"  validated: {len(alerting)} alerting file(s), {n} rule(s), datasources {sorted(ds)}")
sys.exit(1 if problems else 0)
PY

[ "$CHECK" -eq 1 ] && { echo "  --check: valid, nothing written"; exit 0; }
[ -d "$STACK" ] || { echo "cannot install: ${STACK} does not exist"; exit 2; }

# Files are replaced in place, never the directory: the directory is
# bind-mounted into the Grafana container, and a directory swapped in by rename
# is a new inode the container never sees. New files are copied in FIRST and
# stale ones removed after, so a failed copy can leave an extra file behind but
# never an empty directory — Grafana started on an empty one loads no rules.
shopt -s nullglob
for sub in alerting datasources; do
  src="$HERE/alerting"; [ "$sub" = datasources ] && src="$HERE/provisioning/datasources"
  dest="$STACK/grafana/provisioning/$sub"
  files=("$src"/*.yaml "$src"/*.yml)
  [ "${#files[@]}" -gt 0 ] || { echo "REFUSING: nothing to install from $src" >&2; exit 1; }
  mkdir -p "$dest"
  for f in "${files[@]}"; do
    # install(1) writes the mode in the same step. Grafana (uid 472) must be
    # able to read its files: "permission denied" is a parse failure to
    # Grafana, and it refuses to start rather than skipping the file.
    install -m 0644 "$f" "$dest/$(basename "$f")"
  done
  for old in "$dest"/*.yaml "$dest"/*.yml; do
    keep=0
    for f in "${files[@]}"; do [ "$(basename "$f")" = "$(basename "$old")" ] && keep=1; done
    [ "$keep" -eq 1 ] || { echo "  removing $(basename "$old") from $sub (not in the repo)"; rm -f "$old"; }
  done
  if ! docker run --rm --user 472:0 -v "$dest:/p:ro" alpine sh -c 'cat /p/* >/dev/null' 2>/dev/null; then
    echo "REFUSING: uid 472 (grafana) cannot read ${dest}" >&2; exit 1
  fi
  echo "  installed ${#files[@]} file(s) -> $dest"
done
echo "  Grafana loads these on its next start. After a change to its environment or mounts:"
echo "    cd ~/server-lab/proxy-stack && docker compose up -d grafana   (a plain restart keeps the old env)"
