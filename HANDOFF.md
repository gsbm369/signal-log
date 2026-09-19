# signal.log — handoff

Last refreshed **2026-09-18** from measurements on the machine. §2, §5 (except where
marked), §9 and §10 date from 2026-09-10 and still hold. Written for an agent picking
this up cold. **Measure before relying on any number here.**

---

## 1. What this is

An autonomous engineering newsletter. Every 6 hours a homelab VM pulls **47 RSS feeds in
9 categories**, ranks them deterministically (**no LLM in the ranking path**), writes
Markdown, pushes the Markdown to GitHub, and GitHub Actions builds and deploys it to
GitHub Pages.

- **Live:** https://blog.gs-bm.com
- **Repo:** https://github.com/gsbm369/signal-log (branch `main`)
- **Working dir:** `/home/nikita/ai-blog`
- **Local preview:** http://192.168.100.25:8080 (nginx container `aiblog-web`)

### Last verified cycle (2026-09-18 19:10 UTC, production)

```
cycle_status ok · push ok · deploy ok · feeds_ok 47 · feeds_failed 0
posts_live 60 · articles_kept 36 · duration 138s · cost_usd 0.0
```

**Running cost: $0.** `summarizer_backend: none`: post bodies are feed descriptions.

### Front page (owner's reviewed reference, plus 2026-09-18 amendments)

- **Freshness:** nothing older than 7 days, anywhere. `today` = age ≤ 24h,
  `this week` = ≤ 7d, labelled. Age = `CYCLE_START_UTC` − author date; one clock for
  curator, build and gates.
- **Fold:** 5 slots, **at most one story per source**: today by score, then this week
  under the same rule.
- **Sections**, fixed order: microsoft, system_design, devops_linux, languages,
  company_eng, deep_dives, fintech, aggregators, gaming. At most 2 per source
  then the 6-slot quota; never filled from another category.
- **Empty section:** "No new posts this week." only if nothing is fresh; if its fresh
  stories are all in the fold, "Today's/This week's <label> stories are in the
  headlines above." linking to `#feed`.
- **"+N more"** per section → `/category/<cat>/`, every fresh story in the category.
- **Stock:** at most `CATEGORY_CEILING` = 10 posts per category (`curate.py`), and
  `max_posts` 90 = 10 × 9, so the global cap never evicts. `test_categories.py`
  asserts `max_posts ≥ ceiling × categories`.

Enforced after every build, in `run-cycle.sh`: `check_freshness.py` (index and every
category page) and `check_selection.py`, an **independent** implementation of the
selection rules compared slot by slot against the built page.

---

## 2. Architecture

```
homelab VM (systemd timer, 6h)         GitHub                  GitHub Pages
┌───────────────────────┐            ┌──────────────┐        ┌────────────────┐
│ curate → rank → image │  push .md  │ Actions      │ artifact│ blog.gs-bm.com │
│ → write Markdown      │───────────>│ npm ci       │───────>│ + HTTPS        │
│ → astro build         │   main     │ astro build  │        └────────────────┘
│ → validate → publish  │            │ deploy-pages │
└───────────────────────┘            └──────────────┘
        │
        ├── local nginx :8080 (preview + pre-push validation gate)
        └── Loki JSON metrics → Grafana dashboard + alerts
```

**The homelab pushes CONTENT, never `dist/`.** Deliberate: the site rebuilds from a clone
alone, the homelab is not a single point of failure for the published artifact, and the
public Actions log is dated evidence the pipeline ran. Do not "simplify" this by pushing
built HTML to `gh-pages`.

---

## 3. File map

