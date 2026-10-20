---
title: "Pinterest Uses Event Time Watermarks to Finalize Petabyte Scale Data Partitions"
description: "Pinterest has introduced event time-based partition finalization for its database ingestion framework. The mechanism uses Apache Flink to track event time and Apache Iceberg metadata to publish a non-regressing watermark"
pubDate: 2026-10-19T14:37:00+00:00
addedAt: 2026-10-20T03:18:31.634847+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/pinterest-event-time-partition/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 91
score: 0.80664
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/pinterest-event-time-partition/en/headerimage/generatedHeaderImage-1791063877867.jpg"
---

Pinterest has introduced event time-based partition finalization for its database ingestion framework. The mechanism uses Apache Flink to track event time and Apache Iceberg metadata to publish a non-regressing watermark, helping downstream jobs determine when continuously ingested CDC data is sufficiently complete for processing. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
