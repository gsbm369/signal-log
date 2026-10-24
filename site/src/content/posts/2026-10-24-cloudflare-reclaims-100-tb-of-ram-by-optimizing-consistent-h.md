---
title: "Cloudflare Reclaims 100 TB of RAM by Optimizing Consistent Hashing"
description: "Cloudflare recently documented how it reduced the memory footprint of its internal load-balancing service by more than 100 TB by optimizing the Rust implementation of consistent hashing in pingora-ketama. The changes com"
pubDate: 2026-10-24T08:10:00+00:00
addedAt: 2026-10-24T09:18:27.510832+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/cloudflare-hashing-optimization/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare", "rust"]
heat: 100
score: 1.39592
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/cloudflare-hashing-optimization/en/headerimage/generatedHeaderImage-1790410589563.jpg"
---

Cloudflare recently documented how it reduced the memory footprint of its internal load-balancing service by more than 100 TB by optimizing the Rust implementation of consistent hashing in pingora-ketama. The changes compacted hash-ring entries and used statistical analysis of hash distribution and collision rates to reduce the number of hashes per backend by about 90%. By Renato Losio

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
