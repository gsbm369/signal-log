---
title: "This site writes itself every four hours"
description: "A short note on what signal.log is, what runs it, and what it deliberately will not do."
pubDate: 2026-09-05T08:00:00+00:00
source: "signal.log"
tags: ["meta", "automation", "astro"]
heat: 40
readMinutes: 2
---

Everything else on this site is machine-curated. This post is the exception — it is the
note left behind by whoever set the thing up.

## What runs

A cron job fires every four hours. It starts a container that does three things in order:

1. Pulls RSS from Hacker News, TechCrunch, Ars Technica, The Verge and MIT Technology Review.
2. Hands the batch to Claude with a fairly blunt editorial brief: drop the funding rounds,
   the rumours, the opinion columns, and anything where the headline is the entire story.
   Score what survives on whether it actually changes something.
3. Writes the survivors to Markdown, rebuilds the static site, and swaps the output into
   the directory nginx serves.

If the curation step fails, the build still runs against the posts already on disk. The
site does not go down because an API call timed out.

## What it will not do

The curator writes from headlines and feed blurbs — it has not read the full articles. So
it is instructed not to invent quotes, benchmark numbers, or named sources, and to write a
shorter piece when the source material is thin. **Every post links back to its original
source**, and that link is the authority, not the summary.

The `heat` score next to each story is the model's own estimate of significance. A quiet
day where nothing clears 60 is a correct outcome, not a broken one.

## The stack

Astro and Tailwind for the static site, Python and the Anthropic SDK for the curator,
Docker for both, Ansible to put it all on the box. Roughly four hundred lines total.
