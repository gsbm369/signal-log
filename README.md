# signal.log

A dark, minimal tech blog that keeps itself current. Every six hours a homelab cron job
pulls the major technology RSS feeds, ranks them with a deterministic heuristic, writes the
survivors as Markdown, and pushes that content to this repository. GitHub Actions builds
the Astro site and deploys it to Pages.

**No model runs in the shipped default, and the system needs no API key.** Selection is a
scored heuristic — exponential recency decay, per-source weighting, title-first topic
relevance, cross-source deduplication, a noise filter and a per-source cap — and it is
covered by a golden test that freezes the exact ranked order, so a change to any constant
has to be consciously re-approved rather than drifting. Summaries come from each feed's own
`<description>`. Running cost: **zero**.

Summarisation is a pluggable backend, and an LLM is one of the three options
(`none` · `ollama` · `anthropic`). Switching is one variable and changes prose only — never
which stories appear, because ranking uses no model in any mode.

Built as a homelab exercise in unattended publishing: what it takes for a pipeline to run
on its own for months, fail safely when a feed rots or a token expires, and prove it is
still working rather than merely appearing to.

---

## Architecture

```
  homelab (cron, 6h)              GitHub                    GitHub Pages
  ┌──────────────────┐          ┌──────────────┐          ┌───────────────┐
  │ curate           │  push    │ Actions      │ artifact │ blog.gs-bm.com│
  │ rank             │ markdown │ npm ci       │─────────>│ + HTTPS       │
  │ summarize(none)  │─────────>│ astro build  │          │               │
  │ write .md        │   main   │ deploy-pages │          │               │
  │ build + validate │          └──────────────┘          └───────────────┘
  └──────────────────┘                 │
          │                            └── public, dated logs = evidence
          └── local preview on :8080, Loki metrics
```

**The homelab pushes content, not built HTML.** Not a shortcut worth taking: separating
content from build means the site rebuilds from the repo alone, so the homelab is not a
single point of failure for the published artifact; anyone can reproduce the build from a
clone; and the Actions log is public, dated evidence that the pipeline works. Pushing
`dist/` to a `gh-pages` branch would cost all three.

The local nginx on :8080 stays as a preview and as a pre-push validation gate — if the
content breaks the build, that is caught here before anything is pushed.

## Local architecture

```
                        ┌──────────────── every 6h (cron + flock) ─────────────────┐
                        ▼                                                          │
   RSS feeds ──▶ curate.py ──▶ Claude API ──▶ site/src/content/posts/*.md          │
   (7 sources)      │          (opus-5,          (bind mount, host-owned)          │
                    │       structured output)              │                      │
                    │                                       ▼                      │
                    │                                 astro build                  │
                    │                                       │                      │
                    │                                       ▼                      │
                    │                              validate output ────┐           │
                    │                                       │          │ refuse    │
                    │                                       ▼          │           │
                    │                    public_html/releases/<ts>/     │           │
                    │                                       │          │           │
                    │                          atomic symlink swap     │           │
                    │                                       ▼          ▼           │
                    │                        public_html/current ──▶ nginx :8080   │
                    │                                                              │
                    └──▶ metrics.json ──▶ ship_to_loki.py ──▶ Loki ──▶ Grafana ────┘
```

Two containers. `web` is nginx and stays up. `builder` is a one-shot job that runs the
cycle and exits — cron invokes it, nothing is left running between cycles.

### Why releases and a symlink

The published output is not overwritten in place. Each cycle builds into
`public_html/releases/<timestamp>/`, validates it, and only then swaps
`public_html/current` with `rename(2)`, which is atomic. nginx's root is that symlink.

This means there is no window where the site is half-written, and a rollback is one
command:

```bash
ln -sfn releases/20260905T124120Z public_html/current.tmp && mv -Tf public_html/current.tmp public_html/current
```

The last 5 releases are kept.

### What "fail safe" means here

Four independent guards, each verified by an injected-failure test:

| Failure | Behaviour |
|---|---|
| Claude API unreachable / auth fails | Curator logs the error, cycle continues, site rebuilds from existing posts and republishes. Status `degraded`. |
| `astro build` fails | Publish skipped, nothing pushed. Live symlink untouched. Status `failed`. |
| `git push` fails | Status **`publish_failed`**, exit 1. The commit is kept so the next cycle retries it. |
| Actions run fails or times out | Status **`publish_failed`**, exit 1. |
| No new content | Status `ok`, `push_status: nothing_to_push`. No empty commit, no pointless deploy. |
| Build output missing or `index.html` under 500 B | Publish refused. Status `failed`. |
| Post count drops by more than half | Publish refused as suspected data loss. Override with `FORCE_PUBLISH=1`. |

