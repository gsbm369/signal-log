---
title: "A performance trap: when store forwarding fails"
description: "A store does not go straight into the cache. Waiting for that write would stall the processor."
pubDate: 2026-11-05T13:06:20+00:00
addedAt: 2026-11-05T16:18:32.669249+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/11/05/a-performance-trap-when-store-forwarding-fails/"
tags: ["tech"]
heat: 66
score: 0.98688
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/11/storeforwarding-feature-150x150.jpg"
imageAlt: "A store sits in the store buffer. A later load can take those bytes from the buffer instead of waiting for the data cache."
hnPoints: 3
hnComments: 0
buzz: 22
---

A store does not go straight into the cache. Waiting for that write would stall the processor. It sits in a store buffer, and a later load can take its bytes from that buffer. That is store forwarding. Forwarding works when the load is the same size as the store, or smaller and completely inside Continue reading A performance trap: when store forwarding fails

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
