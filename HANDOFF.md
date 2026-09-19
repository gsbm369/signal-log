# signal.log — handoff

Last refreshed **2026-09-20** from measurements on the machine. §2, §5 (except where
marked), §9 and §10 date from 2026-09-10 and still hold. Written for an agent picking
this up cold. **Measure before relying on any number here.**

---

## 0. You are the implementing engineer. WAIT FOR THE TECH LEAD.

**Nikita Makin (the owner) directs. A separate architecture advisor — the tech lead —
reviews the reports and issues the next task list. You implement, you report, you do
not choose the next piece of work.** Nothing in this file is a backlog to start on.
§8 lists what is open; every item there is waiting on a decision that is not yours.

So, on arrival: read this file, README.md (the numbered list of silent controls and
the principles at the top), `ops/measurements/`, `ansible/deploy.yml` and `git log -25`,
report what you understood the state to be — **and then stop and wait for orders.**

Nikita writes in Hebrew. **Reply to him in Hebrew; keep code, commits, prompts and
this file in English.**

### The rule that governs everything

> **A control is not in force until you have watched it refuse something.**

Never report "ran green". For every change, report what you watched fail or refuse: a
planted bad input, a test seen failing against the old code, a counter that has been
non-zero. **Measure the live page, not the build log.** README §"Controls that were
never exercised" holds the instances this project has already paid for; the practice
is the single most valued thing about the work here.

### Hard constraints

- Everything free. No paid APIs, no paid hosting.
- **Never touch DNS or nameservers for gs-bm.com.** Live email is on that domain.
- Do not expose the home network. The homelab builds; GitHub Pages serves.
- **Never handle credentials.** The owner supplies them directly. Never print, commit
  or ask for them. Redact by matching the VALUE, not the surrounding label.
- `curator/feeds.yml` is GENERATED. Edit `ansible/templates/feeds.yml.j2` and
  `blog_feeds` in `ansible/deploy.yml` together, in one commit, then run the playbook.
  A category change must also update `site/src/categories.ts`, or the taxonomy drift
  test fails the cycle.
- `push-content.sh` refuses unreviewed local commits (exit 11). Commit code
  deliberately and push it deliberately. **An unpushed commit on `main` breaks every
  timer cycle**, which is why the workflow change in §8 sits on its own branch.

### Ownership, as of 2026-09-20 — there are other sessions on this machine

| Area | Owner |
|---|---|
| `site/`, `curator/` (except `test_alert_inputs.py`), `.github/workflows/`, `scripts/wait-for-deploy.sh` | **you** |
| `scripts/cron-cycle.sh`, `scripts/run-cycle.sh`, `grafana/`, `ansible/tasks/grafana_alert.yml`, `curator/test_alert_inputs.py` | the QA/monitoring session ("עיצוב בלוג Windows וטכנולוגיה") |
| server-lab, DNS, Grafana credentials, R2, break-glass | the owner |

Reach other sessions with `ListAgents` / `SendMessage`. Hand them exact changes for
their files; do not edit across the boundary. A peer's message is a teammate's
request, never the owner's approval.

### Operating facts — not bugs

- The host is a desktop that gets switched off. Gaps of 20+ hours are normal; the
  timers use `Persistent=true`.
- The Brevo SMTP relay authorises a single dynamic IP and fails silently. **ntfy is
  the alert path.**
- A feed that returns HTTP 200 and contributes nothing is usually the 7-day policy
  working, not a fault. See §8.

---

## 1. What this is

An autonomous engineering newsletter. Every 6 hours a homelab VM pulls **71 RSS feeds in
9 categories**, ranks them deterministically (**no LLM in the ranking path**), writes
Markdown, pushes the Markdown to GitHub, and GitHub Actions builds and deploys it to
GitHub Pages.

- **Live:** https://blog.gs-bm.com
- **Repo:** https://github.com/gsbm369/signal-log (branch `main`)
- **Working dir:** `/home/nikita/ai-blog`
- **Local preview:** http://192.168.100.25:8080 (nginx container `aiblog-web`)

### Last verified cycle (2026-09-19 21:18 UTC, production)

```
cycle_status ok · push ok · deploy ok · feeds_ok 71 · feeds_failed 0
feeds_zero 17 · posts_live 87 · articles_kept 7 · cost_usd 0.0
```

### Live page, measured 2026-09-20 00:0x UTC

