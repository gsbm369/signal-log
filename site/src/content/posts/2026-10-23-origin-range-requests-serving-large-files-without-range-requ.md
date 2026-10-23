---
title: "Origin Range Requests: Serving large files without range-request tuning"
description: "Naive byte-range caching can waste gigabytes of origin bandwidth on small requests. We rebuilt our cache architecture in Pingora to coordinate partial fetches automatically, cutting R2 p99 latency in half."
pubDate: 2026-10-23T18:22:59+00:00
addedAt: 2026-10-23T21:18:36.348518+00:00
source: "Cloudflare"
category: company_eng
sourceUrl: "https://blog.cloudflare.com/origin-range-requests/"
tags: ["tech"]
heat: 71
score: 0.94428
readMinutes: 1
image: "https://blog.cloudflare.com/_emdash/api/media/file/01M5MZP89Y10XGACD5T6G2F398.png"
---

Naive byte-range caching can waste gigabytes of origin bandwidth on small requests. We rebuilt our cache architecture in Pingora to coordinate partial fetches automatically, cutting R2 p99 latency in half.

*Reproduced from the Cloudflare feed. No model was used to write this entry — follow the link for the full article.*
