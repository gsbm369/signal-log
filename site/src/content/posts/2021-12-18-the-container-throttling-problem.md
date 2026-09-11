---
title: "The container throttling problem"
description: "This is an excerpt from an internal document David Mackey and I co-authored in April 2019. The document is excerpted since much of the original doc was about comparing possible approaches to increasing efficency at Twitt"
pubDate: 2021-12-18T00:00:00+00:00
addedAt: 2026-09-11T11:45:59.579510+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/cgroup-throttling/"
tags: ["tech"]
heat: 5
score: 0.00122
readMinutes: 1
image: "https://danluu.com/images/cgroup-throttling/cpu-histogram-1.webp"
imageAlt: "Histogram for service with 20 CPU quota showing that average utilization is much lower but peak utilization is significantly higher when the service is overloaded and violates its SLO"
---

This is an excerpt from an internal document David Mackey and I co-authored in April 2019. The document is excerpted since much of the original doc was about comparing possible approaches to increasing efficency at Twitter, which is mostly information that's meaningless outside of Twitter without a large amount of additional explanation/context. At Twitter, most CPU bound services start falling over at around 50% reserved container CPU utilization and almost all services start falling over at not much more CPU utilization even though CPU bound services should, theoretically, be able to get higher CPU utilizations. Because load isn't, in general, evenly balanced across shards and the shard-level degradation in performance is so severe when we exceed 50% CPU utilization, this makes the practical limit much lower than 50% even during peak load events. This document will describe potential s

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