The rule throughout: **a bad build is never allowed to replace a good one**, and **a green
local build is never reported as a successful publish.** `cycle_status: publish_failed` is
its own terminal state precisely because "built fine here, never reached production" is the
failure most easily mistaken for success.

Commits are conditional — `git diff --cached --quiet || commit`. An unconditional 6-hourly
commit turns both the git history and the Actions log into noise inside a week.

### Alerting

`grafana/alerting/signal-log-alerts.yaml` — one rule: **no successful cycle reached
production in 48h → email**, via the Postfix relay Grafana is already pointed at.

```bash
ansible-playbook deploy.yml -e grafana_user=admin -e grafana_password=... --tags alert
```

It watches `reached_production`, not `exit_code`. A cycle that builds cleanly and finds
nothing new is a healthy no-op, and `reached_production` covers published / nothing-to-
publish / deliberately-skipped while excluding every failure mode. `noDataState: Alerting`,
because a curator that has stopped reporting is worse than one reporting failures.

The rule routes straight to its own contact point via `notification_settings`, so the
existing homelab notification policy tree is not touched.

---

## Stack

| Layer | Choice |
|---|---|
| Site | Astro 7 (static output), Tailwind CSS 4 |
| Feed | `@astrojs/rss` at `/rss.xml`, custom fields under an `xmlns:signal` namespace |
| Curator | Python 3.11, `anthropic` SDK, `feedparser`, `PyYAML` |
| Model | `claude-opus-5`, adaptive thinking, JSON-schema structured output |
| Serving | nginx 1.27-alpine |
| Build/runtime | Docker + Compose, `node:22-bookworm-slim` builder image |
| Config management | Ansible (`prereqs.yml`, `deploy.yml`) |
| Observability | JSON metric line per run → Loki → Grafana |

---

## Layout

| Path | What it is |
|---|---|
| `site/` | Astro site. Design tokens are all in `src/styles/global.css` under `@theme`. |
| `curator/curate.py` | Fetch RSS → rank and summarise with Claude → write Markdown. |
| `curator/ship_to_loki.py` | Turns `metrics.json` into one JSON log line and pushes it to Loki. |
| `curator/feeds.yml` | Sources, and the per-run caps that determine cost. |
| `curator/state/` | `seen.json` (dedupe), `metrics.json` (last run), image context hash. |
| `scripts/run-cycle.sh` | The cycle: curate → build → validate → publish → report. |
| `docker/Dockerfile.builder` | Node + Python image. Site source is baked in, not mounted. |
| `ansible/deploy.yml` | Full deploy. Idempotent — a second run reports `changed=0`. |
| `ansible/tasks/npm_proxy_host.yml` | Registers the site with Nginx Proxy Manager. |
| `public_html/` | Generated. `releases/` + `current` symlink. Not in git. |

---

## Publishing

| Piece | Where | Notes |
|---|---|---|
| Content | `site/src/content/posts/*.md`, tracked in git | The payload. |
| Build | `.github/workflows/deploy.yml` | `npm ci` → `astro build` → `deploy-pages`. |
| Domain | `site/public/CNAME` | Committed, so every build emits it. |
| DNS | `blog.gs-bm.com  CNAME  gsbm369.github.io` | **CNAME, not an A record.** |

Repository settings that are not in code:

- **Pages source must be "GitHub Actions"**, not "deploy from a branch".
- The repo must be **public** — Actions minutes are then unlimited and free.

`astro.config.mjs` sets `base: '/'`, which is correct *because* there is a custom domain.
Without one it would need `base: '/signal-log'`, and every internal link would break in a
way that only appears in production. The CNAME is committed rather than left to the repo
setting, because the artifact deploy flow does not reliably preserve a setting-only value.

### The only secret in the system

A fine-grained PAT, scoped to this one repository, `Contents: write`, nothing else. It can
add commits to one public repo. That is the entire blast radius.

It replaces an Anthropic API key, which was billable, usable from anywhere, and scoped to
an account rather than a resource. A leaked PAT means someone can commit to a public repo
whose entire content is already public and machine-generated; a leaked API key means
someone spends your money. Moving the summarizer default to `none` removed the API key
from the running system entirely — this is the trade that made that possible.

**Issued 2026-09-05, expires 2026-12-04** (90 days). Renew before then.