```
ansible/deploy.yml            single source of truth — all tunables live in `vars:`
ansible/tasks/                npm_proxy_host.yml
grafana/install.sh            the ONE alerting path: validates, installs file provisioning
ansible/templates/feeds.yml.j2  → renders curator/feeds.yml (GENERATED, tracked)

curator/curate.py             fetch → dedupe → per-category rank → write front matter
curator/ranker.py             FROZEN. deterministic scoring. do not tune casually
curator/images.py             lead-image extraction (5 steps, see §5)
curator/summarizers.py        pluggable: none | ollama | anthropic (Batch API, haiku)
curator/loki.py               metric shipping
curator/weekly_digest.py      Sunday email digest
curator/test_ranker_golden.py FROZEN fixture: full ranked order + stats + 8 invariants
curator/test_ranker.py        unit tests
curator/test_feeds.py         CDATA-in-pubDate regression test
curator/check_freshness.py    publish gate: 7-day policy on index + category pages
curator/check_selection.py    publish gate: independent implementation of the selection
curator/test_*.py             standalone scripts (no pytest in the image), see §7
scripts/test-front-page.sh    real Astro build of a fixture with a known answer
scripts/test-section-isolation.sh  deleting one category changes no other section

scripts/run-cycle.sh          IN CONTAINER: curate → build → validate → atomic publish
scripts/cron-cycle.sh         ON HOST: lock → container → push → wait-for-deploy → 1 metric
scripts/push-content.sh       git push; NEVER touches the token (credential helper does)
scripts/wait-for-deploy.sh    polls Actions; path-filter aware; exit 3 = no run expected
scripts/weekly-digest.sh      Sunday entry point (uses host Postfix)

site/                         Astro 7.3.1 static + Tailwind 4 (@theme tokens)
site/src/layouts/BaseLayout.astro   CSP with hashed inline script, og:image
site/src/categories.ts        site half of the category contract; SECTION_ORDER, labels
site/src/pages/category/[cat].astro  the "+N more" pages
site/src/content/posts/*.md   the published content (≤ 90 files)
site/public/CNAME             blog.gs-bm.com — CI derives the site URL from this file
site/public/og-card.png       1200×630 social card, 37188 B

systemd/                      signal-log-cycle.{service,timer}, signal-log-digest.*
grafana/alerting/signal-log-alerts.yaml   two-tier alert rules + contact points
.github/workflows/deploy.yml  the ONLY thing that builds production
docker-compose.yml            web (nginx, always up) + builder (one-shot)
README.md                     long; §"Controls that were never exercised" is the important part
```

---

## 4. Key tunables — `ansible/deploy.yml` `vars:`

| var | value | note |
|---|---|---|
| `cycle_hours` / `cron_minute` | 6 / 17 | 00,06,12,18 at :17 |
| `max_posts` | 90 | = ceiling 10 × 9 categories; must never be the thing that evicts |
| `per_source_cap` | 3 | per source per run |
| `scoring_categories` | 9 entries | half_life / ingest_days (≤ 7, capped in code) / retention / cap 6 |
| `blog_feeds` | 47 feeds | weight band [0.60, 1.30]; rejected feeds listed with measurements |
| `summarizer_backend` | `none` | `ollama` / `anthropic` also implemented |

Change tunables **only** in `deploy.yml`, then re-run the playbook. `curator/feeds.yml` is
generated; editing it directly is thrown away. A category change must also update
`site/src/categories.ts`, or `test_categories.py` fails the cycle.

## 5. Non-obvious design decisions (read before changing anything)

### Ranking is deterministic and frozen
`score = recency × source_weight × relevance`. Relevance **multiplies** — it is structural,
not tuning. Constants: 36h half-life, `FOCUS_HIT_BONUS 0.5` (title hits only),
`TOPIC_BONUS 0.15`, source weights compressed to **0.85–1.30 with HackerNews at the floor**.
The noise regex list is verbatim from an earlier `feeds.mjs` implementation.
`test_ranker_golden.py` asserts the full ranked order plus
`{noise:2, stub:1, dupe_url:1, dupe_title:1, capped:2}`. **If you touch ranker.py the
golden test must be re-blessed deliberately, never auto-updated.**

Word-boundary matching with a `PREFIX_TERMS` set is used instead of `.includes()` — the
substring version matched `arm` inside *alarm*, *warming*, *frame*.

