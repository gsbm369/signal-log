---
title: "Cloudflare Opens Quicksilver to Customers as Workers KV Instant, Inside a 1 MB Envelope"
description: "Cloudflare has put Quicksilver, the internal key-value store behind nearly every request it serves, into private beta as a Workers KV mode. Reads resolve in 1.62 ms at p99 against 287 ms for classic KV."
pubDate: 2026-10-28T08:57:00+00:00
addedAt: 2026-10-28T10:18:29.535254+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/workers-kv-instant/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare"]
heat: 100
score: 1.39467
readMinutes: 1
image: "https://www.infoq.com/styles/static/images/logo/logo_bigger.jpg"
---

Cloudflare has put Quicksilver, the internal key-value store behind nearly every request it serves, into private beta as a Workers KV mode. Reads resolve in 1.62 ms at p99 against 287 ms for classic KV. The constraints decide the use case: 10,000 keys, one megabyte per namespace, and one write per namespace per second. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
