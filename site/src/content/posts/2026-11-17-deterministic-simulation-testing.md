---
title: "Deterministic Simulation Testing"
description: "Distributed systems are hard to test because partial failures overlap with live traffic and the same fault can produce different execution traces on different runs. Unmesh Joshi describes how deterministic simulation tes"
pubDate: 2026-11-17T14:33:00+00:00
addedAt: 2026-11-17T15:48:32.105259+00:00
source: "Martin Fowler"
category: system_design
sourceUrl: "https://martinfowler.com/articles/deterministic-simulation-testing.html"
tags: ["tech"]
heat: 82
score: 0.99483
readMinutes: 1
hnPoints: 3
hnComments: 0
buzz: 22
---

Distributed systems are hard to test because partial failures overlap with live traffic and the same fault can produce different execution traces on different runs. Unmesh Joshi describes how deterministic simulation testing addresses this by replacing real clocks, networks, and storage with simulated components driven by a single-threaded execution loop. This allows simulating both hard failures and routine slowdowns&#x2014;such as network and disk latency spikes&#x2014;and more importantly makes every execution reproducible. This article explains the technique using a quorum key-value store as a running example, with code from Tickloom, a Java implementation of the approach. more…

*Reproduced from the Martin Fowler feed. No model was used to write this entry — follow the link for the full article.*
