---
title: "Parsing compressed JSON at 40 GB/s"
description: "A common way to store JSON data is to write one document per line. We call it NDJSON or JSON Lines."
pubDate: 2026-10-01T03:10:29+00:00
addedAt: 2026-10-01T20:05:21.114831+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/10/01/parsing-compressed-json-at-40-gb-s/"
tags: ["tech"]
heat: 68
score: 0.93261
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/10/jsonstream-cover-150x150.jpg"
imageAlt: "Parsing compressed JSON at 40 GB/s"
---

A common way to store JSON data is to write one document per line. We call it NDJSON or JSON Lines. Log files, database exports and machine-learning datasets often come in this format. The files can be large, so we may compress them. {"id":1,"active":true,"user":{"name":"user_1","tags":["guest"]},"score":-3862,"note":"..."} {"id":2,"active":false,"user":{"name":"user_2","tags":["staff","admin"]},"score":8123,"note":"..."} How fast can you read such a file? I wrote Continue reading Parsing compressed JSON at 40 GB/s

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