### Categories come from the feed, never from keywords
Every feed declares `category:`. Nine categories as of 2026-09-18. Ranking runs
**per category**, and `max_candidates` is applied **after** the split. It used to be applied
to the pooled list: with 182 articles the newest 40 were world/gaming-heavy and **tech
published nothing at all**. That bug is invisible in logs — the cycle exits green.

### Image extraction order (`curator/images.py`)
1. `media:content` → 2. `media:thumbnail` → 3. `enclosure` → 4. **first `<img>` in entry
HTML** → 5. `og:image` fetched from `sourceUrl`.

Step 4 was added after measurement: The Verge ships its image in `content[0].value` HTML,
not as a media element (10/10 entries); MIT 5/10. Without it both fall through to a network
fetch for an image the feed already handed over. In-feed coverage 29% → 51%, total 89%.
`enclosure` measured 0/68 — kept for correctness, contributes nothing today.

Hard rules: **HTTPS only** (the CSP silently blocks `http:`), junk-URL regex (tracking
pixels, avatars, badges), 6s timeout, 200 KB read cap, and **an image failure must never
fail the cycle**. Step 5 runs **only for selected stories** (~1.2 s each; at collect time it
would add minutes per cycle for images that get discarded). **A post with no image is
normal** — no placeholder, no forcing.

### Publishing is atomic
Build lands in `public_html/releases/<timestamp>/`; only after validation is
`public_html/current` swapped with `mv -T` (rename(2)). Any failure before the swap leaves
the live site untouched.

### Scheduling: systemd timers, not cron
The Linux guest runs on a Hyper-V host **the owner switches off**. Vixie cron silently
loses every window elapsed while the VM is saved — that cost ~21 hours of publishing once
and looked exactly like a code bug. `Persistent=true` fires immediately on resume.
`loginctl enable-linger` is on. **Gaps in publishing are usually the machine being off,
not a fault.**

### The only secret
A fine-grained GitHub PAT in `~/.config/signal-log/git-credentials` (0600, dir 0700), used
via the git credential helper. Rules the owner set explicitly and that still stand:
- never in a remote URL, never as a command-line argument (argv is world-readable)
- **do not grant it Workflows scope**
- `grep -rI 'github_pat' ~/ai-blog` must return nothing
- **expires 2026-12-04** — renewal is the owner's job

### CSP
`BaseLayout.astro` computes a sha256 of the inline reveal script at build time and embeds
it in the CSP. `img-src` currently allows remote hosts because images are hot-linked.
`frame-ancestors` cannot be enforced from a `<meta>` tag — this is documented honestly in
the README rather than faked.

---

## 6. Observability and alerting

- **Metrics:** one JSON line per cycle → Loki, `job=signal-log`. Also in `logs/cycle.log`.
- **Grafana:** http://localhost:3000 — dashboard `grafana/signal-log-dashboard.json`.
  Lab credentials the owner supplied: user `bot`, password `[redacted]` (LAN only).
- **Alerts, two tiers:**
  - *missed two consecutive cycles* — `for: 20m`, severity `warning`
  - *no publish in 48h (backstop)* — `for: 30m`, severity `critical`
  - both use `... or vector(0)` so silence evaluates to `0` instead of an empty result.
    Relying on Grafana's `noDataState` dropdown for this was one of the bugs.
- **Two delivery paths, because one is dead:**
  - **ntfy.sh** → topic in `grafana/alerting/signal-log-alerts.yaml` — **working, verified end to end**
  - **email** via host Postfix → Brevo — **BROKEN.** Brevo rejects with
    `525 5.7.1 Unauthorized IP address`; the relay's IP allowlist is set against a dynamic
    address. Postfix *accepts* the message and the sender logs success — delivery failure
    is only visible by inspecting the queue. **This is the owner's to fix** (authorise the
    IP, or move the relay to a static address).

---

## 7. Operating commands

