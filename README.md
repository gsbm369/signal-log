# signal.log

A dark, minimal tech blog that writes itself. A cron job pulls the major technology RSS
feeds, asks Claude which stories actually matter, writes them up as Markdown, rebuilds a
static Astro site, and swaps the result into place atomically.

Built as a homelab exercise in making an LLM do useful unattended work — and, more
interestingly, in making it fail safely when it doesn't.

---

## Architecture

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
| `astro build` fails | Publish is skipped entirely. Live symlink untouched. Status `failed`. |
| Build output missing or `index.html` under 500 B | Publish refused. Status `failed`. |
| Post count drops by more than half | Publish refused as suspected data loss. Override with `FORCE_PUBLISH=1`. |

The rule throughout: **a bad build is never allowed to replace a good one.**

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

## Cost control

The recurring cost is one Claude call per cycle. Everything that drives it is a variable
in `ansible/deploy.yml`:

| Variable | Default | Effect |
|---|---|---|
| `cycle_hours` | 6 | Calls per day = 24 / this |
| `max_candidates` | 40 | Articles sent to the model — the input-token driver |
| `publish_count` | 5 | Articles summarised — the output-token driver |
| `curator_model` | `claude-opus-5` | Per-token rate |

`curate.py` prices each run from `PRICING` and writes `cost_usd` into `metrics.json`, so
actual spend is in Loki rather than estimated.

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

## Editorial behaviour

The curator writes from headlines and feed blurbs; it has **not** read the full articles.
It is instructed accordingly: no invented quotes, figures, or named sources, and a shorter
write-up when the source material is thin. Every post links to its origin, and that link
is the authority — not the summary.

The `heat` score is the model's own estimate of significance. A cycle where nothing clears
60 is a correct outcome, not a broken one.

The real editorial dial is `SYSTEM_PROMPT` in `curator/curate.py`.
