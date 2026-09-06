---
title: "How this site stays current"
description: "What runs this site, why no model decides what appears, and what it deliberately will not do."
pubDate: 2026-09-05T08:00:00+00:00
source: "signal.log"
tags: ["meta", "automation", "astro"]
heat: 40
readMinutes: 2
---

Everything else here arrives automatically. This post is the exception — a note from
whoever set it up.

## What runs

A cron job fires every four hours. It starts a container that does three things in order:

1. Pulls RSS from Hacker News, TechCrunch, Ars Technica, The Verge, IEEE Spectrum and
   MIT Technology Review.
2. Ranks the batch with a deterministic heuristic — no model. Exponential recency decay
   (36h half-life), a narrow per-source weight, topic relevance read from the **headline**
   rather than the body, cross-source deduplication, a noise filter for routine digests,
   and a cap so one prolific feed cannot dominate.
3. Writes the survivors to Markdown and pushes them to GitHub. Actions builds the site
   and deploys it to Pages.

If a feed is unreachable it is logged and skipped. If the build fails, nothing is pushed
and the live site is untouched. A push that succeeds but never deploys is reported as a
failure, not a success.

## What it will not do

Summaries are the feed's own description, not generated text. **Every post links back to
its original source**, and that link is the authority.

The `heat` score is the ranker's score for that story relative to the best in its run. A
quiet day where nothing scores highly is a correct outcome, not a broken one.

Summarisation is pluggable — a local model or a hosted one can be switched on with one
variable — but ranking never uses a model in any mode, so the choice changes prose only,
never which stories appear.

## The stack

Astro and Tailwind for the site, Python for the ranker, Docker for the build, Ansible to
deploy it, GitHub Actions to publish it. The ranking heuristic is covered by a golden test
that freezes the exact output order, so a change to any constant has to be re-approved
rather than drifting.