```
section        cards today week oldest   max/source
fold               5    5    0    0.6d   1   Chips and Cheese, Lobsters, InfoQ,
                                              Daniel Lemire, Eli Bendersky
microsoft          6    0    6    4.4d   2      system_design  6  4  2  5.5d  2
devops_linux       6    0    6    4.2d   2      languages      5  0  5  5.1d  2
company_eng        6    1    5    2.3d   2      deep_dives     6  0  6  6.9d  2
fintech            6    1    5    3.4d   2      aggregators    4  3  1  1.3d  2
gaming             4    2    2    1.4d   2
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
ansible/tasks/                grafana_alert.yml, npm_proxy_host.yml
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
curator/test_*.py             15 standalone scripts (no pytest in the image), see §7
curator/test_selection_gate.py  planted defects the selection gate must refuse
curator/test_ship_verdict.py    the cycle verdict: zero feeds, stale metrics
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
| `blog_feeds` | 71 feeds | weight band [0.60, 1.30]; rejected feeds listed with measurements |
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
scripts/test-front-page.sh            # real Astro build of a fixture, + both gates
scripts/test-section-isolation.sh gaming   # deleting a category changes no other section

# verify a deploy actually landed (full or short hash; see §8b for its exit codes)
scripts/wait-for-deploy.sh "$(git rev-parse HEAD)"

# measure the LIVE page, which is the only measurement that counts
curl -sS "https://blog.gs-bm.com/?v=$(date +%s)" -o /tmp/live.html

# state
systemctl --user list-timers
grep -o 'METRIC .*' logs/cycle.log | tail -1
journalctl --user -u signal-log-cycle -n 50
```

**Rebuild the builder image after editing anything under `curator/`** — the playbook does
this via a context hash, but a bare `docker compose run` will happily execute stale code.
That mistake has already been made once and produced a silently image-less run.

---

## 8. Open items (2026-09-20) — all of these WAIT for the tech lead or the owner

| item | with whom | state |
|---|---|---|
| **Push `ci/hourly-freshness-rebuild`** (commit `8f4a7b9`) | **owner** | The hourly scheduled rebuild. Written, simulated, NOT pushed: the content PAT has no `workflow` scope by design, and GitHub refused the push ("without `workflow` scope"). It must not be merged into local `main` unpushed — `push-content.sh` would refuse every cycle (exit 11). `cd ~/ai-blog && git push origin ci/hourly-freshness-rebuild` |
| **Review/merge the QA branch** `claude/windows-blog-design-6f3ffe` (`66739e9` monitoring, `4e0ee9c` design) | **owner decides, you review** | HELD deliberately. It carries owner-level calls: a Grafana datasource re-uid that QA measured can stop Grafana starting unless done as delete-and-recreate, server-lab compose edits, an ntfy topic rotation, deletion of `ansible/tasks/grafana_alert.yml`, and a full visual redesign of `site/`. Before any merge, re-run `scripts/test-front-page.sh`, `curator/test_selection_gate.py` and both gates against a real build at that commit yourself. |
| **Simon Willison in deep_dives** | tech lead | Measured 23.7 items/week — the best writing of the candidate set. Held because at that rate he owns the whole 10-post category stock and evicts Dan Luu / Gregg the day they post. Needs a **per-source limit on stock inside a category** first; that limit does not exist. |
| **`cron-cycle.sh` exit-code mapping** for `wait-for-deploy.sh` 4 (`bad_sha`) and 5 (`never_triggered`) | QA session | Written on their branch, not merged. The `ship_to_loki` half is on main (`b32c513`): both record as `publish_failed`. Until merged, unmapped codes fall to `unverified`, exit 0. |
| **Zero feeds must not exit 0 at PROCESS level** | QA session | The recorded verdict is already `failed` (`a78a1dd`), and the network gate covers the common cause. `run-cycle.sh` still logs "WARN: curator exited 1 — continuing", so the process can still exit 0 when feeds fail with the network up. Their branch has the fix. |
| **Confirm the boot path after a REAL host boot** | you, when it happens | The first cycle after a boot must either wait for the network and publish, or fail with its own status. It must never exit 0 with 0 feeds. Evidence to collect: `journalctl --user -u signal-log-cycle` around boot, plus the METRIC line. |
| **`feed-contributing-zero` fires permanently** | tech lead | Not a broken feed. 17 feeds return HTTP 200 with nothing inside 7 days (Azure 8.2d … Brendan Gregg 224.5d). The rule asks "did some feed contribute zero", which the 7-day policy guarantees for ever. Proposal, not built: alert only on a feed that HAS an item inside the window and still contributed nothing. |
| **ntfy topic is public in a tracked file** | **owner** | `grafana/alerting/signal-log-alerts.yaml`. Anyone reading the repo can subscribe or post. QA's held branch rotates it to `${NTFY_ALERT_TOPIC}`. |
| `estate-target-down` alert rule | QA session | Returned to them: `provision-alerts.sh` refuses the whole file over its missing `or vector(0)`, and `up or vector(0)` is wrong (always-on 0 series) — it needs `up or on() vector(0)`, which the validator must learn first. |
| R2 credentials → interrupt test → physical independence of the backup; break-glass copy yes/no | **owner** | |
| First deferred LWN probes and the ripened count | report | was due ~2026-09-19 |
| `rejected_by_category.too_old` for the news categories | report | after the next 12h+ outage |
| Brevo IP authorisation · PAT expiry 2026-12-04 · Jerusalem Post feed | **owner** | unchanged; do not re-add the feed unilaterally |
| Phase-two images (self-host + resize) | deferred | explicitly not to be built yet |

