---
title: "Locality, and Temporal-Spatial Hypothesis"
description: "Locality, and Temporal-Spatial Hypothesis Good fences make good neighbors? Last week at PGConf NYC, I had the pleasure of hearing Andres Freund talking about the great work he’s been doing to bring async IO to Postgres 1"
pubDate: 2025-10-05T00:00:00+00:00
addedAt: 2026-09-11T10:52:16.178890+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/10/05/locality.html"
tags: ["linux", "postgres"]
heat: 49
score: 0.29335
readMinutes: 1
---

Locality, and Temporal-Spatial Hypothesis Good fences make good neighbors? Last week at PGConf NYC, I had the pleasure of hearing Andres Freund talking about the great work he’s been doing to bring async IO to Postgres 18. One particular result caught my eye: a large difference in performance between forward and reverse scans, seemingly driven by read ahead 1 . The short version is that IO layers (like Linux’s) optimize performance by proactively pre-fetching data ahead of the current read point in a file, so it’s already cached when needed. Notably, most of these systems don’t do this backwards. This leads to a big difference in performance between forward scans (where the pages are already in the cache when they’re needed) and backward scans (where the database needs to block on IO to fetch the next page). This lead me to thinking more about a particular hypothesis behind many database

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
