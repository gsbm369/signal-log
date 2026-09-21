---
title: "Uber Redesigns M3DB Sharding with Subclusters to Limit Failure Impact"
description: "Uber has redesigned shard placement in M3DB with fixed size subclusters to limit the impact of node failures, maintenance, and cluster scaling. The approach bounds shard dependencies, preserves replica isolation, and use"
pubDate: 2026-09-21T14:37:00+00:00
addedAt: 2026-09-21T15:17:36.731320+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/09/uber-m3db-subcluster-sharding/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 69
score: 0.84764
readMinutes: 1
image: "https://res.infoq.com/news/2026/09/uber-m3db-subcluster-sharding/en/headerimage/generatedHeaderImage-1788717337142.jpg"
---

Uber has redesigned shard placement in M3DB with fixed size subclusters to limit the impact of node failures, maintenance, and cluster scaling. The approach bounds shard dependencies, preserves replica isolation, and uses a greedy algorithm to select shard migrations while avoiding a separate rebalancing pass and unnecessary data movement. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
