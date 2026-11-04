---
title: "How we halved DNS build delay and cut memory use by 85%"
description: "Zone setting changes used to rebuild entire DNS zones, even ones with tens of millions of records. Here is how we built a planner that picks the smallest safe build, cutting full builds by 40%, peak memory by 85%, and ha"
pubDate: 2026-11-02T14:00:00+00:00
addedAt: 2026-11-02T16:18:31.628300+00:00
source: "Cloudflare"
category: company_eng
sourceUrl: "https://blog.cloudflare.com/dns-targeted-zone-builds/"
tags: ["tech"]
heat: 67
score: 0.94549
readMinutes: 1
image: "https://blog.cloudflare.com/_emdash/api/media/file/01M6427MMYH94N030R2BSS8Z72.01M6427NA85VEN498BC5RPEDXK.png"
hnPoints: 196
hnComments: 80
buzz: 85
---

Zone setting changes used to rebuild entire DNS zones, even ones with tens of millions of records. Here is how we built a planner that picks the smallest safe build, cutting full builds by 40%, peak memory by 85%, and halving build delay.

*Reproduced from the Cloudflare feed. No model was used to write this entry — follow the link for the full article.*
