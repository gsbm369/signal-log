---
title: "What Does a Database for SSDs Look Like?"
description: "What Does a Database for SSDs Look Like? Maybe not what you think."
pubDate: 2025-12-15T00:00:00+00:00
addedAt: 2026-09-11T10:20:27.667926+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/12/15/database-for-ssd.html"
tags: ["postgres", "sqlite"]
heat: 78
score: 0.38562
readMinutes: 1
---

What Does a Database for SSDs Look Like? Maybe not what you think. Over on X, Ben Dicken asked : What does a relational database designed specifically for local SSDs look like? Postgres, MySQL, SQLite and many others were invented in the 90s and 00s, the era of spinning disks. A local NVMe SSD has ~1000x improvement in both throughput and latency. Design decisions like write-ahead logs, large page sizes, and buffering table writes in bulk were built around disks where I/O was SLOW, and where sequential I/O was order(s)-of-magnitude faster than random. If we had to throw these databases away and begin from scratch in 2025, what would change and what would remain? How might we tackle this question quantitatively for the modern transaction-orientated database? But first, the bigger picture. It’s not only SSDs that have come along since databases like Postgres were first designed. We also ha

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
