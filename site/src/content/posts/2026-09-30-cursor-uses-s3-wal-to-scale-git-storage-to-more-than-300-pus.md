---
title: "Cursor Uses S3 WAL to Scale Git Storage to More than 300 Pushes per Second"
description: "Cursor has introduced Continuity, a Git storage architecture that uses an S3 backed write ahead log as the source of truth. The design turns local NVMe repositories into warm caches and separates replica coordination fro"
pubDate: 2026-09-30T13:47:00+00:00
addedAt: 2026-09-30T15:17:36.068138+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/09/cursor-continuity-git-storage/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 59
score: 0.84473
readMinutes: 1
image: "https://www.infoq.com/styles/static/images/logo/logo_bigger.jpg"
---

Cursor has introduced Continuity, a Git storage architecture that uses an S3 backed write ahead log as the source of truth. The design turns local NVMe repositories into warm caches and separates replica coordination from consistency. Cursor reports linear read scaling with up to 100 replicas and more than 300 pushes per second with S3 Express One Zone in synthetic tests. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
