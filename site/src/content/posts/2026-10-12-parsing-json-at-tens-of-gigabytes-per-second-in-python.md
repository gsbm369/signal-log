---
title: "Parsing JSON at tens of gigabytes per second… in Python"
description: "Python used to have limited parallelism, due to its global interpreter lock (GIL). Only one thread could run Python code at a time."
pubDate: 2026-10-12T13:06:39+00:00
addedAt: 2026-10-12T15:40:20.308002+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/10/12/parsing-json-at-tens-of-gigabytes-per-second-in-python/"
tags: ["python"]
heat: 100
score: 1.63267
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/10/pyjson-cover-150x150.jpg"
---

Python used to have limited parallelism, due to its global interpreter lock (GIL). Only one thread could run Python code at a time. Python 3.14 comes in a free-threaded version (python3.14t), without the global interpreter lock. Several threads can now run Python code at the same time. Let us pick a realistic problem. GitHub publishes Continue reading Parsing JSON at tens of gigabytes per second in Python

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