Scope: `signal-log` only — Contents: read/write, Metadata: read (mandatory).

**Deliberately NOT granted: Workflows.** GitHub refuses a push that touches
`.github/workflows/` without it:

```
! [remote rejected] main -> main (refusing to allow a Personal Access Token to
  create or update workflow `.github/workflows/deploy.yml` without `workflow` scope)
```

That refusal is the desired behaviour, not an obstacle. The workflow holds `pages: write`
and `id-token: write` — it *is* the deployment. A token that can rewrite it can redirect
the deployment anywhere. The workflow is therefore added once through the GitHub web UI,
and the cron token can only ever append Markdown to `site/src/content/posts/`.

Changing the pipeline is a human action through a reviewed path; publishing content is
automated. That split is the whole point of the scope.

**The security property, stated plainly: the publishing automation cannot modify its own
deployment pipeline.** If the curator were ever compromised — a hostile feed, a parsing bug,
a bad dependency — it could publish bad content to a public blog. It could not alter CI to
reach secrets, exfiltrate the repository, or push anywhere else. The workflow is added once
by a human through the GitHub web UI, and the cron token never holds the permission at all.

That asymmetry is deliberate: the automation pushes content every six hours and touches the
workflow perhaps once a month. Granting a permanent capability to serve a one-time action
would invert the tradeoff.

#### How it is stored

Never in the remote URL, never in an argument. A `https://<token>@github.com/...` remote
writes the secret into `.git/config`, where it surfaces in `git remote -v`, in every
diagnostic dump, and in any log that prints the remote — the most common way these leak.
Arguments are worse: `ps` exposes them to every process on the box for the lifetime of the
command.

```
~/.config/signal-log/          drwx------   (700)
~/.config/signal-log/git-credentials   -rw-------   (600)
```

```bash
git config --local credential.helper \
    'store --file=/home/nikita/.config/signal-log/git-credentials'
```

Only that path lands in `.git/config`. `push-content.sh` handles no token at all — it
pushes by remote *name* and lets the helper authenticate, and it refuses to run if no local
credential helper is configured. `wait-for-deploy.sh` needs the token for the GitHub API and
reads it from the credential file *inside* a Python process, using it from memory; it is
never a curl argument.

`.env` holds no token. The credential file is the only copy on the machine.

#### When it expires

Pushes start failing. That surfaces as `cycle_status: publish_failed` in Loki and, if it
goes unnoticed, as the 48h Grafana alert. **An expired token must arrive as an alert, not
as a site that quietly stops updating** — which is why both are wired before this stage
counts as done.

## Setup

```bash
cp .env.example .env
# add ANTHROPIC_API_KEY
cd ansible && ansible-playbook prereqs.yml && ansible-playbook deploy.yml
```

Behind a reverse proxy:

```bash
ansible-playbook deploy.yml \
  -e blog_hostname=blog.example.com \
  -e npm_email=admin@example.com -e npm_password=... \
  -e site_url=https://blog.example.com \
  -e blog_ssl=true
```

`blog_ssl=true` requests a Let's Encrypt certificate through NPM's API, which requires the
hostname to resolve publicly to this host and port 80 to be reachable from the internet.

---

## Operating

```bash
docker compose run --rm builder                    # publish now
SKIP_CURATE=1 docker compose run --rm builder      # rebuild, no API call
docker compose run --rm --entrypoint python3 builder /app/curator/curate.py --dry-run
tail -f logs/cycle.log                             # local log
ansible-playbook deploy.yml -e cycle_hours=2 --tags cron
```

Editing a `.astro` file requires `docker compose build builder` first — site source is
baked into the image (see "problems hit" below).

---

## Summarizer backends

Two stages, deliberately separated:

| Stage | Where | Uses a model? |
|---|---|---|
| **Selection** — what gets published | `curator/ranker.py` | **Never**, in any mode |
| **Summary** — how it reads | `curator/summarizers.py` | Depends on the backend |

Selection is a pure heuristic and costs nothing, so choosing a backend only changes the
prose, never which stories appear. All three satisfy one interface:

```python
backend.name                 -> str
backend.health()             -> (ok: bool, detail: str)
backend.summarize(articles)  -> list[Summary]   # one per input, same order, none dropped
backend.usage                -> {"model", "input_tokens", "output_tokens", "cost_usd"}
```

A backend that fails on an individual article falls back to the feed description rather
than losing the story, so a partial outage degrades quality, not coverage.

