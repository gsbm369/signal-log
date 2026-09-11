---
title: "A Tale of Two Flink Autoscalers"
description: "Samuel Yeboah , Francesco Di Chiara and Mingliang Liu Today, Netflix runs two Flink autoscalers. That is exactly one more than we want."
pubDate: 2026-08-21T16:01:01+00:00
addedAt: 2026-09-11T04:18:17.889230+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/a-tale-of-two-flink-autoscalers-e9f6a1b1492b?source=rss----2615bd06b42e---4"
tags: ["aws"]
heat: 62
score: 0.37488
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*Rn81hdaUHY94Sf8S-GOHZA.png"
---

Samuel Yeboah , Francesco Di Chiara and Mingliang Liu Today, Netflix runs two Flink autoscalers. That is exactly one more than we want. We built the first one in-house years ago, when there was no mature option suited to our platform. The second came from the Apache Flink community, and it can scale workloads our homegrown system was never designed for. We now run both in production and are steadily converging on the open-source one. Along the way we learned some hard lessons about metrics, cost, and the real price of maintaining infrastructure you could instead adopt, and we hope they are useful whether you run a handful of Flink jobs or tens of thousands. Why autoscaling is not optional at our scale Netflix has run stream processing on Apache Flink since 2017. As of 2026 we operate more than 30,000 Flink jobs across multiple AWS regions. Most are not deployed by hand; they are generate

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
