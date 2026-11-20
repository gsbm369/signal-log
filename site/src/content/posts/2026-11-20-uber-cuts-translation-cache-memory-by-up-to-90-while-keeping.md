---
title: "Uber Cuts Translation Cache Memory by up to 90% While Keeping P99 Latency Below 1 MS"
description: "Uber redesigned its Go-based translation cache to reduce its initial memory footprint by more than 90% while maintaining a cache hit rate above 99.9% and p99 disk-backed cache miss latency below 100 microseconds. The hyb"
pubDate: 2026-11-20T14:38:00+00:00
addedAt: 2026-11-20T15:48:35.109011+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/uber-go-translation-cache/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 67
score: 0.8459
readMinutes: 1
image: "https://www.infoq.com/styles/static/images/logo/logo_bigger.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

Uber redesigned its Go-based translation cache to reduce its initial memory footprint by more than 90% while maintaining a cache hit rate above 99.9% and p99 disk-backed cache miss latency below 100 microseconds. The hybrid architecture combines in-memory keys and frequently accessed values with disk-backed storage, reducing garbage-collection overhead and memory consumption. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
