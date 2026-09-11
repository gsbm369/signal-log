---
title: "Lorenz and Little: How Much Does Your Tail Cost?"
description: "Lorenz and Little: How Much Does Your Tail Cost? Lorenz and Little sounds like hipster burger bar from 2015."
pubDate: 2026-07-29T00:00:00+00:00
addedAt: 2026-09-11T04:15:18.672789+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/07/29/lorenz-and-little.html"
tags: ["tech"]
heat: 92
score: 0.80139
readMinutes: 1
---

Lorenz and Little: How Much Does Your Tail Cost? Lorenz and Little sounds like hipster burger bar from 2015. It’s time for Marc’s Amateur Statistics Corner! Today: why I pay a lot of attention to tail latency when optimizing cost. I’ve written before on the importance of tail latency for customer experience (e.g. in 2026 , 2021 , and 2021 , and 2017 ). Today, I want to talk about tail latency from the perspective of cost and capacity. Like many system operators, I think about tail latency using percentiles. Here’s a question: how much does each of my latency percentiles contributed to the mean latency? Intuitively, the answer is “quite a lot”, but can we quantify that? We can! The thing we’re looking for is the empirical Lorenz Curve . It directly calculates the answer to the question: given a latency percentile $P$ (e.g. p99=100ms), how much do requests taking shorter than $P$ contribut

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