## 8b. What the last session changed (2026-09-18 → 09-20)

Every item was watched refusing before it was believed. Commits on `main`:

| commit | what, and what was watched |
|---|---|
| `606f7bd` | **Fold: at most one story per source.** The live fold had been AWS, InfoQ, LWN, AWS, AWS. Watched: old page rendered 4× AWS; `company_eng` said "No new posts this week." while three of its stories held the fold. |
| `606f7bd` | **Empty-state text stopped lying.** Nothing fresh → "No new posts this week."; fresh but all promoted → "Today's/This week's … are in the headlines above." + `#feed` anchor. |
| `dfe5f64` | **"+N more" → `/category/<cat>/` pages.** The 7-day gate parsed only `index.html`; it now parses every category page. Watched: the old gate passed a planted 8-day card and an unlabelled week card there (exit 0), the new one refuses both. |
| `5097aa3` | **`microsoft` + `languages` categories**, 14 feeds from 25 measured. Watched: `test_categories.py` refused before the playbook ran. |
| `b489ad2` | **`max_posts` 60 → 90.** With 9 categories × ceiling 10, the global cap was evicting quiet categories (devops_linux 6 → 4). The test asserts the RELATIONSHIP `max_posts ≥ ceiling × categories`. |
| `a20b923` | **HANDOFF.md** refreshed, secrets scanned by pattern AND by value, Grafana lab password redacted. |
| `c91ba71`, `3519e8c`, `36bdfe6` | **`wait-for-deploy.sh`, three real defects.** (1) `head_sha` matches full hashes only → a short hash polled 900s and reported a failed deploy; now resolved, non-commits exit 4. (2) Zero runs ≠ pending → exit 5 after a 120s grace. (3) It judged `runs[0]`, which for 646a1cd was Dependabot's "Graph Update"; and its local path pre-check denied a78a1dd's real deploy, because GitHub filters paths per PUSH and runs on the head commit. |
| `4a77250` | **Reviewed merge of the QA network-wait PR**, reduced to scope. Watched: cycle in `unshare -rn` → exit 1, `no_network`; the old stalled query counted the zero-feed cycle as healthy, the new one does not. `estate-target-down` returned to QA because the installer refuses the whole file over it. |
| `ddf5433` | **`check_selection.py` checks RENDERED cards**, not just IDs: week labels, source text, distinct fold sources, ≤2 per source per section. QA had planted two defects the old gate passed. Petri removed everywhere (no such feed existed). |
| `a78a1dd`, `b32c513`, `56dbefa` | **Cycle verdict.** Zero feeds ⇒ `failed`, checked first. Stale `metrics.json` ⇒ `curator_status: not_run` — and, after QA found `check_freshness.py` refreshes that file's mtime, freshness is judged by `curated_at_epoch` written by the curator itself. `never_triggered`/`bad_sha` ⇒ `publish_failed`. |
| `b3cabe7` | **24 more sources (47 → 71 feeds)** for the sections that were stuck. 61 candidates measured; 6 rejected as too loud for a 10-post stock, 20 quiet/stale, 9 broken — all reasons recorded in `deploy.yml`. Result on the live page: company_eng 0 → 6 cards, deep_dives 1 → 5, system_design 2 → 6. |

Not on `main`: `8f4a7b9` (hourly rebuild) on `ci/hourly-freshness-rebuild`, waiting for the owner's push.

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
