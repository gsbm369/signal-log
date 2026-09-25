---
title: "Partition Finalization in Pinterest’s Next-Generation DB Ingestion Framework"
description: "Qianrui Zhang | Sr Software Engineer, Logging Platform Kanchi Masalia | Software Engineer II, Stream Processing Platform Liang Mou | Sr Staff Software Engineer, Logging Platform Yi Pan | Principal Engineer, Agent Platfor"
pubDate: 2026-09-25T15:01:03+00:00
addedAt: 2026-09-25T15:17:34.417892+00:00
source: "Pinterest Engineering"
category: company_eng
sourceUrl: "https://medium.com/pinterest-engineering/partition-finalization-in-pinterests-next-generation-db-ingestion-framework-4c7da6e4cc8f?source=rss----4c5a5f6279b6---4"
tags: ["tech"]
heat: 66
score: 0.89949
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*RYnr5fSTAfCGM8R9wcHr_w.png"
---

Qianrui Zhang | Sr Software Engineer, Logging Platform Kanchi Masalia | Software Engineer II, Stream Processing Platform Liang Mou | Sr Staff Software Engineer, Logging Platform Yi Pan | Principal Engineer, Agent Platform Introduction This is the third post in our series on Pinterest’s next-generation database ingestion framework. Part 1 introduced the DB ingestion framework built on Kafka, Flink, Spark, and Iceberg, and Part 2 covered automated schema evolution. This post tackles another challenge in migrating downstream customers to the new ingestion framework: knowing when data is complete enough to read. We’ll walk through that data completeness challenge and how we solve it: what “partition finalization” means, why it matters to downstream customers, how we built a unified mechanism to generate partition finalization markers, and how those markers are consumed. We’ll also look at ho

*Reproduced from the Pinterest Engineering feed. No model was used to write this entry — follow the link for the full article.*
