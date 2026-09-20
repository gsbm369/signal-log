---
title: "Cloudflare Measures Origin TLS Preferences, Cutting Handshake Retries from 52% to 3.7%"
description: "Cloudflare has replaced its static X25519 guess for origin TLS handshakes with per-origin measurement. HelloRetryRequests on scanned origins fell from roughly 52% to 3.7%, removing over 150 ms from p90 latency."
pubDate: 2026-09-20T08:15:00+00:00
addedAt: 2026-09-20T09:17:34.633163+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/09/cloudflare-automatic-key-exchang/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare"]
heat: 100
score: 1.39648
readMinutes: 1
image: "https://res.infoq.com/news/2026/09/cloudflare-automatic-key-exchang/en/headerimage/generatedHeaderImage-1789633148686.jpg"
---

Cloudflare has replaced its static X25519 guess for origin TLS handshakes with per-origin measurement. HelloRetryRequests on scanned origins fell from roughly 52% to 3.7%, removing over 150 ms from p90 latency. Post-quantum connections completing in one round trip rose from 0% to 99.2%, though only 12.8% of origins support it. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
