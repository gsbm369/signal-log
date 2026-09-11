---
title: "Fixing UUIDv7 (for database use-cases)"
description: "Fixing UUIDv7 (for database use-cases) How do I even balance a V7? RFC9562 defines UUID Version 7."
pubDate: 2025-10-22T00:00:00+00:00
addedAt: 2026-09-11T11:03:46.193154+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/10/22/uuidv7.html"
tags: ["tech"]
heat: 46
score: 0.27233
readMinutes: 1
---

Fixing UUIDv7 (for database use-cases) How do I even balance a V7? RFC9562 defines UUID Version 7. This has made a lot of people very angry and been widely regarded as a bad move 1 . More seriously, UUIDv7 has received a lot of criticism, despite seemingly achieving what it set out to do. The legitimate criticism seems to be on a few points. V7 UUIDs: Leak information (namely the server timestamp). Are a bad choice for cases where security or operational requirements require UUIDs that are hard to guess, because they have less entropy. Introduce correlated behavior between datacenters, regions, and installations of applications, increasing the probability of triggering bugs across failure boundaries. Are hard to present in UIs, because the E6EE7F40... format doesn’t work, because of deterministic first digits. Before thinking about how we might fix these issues, let’s understand why folk

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
