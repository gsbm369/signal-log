---
title: "Faster Python startup with lazy imports"
description: "When a Python program starts, it needs to load all its dependencies (import). With the upcoming version of Python, it is possible to use lazy imports instead."
pubDate: 2026-10-09T03:15:06+00:00
addedAt: 2026-10-10T16:16:16.937446+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/10/09/faster-python-startup-with-lazy-imports/"
tags: ["python"]
heat: 80
score: 1.41631
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/10/lazy-import-cover-150x150.jpg"
---

When a Python program starts, it needs to load all its dependencies (import). With the upcoming version of Python, it is possible to use lazy imports instead. lazy import json lazy from decimal import Decimal In this instance, the name json is no longer the module, but a mere placeholder object. The actual import only Continue reading Faster Python startup with lazy imports

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