| Backend | What it does | Needs | Cost |
|---|---|---|---|
| **`none`** *(default)* | Uses each feed's own `<description>`, cleaned up. | nothing | **$0** |
| `ollama` | A local model on the Docker host, over HTTP. | a container + RAM | $0 |
| `anthropic` | `claude-haiku-4-5` via the **Batch API**. | API key | ~$0.70–1.40/mo |

Switch with one variable — no code change:

```bash
ansible-playbook deploy.yml -e summarizer_backend=ollama -e force_cycle=true
ansible-playbook deploy.yml -e summarizer_backend=anthropic -e force_cycle=true
```

### `ollama` — RAM is the constraint

Ollama needs the whole model resident; CPU only affects speed. Budget roughly:

| Model | Resident RAM | Notes |
|---|---|---|
| `llama3.2:3b` *(default)* | ~3–4 GB | Adequate for compressing a feed blurb. |
| `llama3.1:8b` | ~6–8 GB | Noticeably better prose. |
| `mistral-nemo:12b` | ~9–12 GB | Diminishing returns for this task. |

This host has other containers running (Grafana, Loki, NPM, Portainer, Prometheus) — check
free memory before pulling anything above 8B. Add the service and pull the model:

```bash
docker run -d --name ollama --restart unless-stopped \
  --network proxy-stack_proxy-net -v ollama:/root/.ollama ollama/ollama
docker exec ollama ollama pull llama3.2:3b
```

`health()` fails loudly if the endpoint is unreachable *or* the model was never pulled —
a common and otherwise silent misconfiguration.

### `anthropic` — Haiku, and Batch

Two deliberate choices. **Haiku 4.5, not Opus**: "compress a blurb into three sentences" is
not a frontier-model task, and Opus costs 5× the input and 5× the output for it. **The Batch
API**, because a scheduled job is not latency-sensitive and batch is half price. Results
come back in arbitrary order and are matched by `custom_id`, never by position.

## Cost control

On the default `none` backend the recurring cost is **zero** — no model is called at any
stage. The figures below apply only when `summarizer_backend=anthropic`.

Everything that drives cost is a variable in `ansible/deploy.yml`:

| Variable | Default | Effect |
|---|---|---|
| `cycle_hours` | 6 | Calls per day = 24 / this |
| `max_candidates` | 40 | Articles sent to the model — the input-token driver |
| `publish_count` | 5 | Articles summarised — the output-token driver |
| `curator_model` | `claude-haiku-4-5` | Per-token rate |
| `per_source_cap` | 3 | Stops one prolific feed dominating |

Measured against ~25K input / 4K output per run:

| Model | Cadence | Approx / month |
|---|---|---|
| Opus 5 | every 6h | ~$27 |
| Haiku 4.5 | every 6h | ~$5 |
| Haiku 4.5 | daily | ~$1.40 |
| Haiku 4.5 | daily, Batch API | **~$0.70** |
| **`none`** | any | **$0** |

`summarizers.py` prices each run from `PRICING` (halved for Batch) and writes `cost_usd`
into `metrics.json`, so actual spend is in Loki rather than estimated.

Only *unseen* articles are sent — `seen.json` means a quiet cycle costs almost nothing,
and a cycle with no new articles skips the API call entirely.

---

## Observability

One JSON line per cycle, to stdout (captured in `logs/cycle.log`) and to Loki:

```json
{"ts":"2026-09-05T12:41:58Z","event":"publish_cycle","cycle_status":"degraded",
 "curator_status":"error","build_status":"ok","publish_status":"ok","exit_code":0,
 "duration_s":3.0,"articles_fetched":62,"articles_new":62,"articles_kept":0,
 "feeds_ok":7,"feeds_failed":0,"model":"claude-opus-5","input_tokens":0,
 "output_tokens":0,"cost_usd":0.0,"posts_live":1,"error":"AuthenticationError: ..."}
```

Labels are kept low-cardinality (`job`, `service`, `host`, `level`, `status`); all numbers
live in the line body so Grafana parses them with `| json`.

```logql
{job="signal-log"} | json | cycle_status != "ok"
sum(sum_over_time({job="signal-log"} | json | unwrap cost_usd [24h]))
```

### Grafana dashboard

`grafana/signal-log-dashboard.json` — import it via **Dashboards → New → Import** and pick
the Loki datasource when prompted (it is a dashboard variable, so no UID is hardcoded).

