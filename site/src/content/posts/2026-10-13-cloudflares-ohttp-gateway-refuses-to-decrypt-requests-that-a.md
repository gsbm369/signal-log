---
title: "Cloudflare’s OHTTP Gateway Refuses to Decrypt Requests That Arrive Through Cloudflare"
description: "Cloudflare has opened a closed beta of its OHTTP Gateway, a managed endpoint that decrypts Oblivious HTTP requests for an origin. The design choice drawing attention is a refusal: the Gateway will not decrypt requests ar"
pubDate: 2026-10-13T06:44:00+00:00
addedAt: 2026-10-13T16:25:24.324443+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/cloudflare-ohttp-gateway/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare"]
heat: 91
score: 1.34755
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/cloudflare-ohttp-gateway/en/headerimage/generatedHeaderImage-1791773464365.jpg"
---

Cloudflare has opened a closed beta of its OHTTP Gateway, a managed endpoint that decrypts Oblivious HTTP requests for an origin. The design choice drawing attention is a refusal: the Gateway will not decrypt requests arriving from Cloudflare Workers or from hosts proxied through Cloudflare, because that would put client identifiers and request contents in the same hands. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