```bash
# full deploy / apply config changes
cd /home/nikita/ai-blog/ansible && ansible-playbook deploy.yml

# force a publish cycle now
ansible-playbook deploy.yml -e force_cycle=true
# or, the production path:
systemctl --user start signal-log-cycle.service

# tests
docker compose run --rm --entrypoint sh builder -c 'cd /app && for t in curator/test_*.py; do python3 $t >/dev/null 2>&1; echo "$? $t"; done'
scripts/test-front-page.sh

# state
systemctl --user list-timers
grep -o 'METRIC .*' logs/cycle.log | tail -1
journalctl --user -u signal-log-cycle -n 50
```

**Rebuild the builder image after editing anything under `curator/`** — the playbook does
this via a context hash, but a bare `docker compose run` will happily execute stale code.
That mistake has already been made once and produced a silently image-less run.

---

## 8. Open items (2026-09-18)

| item | owner | state |
|---|---|---|
| Boot cycle runs before DNS: the user unit's `After=network-online.target` is `not-found` in the user manager; two zero-feed cycles measured (09-16, 09-18), both exit 0 | other session | DNS wait written on its branch, not merged |
| `cron-cycle.sh` mapping of `wait-for-deploy.sh` exit 4 (not a commit) and 5 (no run ever triggered); today both fall to `unverified`, exit 0. `ship_to_loki.py` must also treat `never_triggered` as `publish_failed` | cron-cycle.sh owner | codes handed over; waiting for the owner's OK |
| R2 credentials → interrupt test → physical independence of the backup; break-glass copy yes/no | **owner** | |
| First deferred LWN probes and ripened count | report ~2026-09-19 | |
| `rejected_by_category.too_old` for news categories after the next 12h+ outage | report | |
| Brevo IP authorisation | **owner** | blocks all email; ntfy path unaffected |
| ntfy topic is in a tracked, public file (`grafana/alerting/signal-log-alerts.yaml`); anyone who reads the repo can subscribe to or post on it | **owner** | not changed |
| Phase-two images (self-host + resize) | deferred | explicitly not to be built yet |
| PAT expiry 2026-12-04 | owner | |
| Jerusalem Post feed | owner's call | do not re-add unilaterally |

## 9. How the owner wants to be worked with

Stated directly, and consistently reinforced:

1. **Fewer words, more conclusions.** Efficiency over narration.
2. **"Show me the output, not the intention."** Every claim must come with the command
   output that proves it. Do not report what a change *should* do.
3. **Report per item, in the order asked.**
4. Act as a senior DevOps peer, not an assistant asking permission for routine work.
5. Do not reverse the owner's explicit decisions (rejected feeds, PAT scopes, etc.) — bring
   the evidence and let them decide.
6. Never touch DNS for `gs-bm.com`. **Live email (MX/SPF/DKIM) is on that domain; an NS
   change risks breaking it.** (`gs-bm.com` is the live domain; `gsbm.com` is a separate,
   broken zone — do not confuse them.)
7. Do not reset the Grafana admin password.

### The project's governing rule

> **A control is not in force until you have watched it refuse something.**

