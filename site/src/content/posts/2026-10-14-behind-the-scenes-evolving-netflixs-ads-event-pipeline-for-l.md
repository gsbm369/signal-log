---
title: "Behind the Scenes: Evolving Netflix’s Ads Event Pipeline for Live — Part II"
description: "By Yogesh Nagarur Introduction In Part 1 of this series , we shared how Netflix built the Ads Event pipeline and approached it as a system design problem: replacing fragmented pipelines with a centralized collection, enr"
pubDate: 2026-10-14T19:51:35+00:00
addedAt: 2026-10-15T09:18:01.001349+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb?source=rss----2615bd06b42e---4"
tags: ["tech"]
heat: 100
score: 0.87539
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*LkXsONCex0Q1KvttewSZ1w.png"
---

By Yogesh Nagarur Introduction In Part 1 of this series , we shared how Netflix built the Ads Event pipeline and approached it as a system design problem: replacing fragmented pipelines with a centralized collection, enrichment, and a standard data contract. The result was Ads Event Publisher, the system that collects ad telemetry from client devices, enriches it with the context of the ad that was actually served, and publishes a single, unified stream of ad events to every downstream consumer: frequency capping, metrics, billing, measurement partners, and reporting. Any member viewing or account details that move through this pipeline end-to-end are encrypted and handled in accordance with Netflix’s strict privacy and security practices to safeguard member PII. If ad serving is the “brain” and ad events are the “heartbeats” that feed it, then enrichment is what gives each heartbeat its

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
