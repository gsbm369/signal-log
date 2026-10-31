---
title: "Cloudflare’s Post-Quantum GeoKey Manager Enters Closed Beta Without Attribute-Based Encryption"
description: "Cloudflare has moved a post-quantum rebuild of GeoKey Manager into closed beta, guarding geo-fenced keys with hybrid ML-KEM-768 and X25519 instead of the attribute-based encryption used since 2022. Keys live only in kern"
pubDate: 2026-10-31T19:56:00+00:00
addedAt: 2026-10-31T22:18:35.064906+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/cf-pq-geokey-manager/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare", "kernel"]
heat: 100
score: 1.38882
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/cf-pq-geokey-manager/en/headerimage/generatedHeaderImage-1793376907936.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

Cloudflare has moved a post-quantum rebuild of GeoKey Manager into closed beta, guarding geo-fenced keys with hybrid ML-KEM-768 and X25519 instead of the attribute-based encryption used since 2022. Keys live only in kernel memory on verified regional servers, and any failed check rejects the request, a fail-closed choice practitioners ask could cause a regional outage. GA is planned for Q1 2027. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
