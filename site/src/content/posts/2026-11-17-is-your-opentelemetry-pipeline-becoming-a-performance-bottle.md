---
title: "Is your OpenTelemetry pipeline becoming a performance bottleneck?"
description: "At Cloud Native Days Austria 2026, I presented a talk called How to Defeat OTel’s Silent Killer: The Performance Overhead, exploring a problem that is easy to overlook when building observability pipelines: the cost of c"
pubDate: 2026-11-17T12:21:00+00:00
addedAt: 2026-11-17T15:48:32.103279+00:00
source: "CNCF"
category: devops_linux
sourceUrl: "https://www.cncf.io/blog/2026/11/17/is-your-opentelemetry-pipeline-becoming-a-performance-bottleneck/"
tags: ["observability"]
heat: 80
score: 0.94551
readMinutes: 1
image: "https://www.cncf.io/wp-content/uploads/2026/11/image-12.png"
imageAlt: "Figure 1: OpenTelemetry Collector YAML configuration showing tail-based sampling with a 10-second decision window. The configuration retains traces with an ERROR status and probabilistically samples 5% of traces. The trace pipeline applies memory limiting, resource detection, span sanitization, GenAI normalization, tail sampling, and batching before exporting telemetry."
hnPoints: 0
hnComments: 0
buzz: 0
---

At Cloud Native Days Austria 2026, I presented a talk called How to Defeat OTel’s Silent Killer: The Performance Overhead, exploring a problem that is easy to overlook when building observability pipelines: the cost of collecting...

*Reproduced from the CNCF feed. No model was used to write this entry — follow the link for the full article.*