Twelve panels: problem-cycle and spend counters, outcomes over time as a stacked bar
(`ok` / `degraded` / `failed` / `skipped`), cost and tokens per run, articles
fetched/new/kept, feed health, and log panels for problem cycles and the full record
stream. Every query was validated against the live Loki before shipping.

Note: this Grafana container has **no volume mounts** — its config lives in the container's
internal SQLite, so an imported dashboard is lost if the container is recreated. Keeping
the JSON in git is the durable copy. Worth giving Grafana a volume separately.

Shipping failures never fail the cycle — `ship_to_loki.py` swallows connection errors and
still prints the record locally.

Shipping failures never fail the cycle — `ship_to_loki.py` swallows connection errors and
still prints the record locally.

---

## TLS and the two domains

The homelab has two similarly-named domains and they are not interchangeable:

| Domain | State | Usable for TLS? |
|---|---|---|
| `gsbm.com` | Registered, delegated to Google Cloud DNS, but the nameservers answer **REFUSED** — no hosted zone exists there, so public resolvers `SERVFAIL`. All `*.gsbm.com` homelab names work only through the LAN resolver. | **No** — neither HTTP-01 nor DNS-01 can work until the zone is recreated. |
| `gs-bm.com` | Live. `NOERROR`, A records at GitHub Pages, NS at `domaincontrol.com` (GoDaddy). Serves HTTPS 200. | **Yes** — `blog.gs-bm.com` is `NXDOMAIN` and free to create with one additive A record. |

`gs-bm.com` also carries live email — Microsoft 365 MX, `v=spf1 include:secureserver.net -all`,
and an M365 domain-verification TXT — all served by GoDaddy's nameservers. **Adding an A
record is additive and safe. Moving the nameservers is not**, and no TLS path documented
here requires it.

### Why not Cloudflare Tunnel

A tunnel removes the need for any inbound port, which is attractive. But a named tunnel
routes a hostname via a CNAME to `<tunnel-uuid>.cfargotunnel.com`, and that name only
yields an address when it is resolved inside a Cloudflare zone with the record proxied.
From a public resolver it is `NOERROR` with no address:

```
dig @8.8.8.8 test.cfargotunnel.com A   ->  status: NOERROR, no A record
dig @a.gtld-servers.net cfargotunnel.com NS  ->  dell/kurt.ns.cloudflare.com
```

A CNAME pointing there from GoDaddy would therefore resolve to nothing. Using a tunnel with
a custom hostname means putting the zone on Cloudflare — an NS move, which is exactly the
change that endangers the live mail. So a tunnel is not a drop-in fallback here.

### The DNS-01 fallback that needs no NS move

If inbound port 80 turns out to be blocked, DNS-01 is the path, and it does **not** require
moving nameservers. Two variants, in order of preference:

1. **CNAME delegation of the challenge only.** Add one static record in GoDaddy —
   `_acme-challenge.blog.gs-bm.com  CNAME  <target in a zone you control>` — and let acme.sh
   answer there. GoDaddy then needs no API access at all, and the delegation is set once.
   Immune to GoDaddy's API eligibility rules.
2. **acme.sh with the GoDaddy DNS API** (`dns_gd`), using a key/secret from the GoDaddy
   developer portal. Simpler conceptually, but GoDaddy gates DNS API access by account
   tier, so confirm the key works before committing to it.

### Preflight

`ansible/preflight-acme.yml` answers the port-80 question authoritatively before anything is
changed. It checks public DNS, compares against the egress IP, verifies NPM serves
`/.well-known/acme-challenge/` locally, then asks **Let's Encrypt staging** to validate over
HTTP-01 with `--dry-run` and an isolated config dir — so nothing under `/etc/letsencrypt` or
any existing proxy host is touched.

```bash
ansible-playbook preflight-acme.yml -e blog_hostname=blog.gs-bm.com
```

