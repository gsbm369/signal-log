---
title: "Agoda Replaces 72-Shard SQL Server Price Cache with DragonflyDB"
description: "Agoda migrated its 1.5 TB hotel Price Cache from 72 SQL Server shards to DragonflyDB to handle growing read and write volumes. The migration used staged dual reads, parity validation, gradual traffic shifting, and decent"
pubDate: 2026-09-14T13:48:00+00:00
addedAt: 2026-09-14T18:36:46.489706+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/09/agoda-price-cache-dragonflydb/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 67
score: 0.83329
readMinutes: 1
image: "https://res.infoq.com/news/2026/09/agoda-price-cache-dragonflydb/en/headerimage/generatedHeaderImage-1787939534250.jpg"
---

Agoda migrated its 1.5 TB hotel Price Cache from 72 SQL Server shards to DragonflyDB to handle growing read and write volumes. The migration used staged dual reads, parity validation, gradual traffic shifting, and decentralized failover detection. Agoda reports an approximately eightfold reduction in P99 read latency, with two DragonflyDB clusters providing high availability. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
