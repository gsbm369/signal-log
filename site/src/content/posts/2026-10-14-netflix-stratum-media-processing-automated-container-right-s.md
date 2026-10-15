---
title: "Netflix Stratum Media Processing: Automated Container Right-Sizing"
description: "By Violetta Pidvolotska and Naveen Mareddy Stratum is Netflix’s internal serverless media processing platform, shaped by over a decade of experience developing large-scale distributed systems. It powers a wide range of m"
pubDate: 2026-10-14T19:48:20+00:00
addedAt: 2026-10-15T03:18:05.350669+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/netflix-stratum-media-processing-automated-container-right-sizing-ddf9aa68a801?source=rss----2615bd06b42e---4"
tags: ["embedding"]
heat: 77
score: 1.01912
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*_8R96y0lKNJmgSs1qZ0qTw.png"
---

By Violetta Pidvolotska and Naveen Mareddy Stratum is Netflix’s internal serverless media processing platform, shaped by over a decade of experience developing large-scale distributed systems. It powers a wide range of media workloads — including encoding, packaging, inspection, and quality scoring — behind playback, advertising, studio workflows, AI embeddings, and more. Engineers develop Stratum functions by packaging application code and OS dependencies into OCI images. Stratum then schedules these containers as batch jobs on Netflix’s Titus compute platform, with upstream services triggering function executions. Every day, Stratum manages hundreds of thousands of containers across bursty, high-throughput, and latency-sensitive workloads. As Netflix’s core media processing platform, this load needs to scale as new content formats enter the catalog, such as podcasts , live events , spo

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
