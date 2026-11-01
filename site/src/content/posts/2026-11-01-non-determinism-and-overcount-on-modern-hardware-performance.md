---
title: "Non-Determinism and Overcount on Modern Hardware Performance Counter Implementations"
description: "Abstract: Ideal hardware performance counters provide exact deterministic results. Real-world performance monitoring unit (PMU) implementations do not always live up to this ideal."
pubDate: 2026-11-01T07:55:47+00:00
addedAt: 2026-11-01T10:18:30.030503+00:00
source: "Lobsters"
category: aggregators
sourceUrl: "https://web.eece.maine.edu/~vweaver/projects/deterministic/deterministic_counters.pdf"
tags: ["tech"]
heat: 65
score: 0.68439
readMinutes: 1
hnPoints: 41
hnComments: 2
buzz: 60
---

Abstract: Ideal hardware performance counters provide exact deterministic results. Real-world performance monitoring unit (PMU) implementations do not always live up to this ideal. Events that should be exact and deterministic (such as retired instructions) show run-to-run variation and overcount on x86_64 machines, even when run in strictly controlled environments. These effects are non-intuitive to casual users and cause difficulties when strict determinism is desirable, such as when implementing deterministic replay or deterministic threading libraries. We investigate eleven different x86_64 CPU implementations and discover the sources of divergence from expected count totals. Of all the counter events investigated, we find only a few that exhibit enough determinism to be used without adjustment in deterministic execution environments. On these machines it appears that the iret interr

*Reproduced from the Lobsters feed. No model was used to write this entry — follow the link for the full article.*