The README documents **six** instances where a control read correctly, was never observed
working, and did nothing: Ansible `stat: follow: true`; `… | tail -3 && echo "syntax OK"`
(tests `tail`'s exit code); Grafana `noDataState`; `smtplib` success ≠ delivered; a Netlify
redirect rule silently dropped as invalid; `wait-for-deploy.sh` unaware of the workflow's
path filter. Every guard in the system now has a matching negative test. **Continue this
practice — it is the single most valued thing about the work so far.**

Two specific traps that have caught this project more than once:
- **piping a command into `sed`/`tail`/`head` reports the pipe's exit code, not the
  command's.** Redirect instead.
- **`str.replace` that matches nothing silently no-ops.** Assert the old string is present
  before replacing.


---

## 10. Security review (2026-09-10)

Audited: secret handling, front-matter injection, XSS sinks, path traversal, SSRF, shell
hygiene, container privileges, CI workflow, dependencies, and exposed services.

### Fixed in this pass

**SSRF in the `og:image` fetch** — `curator/images.py::_from_og` passed the feed-supplied
article link straight to `urllib.request.urlopen` with no scheme or host check. Measured
before the fix:

```
file:///tmp/x.html            -> read and parsed, og:image returned
http://192.168.100.25:8080/   -> reachable from the builder, HTTP 200
```

A hostile or compromised publisher could read local files whose extension maps to
`text/html`, and sweep the LAN from inside the container. The response body never reaches
an attacker, but the extracted og:image URL **is published** — a blind probe with a
one-line exfiltration channel.

Fix (commit `9a50d0e`): `_safe_target` allows only `http`/`https` to a host whose **every**
resolved address is publicly routable, and `_GuardedRedirects` re-runs the check on each
hop (a public host can answer 302 with `Location: http://169.254.169.254/`).
`curator/test_images.py` watches it refuse `file://`, `ftp://`, `data:`, `gopher://`,
loopback, RFC1918, link-local, `localhost` by name, and malformed input — **and watches a
real publisher still pass**, because a guard that refuses everything looks identical to
one that works. Residual, accepted: DNS rebinding between the check and the connect.

### Checked and clean — with the evidence

| Area | Result |
|---|---|
| Secrets in tree and **full git history** | none (`github_pat`/`ghp_`/`sk-ant-`/`AKIA`/private keys) |
| `.env`, credential file perms | `600 nikita:nikita`, dir `700` |
| Tracked secret files | none; `.gitignore` covers `.env`, `*.pem`, `*.key` |
| **YAML front-matter injection** | not achievable — `_clean` collapses `\s+`, so a title of `Breaking\n---\npwned: true` lands as one line. Verified end-to-end |
| XSS | one `set:html`, fed by a **static template literal** with no interpolation; its sha256 is the CSP hash |
| Path traversal via slug | `slugify` strips to `[\w\s-]`, ASCII-folds, caps at 60 |
| Feed transport | **28/28 HTTPS** — no MITM injection point |
| `npm audit` | **0 vulnerabilities** |
| Container privileges | no docker socket, no `privileged`, no `cap_add`; builder runs `USER node` as `${BLOG_UID}:${BLOG_GID}` |
| GitHub Actions | minimal `permissions`, every action pinned to a full SHA, **no `${{ }}` interpolation inside `run:`** |
| nginx | `server_tokens off`, nosniff, X-Frame-Options, Referrer-Policy |
| **Postfix open relay** | **refused, watched**: `RCPT TO:<victim@gmail.com>` → `454 4.7.1 Relay access denied` |

### Open — the owner's call, not code defects

1. **Grafana `bot`/`[redacted]` on `0.0.0.0:3000`.** Verified: unauthenticated `/api/org` → 401,
   `bot:[redacted]` → 200. A four-digit repeated password on a network-listening service. Fine
   on an isolated LAN, not fine if that host is ever exposed. **Do not reset the admin
   password** — the owner said so explicitly.
2. **Unauthenticated services bound to `0.0.0.0`:** Loki `:3100`, Prometheus `:9090`,
   node-exporter `:9100`, Portainer `:9000` — all answered HTTP 200 without credentials.
   Bind to `127.0.0.1` or put them behind the proxy.
3. **Postfix `inet_interfaces = all`** listens on `0.0.0.0:25` with no need.
   `loopback-only` removes the surface; it is not an open relay either way.
4. **Python deps unpinned** (`anthropic>=1.0.0`, `feedparser>=6.0.11`, …). Every image
   rebuild silently takes the newest release. Pin them, or accept the drift knowingly.
5. **`img-src 'self' data: https:`** — images are hot-linked, so every publisher CDN sees
   each visitor's IP. This is exactly what phase-two image self-hosting closes.
6. **`set -uo pipefail` without `-e`** across all five scripts. Deliberate here (failures are
   caught explicitly and reported to Loki rather than aborting mid-cycle), but it means a
   missed exit-code check fails silently — the same shape as the `| tail` bug in the README
   table. Worth a pass to confirm every command's status is actually examined.
