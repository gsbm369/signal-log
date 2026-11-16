---
title: "Reading JSON at 277 GB/s in Python"
description: "Many systems log their data as JSON, one record per line (NDJSON). GitHub, for example, publishes every public event on its site that way through GH Archive: about a gigabyte per hour."
pubDate: 2026-11-14T14:53:50+00:00
addedAt: 2026-11-14T15:48:30.534917+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/11/14/reading-json-at-277-gb-s-in-python/"
tags: ["python"]
heat: 100
score: 1.64383
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/11/superfastjson-feature-150x150.jpg"
hnPoints: 3
hnComments: 0
buzz: 22
---

Many systems log their data as JSON, one record per line (NDJSON). GitHub, for example, publishes every public event on its site that way through GH Archive: about a gigabyte per hour. Suppose you want to know which repositories received the most stars over eight hours. That is 7.6 GB of JSON, 2.2 million events. Continue reading Reading JSON at 277 GB/s in Python

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
