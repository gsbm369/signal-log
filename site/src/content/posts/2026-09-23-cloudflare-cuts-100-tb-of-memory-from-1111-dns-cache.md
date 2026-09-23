---
title: "Cloudflare Cuts 100 TB of Memory from 1.1.1.1 DNS Cache"
description: "Cloudflare redesigned the in-memory representation of its Big Pineapple DNS cache, reducing the per-entry footprint by 56% and freeing roughly 100 TB of working-set memory across its fleet. The Rust-based changes also in"
pubDate: 2026-09-23T13:22:00+00:00
addedAt: 2026-09-23T19:10:58.640992+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/09/cloudflare-dns-cache/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare", "rust"]
heat: 81
score: 1.36926
readMinutes: 1
image: "https://res.infoq.com/news/2026/09/cloudflare-dns-cache/en/headerimage/generatedHeaderImage-1788755192272.jpg"
---

Cloudflare redesigned the in-memory representation of its Big Pineapple DNS cache, reducing the per-entry footprint by 56% and freeing roughly 100 TB of working-set memory across its fleet. The Rust-based changes also increased cache insertion throughput by 43% and reduced lookup latency by 19%, while enabling Cloudflare to increase cache capacity without additional memory. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