A previous manual attempt in June never reached a challenge at all — it failed at
`new-order` with `rejectedIdentifier` for `portainer.local` ("Domain name does not end with
a valid public suffix"). That is why `/etc/letsencrypt` has an `accounts/` directory but no
`live/`, and it means **inbound port 80 has never actually been tested** on this host.

---

## Problems hit while building this

### 1. The named volume was owned by root, and nothing could write to it

The first design published into a Docker *named volume* shared between `builder` and
`web`. It failed on the first real run:

```
rsync: [generator] chgrp "/out/." failed: Operation not permitted (1)
rsync: [receiver] mkstemp "/out/.index.html.D1AnUH" failed: Permission denied (13)
```

The cause is a detail of how Docker initialises named volumes: **an empty named volume
inherits the ownership and permissions of the image path it is first mounted at.** The
compose file listed `web` before `builder`, so nginx mounted the volume first, at
`/usr/share/nginx/html` — a root-owned directory in the nginx image. The volume was
therefore created root-owned. `builder` runs as uid 1000 (deliberately, so files written
into bind mounts stay owned by the host user), and could not write a byte into it.

Three things make this nasty:

- It is order-dependent. Whichever service mounts the volume first wins, and compose
  service order is not something you normally think of as load-bearing.
- It only happens once, at volume *creation*. Recreating the containers does not fix it;
  you have to `docker volume rm` and get the ordering right, or chown out of band.
- `docker compose up` reports success. The failure surfaces later, inside the job.

The fix was to stop using a named volume. The published output is now a plain bind mount
(`./public_html`) owned by the host user, so ownership is explicit and inspectable, the
generated site can be read without entering a container, and the release/symlink scheme
becomes possible — you cannot easily do an atomic symlink swap inside a volume that two
containers disagree about the ownership of.

**Lesson:** if a named volume is written by a non-root container, either chown it
explicitly on creation or don't use one. A bind mount with known ownership is easier to
reason about, and here it enabled a better design.

### 2. musl vs glibc — the node_modules trap

The project was scaffolded by running `npm create astro` in a `node:22-alpine` container,
which built native binaries (esbuild, rollup) against **musl**. The runtime image is
`node:22-bookworm-slim`, which is **glibc**. Bind-mounting the host's `site/` into that
image would have shadowed the image's own `node_modules` with musl binaries that cannot
execute there.

The fix: bake the site source into the image (`COPY site /app/site` after `npm ci`) and
bind-mount only what genuinely needs to be shared — the posts directory, curator state,
and `feeds.yml`. The trade-off is that changing a template requires an image rebuild,
which is the correct behaviour for a deploy pipeline anyway.

### 3. `localhost` in a container is IPv6 first

The nginx healthcheck used `wget -qO- http://localhost/healthz` and reported the container
unhealthy while the site served fine from outside:

```
wget: can't connect to remote host: Connection refused
```

`localhost` resolves to `::1` before `127.0.0.1` in the container, and the nginx config
only had `listen 80;` — IPv4. Fixed on both sides: added `listen [::]:80;` and pointed the
healthcheck at `127.0.0.1` explicitly.

### 4. `<source>` is a reserved RSS element

The first version of the feed emitted `<source>Hacker News</source>` for provenance.
`<source>` is defined in RSS 2.0 as the channel an item was republished from and requires
a `url` attribute — strict readers reject or misinterpret it. All custom fields moved to
their own namespace (`xmlns:signal`), so `signal:source`, `signal:heat`, etc.

### 5. Making Ansible genuinely idempotent

The first playbook reported `changed` on every run because `docker compose build` and
`docker compose run` were plain `command` tasks with `changed_when: true`. Two fixes:

- **Image builds** are gated on a SHA-256 of the build context (Dockerfile, scripts,
  curator, site source, lockfile), stored in `curator/state/.image-context-hash`. The
  build runs only when that hash changes.
- **The publish cycle** runs only when there is no published release yet, or
  `-e force_cycle=true`. The converged state is "a published site exists", not "a build
  was just run".

Second consecutive run is now `changed=0`.

### 6. `stat: follow: true` made a clean deploy silently serve a placeholder

The playbook creates a bootstrap placeholder so nginx has a root on first deploy, then
decides whether to run a publish cycle by checking what `public_html/current` points at:

```yaml
- ansible.builtin.stat:
    path: "{{ blog_root }}/public_html/current"
    follow: true            # <- the bug
  register: current_release
- set_fact:
    do_cycle: "{{ ... or (current_release.stat.path) is search('bootstrap') }}"
```

With `follow: true` the module stats the symlink's **target**, so `stat.lnk_target` is
never populated at all and `stat.path` merely echoes the path that was queried. The
`search('bootstrap')` test could therefore never be true. Since the bootstrap task always
creates `current` before the stat runs, `stat.exists` was always true and `do_cycle`
always evaluated false.

The result on a fresh machine: the placeholder is served indefinitely while the playbook
exits green. The `uri` probe gets a cheerful `200` — *from the placeholder* — and the post
count reads Markdown files on disk that were never actually published.

Two fixes, because either alone is insufficient:

- `follow: false`, and test `stat.lnk_target` (which is only populated when not following).
- The verification step now pulls `return_content: true` and **asserts** the served page is
  not the placeholder. A 200 is not evidence of a deploy; the content is.

Reproduced and confirmed with an isolated playbook:

```
follow:true  -> path=/tmp/statdemo/current  lnk_target=<<UNDEFINED>>  search=False
follow:false -> lnk_target=releases/bootstrap                         search=True
```

**Lesson:** when a check exists to catch a failure, test that it actually fires. This one
was written, looked right, and had never once evaluated true.

### 7. Config written by regex, and other quiet assumptions

Three smaller things in the same family — each works until it doesn't, and fails silently:

- **`lineinfile` on `feeds.yml`** matched `^  max_candidates:` by indentation. If those keys
  ever moved nesting level the regex would miss and append at the wrong scope, producing
  valid YAML that means something else. Replaced with a Jinja template that renders the
  whole file from `blog_feeds` and the cost vars.
- **The cron job hardcoded `/usr/bin/docker` and `/usr/bin/flock`.** Both are now resolved
  at deploy time with `command -v` and written into `.env`, with a PATH-based fallback in
  the wrapper and a clear `FATAL` if neither resolves.
- **`flock -n` silently swallowed an overlapping run.** A skipped cycle now emits the same
  JSON record as any other outcome, with `cycle_status: "skipped"` and
  `reason: "overlapping_run_lock_held"`, so a job that never runs is visible in Grafana
  rather than being indistinguishable from a job that never fired.

That last one exposed a further wrinkle: the cron wrapper runs on the **host**, where
`http://loki:3100` does not resolve — that name only exists on the container network. The
first skip record failed with `HTTP 000`. There are now two Loki URLs, `LOKI_URL` for the
container and `LOKI_URL_HOST` for the host side.

### 8. `site_url` regressed to localhost on every plain re-run

Astro builds RSS links from `site` at build time. `site_url` defaulted to
`http://localhost:8080`, and the playbook wrote that default into `.env` on every run — so
deploying with `-e site_url=https://...` once, then running the playbook plainly, silently
reverted every link in the published feed to localhost.

`site_url` now defaults to empty and resolves as: explicit `-e` > whatever `.env` already
holds > localhost. The read has to happen *before* the `.env` write task, which is a
mistake worth making only once.

### 9. One feed was quietly malformed

`hnrss.org/show` returned XML that feedparser rejected with `mismatched tag`. Because the
collector catches per-feed errors and continues, this showed up only as one warning line
among six successful feeds. It is now counted (`feeds_failed` in the metrics) so a feed
rotting is visible in Grafana rather than buried. Replaced with `hnrss.org/best` and
IEEE Spectrum.

---

## Ranking

`curator/ranker.py` is a port of the heuristic from `netlify/functions/news/feeds.mjs` —
the logic, not the language. Six stages:

1. **Noise filter** — drops digest/roundup/listicle/deals posts and HN discussion threads.
2. **Recency decay** — exponential, 36-hour half-life.
3. **Source weighting** — per-feed `weight`, clamped to a deliberately narrow **[0.85, 1.30]**.
4. **Relevance multiplier** — focus-stack hits **counted from the title alone**.
5. **Cross-source dedupe** — normalised title (stopwords stripped, sorted) plus canonical URL
   (tracking params, `www`, AMP suffixes and fragments removed).
6. **Per-source cap** — applied in score order, so each feed keeps its best.

The score is a plain product:

```
score     = recency(age_hours) x source_weight x relevance
relevance = 1 + focus_hits x 0.5 + (0.15 if any topics else 0)
```

**Relevance is a multiplier, not an addend, and this is structural.** It starts at a
neutral 1.0, so source weight and relevance compete in the same unit. Under an additive
lift, a weight-2.0 source with zero relevance beat a weight-1.0 source with two focus
hits — the source was doing the ranking. As a multiplier, `0.95 x 1.00 = 0.95` loses to
`0.90 x 1.65 = 1.49`.

**The weight band is narrow on purpose.** Source weight should break ties between
comparably relevant stories, not lift an irrelevant one to the top; a 2.0-vs-1.0 spread
makes the source the ranking. Weights are clamped, so a `feeds.yml` typo cannot widen it.
Hacker News sits at the **floor** — it is the noisiest general feed and carries the most
off-topic material:

| Feed | weight |
|---|---|
| IEEE Spectrum | 1.20 |
| MIT Technology Review | 1.15 |
| Ars Technica | 1.10 |
| The Verge | 1.00 |
| TechCrunch / Hacker News Best | 0.95 |
| Hacker News | 0.85 |

`weight` and the fetch quota used to be the same field (`take = weight * 8`), so
compressing the band would have silently cut every feed to ~7 entries. `fetch` is now its
own field.

It ranks ~70 articles in well under a second and costs nothing.

### Title-first classification

Scoring the combined title + summary is wrong, and it fails in a specific way: package-list
digests ("Security updates for Thursday") match five focus terms from their body and take
the top slot on relevance alone, while the headline says nothing. A body that mentions
Kubernetes is not a story about Kubernetes; a headline that does, is.

So `classify()` counts focus hits from the **title only**. The body contributes tags —
useful for the tag chips — but no score. The golden test asserts this directly.

### Tests

```bash
docker compose run --rm --no-deps --entrypoint python3 builder /app/curator/test_ranker.py
docker compose run --rm --no-deps --entrypoint python3 builder /app/curator/test_ranker_golden.py
```

`test_ranker.py` — 38 assertions covering each stage in isolation.

`test_ranker_golden.py` — a frozen fixture at fixed timestamps asserting the **full ranked
order**. Filter tests prove a stage fires; they cannot catch a constant change that quietly
degrades ranking while every filter still passes. Demonstrated:

| Change | `test_ranker.py` | `test_ranker_golden.py` |
|---|---|---|
| `HALF_LIFE_HOURS` 36 → 12 | caught (direct assertion) | caught |
| `RELEVANCE_SCALE` 0.18 → 0.60 | **"All ranker tests passed"** | **caught — positions 4/5 swapped** |

Re-approve an intentional change with `--print` and paste the emitted block over
`EXPECTED_ORDER`. The expectation carries the reasoning for each position, so it doubles as
documentation of why one story outranks another.

**It has already earned its keep twice.** Regenerating the expectation after the
multiplicative change reported `dupe_url = 0` for a fixture that plainly contained a URL
twin — an article dropped as a *title* duplicate never registered its URL, so a third
article sharing that URL sailed through. Rejected duplicates now register both keys. And
the strict-boundary bug (`exploit` missing "actively exploited") surfaced the same way.
Neither was visible to any filter test.

> **Constants were reconstructed, not copied.** `feeds.mjs` has not been reachable from
> this host at any point. Half-life, weights, the focus-stack list, the noise patterns and
> the per-source cap were written from a description and are isolated at the top of
> `ranker.py`.
>
> **Taken verbatim:** the NOISE regex list (`NOISE_PATTERNS_ORIGINAL`) and the scoring
> structure — `recency x sourceWeight x relevance`, with
> `relevance = 1 + focusHits*0.5 + (topics ? 0.15 : 0)`.
>
> **Kept separate:** `NOISE_PATTERNS_EXTRA`. The original polls LWN, Phoronix and vendor
> blogs; this project polls Hacker News and TechCrunch, which produce listicles, deals and
> discussion threads the original never had to filter. The ported list stays verbatim and
> auditable; the extras are opt-out via `extra_noise_filter: false`.
>
> Two deliberate divergences from the original, both requested:
> - Short, collision-prone terms (`iac`, `aws`, `gcp`) use word boundaries rather than the
>   original's literal surrounding spaces, which miss a title that starts with the term and
>   any trailing punctuation — `" aws "` never matches `"AWS, us-east-1 down"`.
> - `exploit`, `breach`, `vulnerab`, `fine-tun`, `benchmark`, `inference` and `transformer`
>   are prefix-matched so inflections count. Strict boundaries made `exploit` miss
>   "actively exploited", which is exactly the headline shape that should score highest.
>
> Term matching is the one place this does **not** align to the original. The original uses
> `.includes()` on stems, which catches inflections for free but is what produced the
> arm-in-alarm failure and forced the literal-space workaround. The synthesis here — a
> leading word boundary with prefix matching for stems (`\bexploit`), full boundaries for
> short exact terms (`\barm\b`) — gets the inflections without the false positives.

## Editorial behaviour

The curator writes from headlines and feed blurbs; it has **not** read the full articles.
It is instructed accordingly: no invented quotes, figures, or named sources, and a shorter
write-up when the source material is thin. Every post links to its origin, and that link
is the authority — not the summary.

The `heat` score is the model's own estimate of significance. A cycle where nothing clears
60 is a correct outcome, not a broken one.

The real editorial dial is `SYSTEM_PROMPT` in `curator/curate.py`.
