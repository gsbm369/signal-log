---
title: "SFQ: Simple, Stateless, Stochastic Fairness"
description: "SFQ: Simple, Stateless, Stochastic Fairness Roll the dice. Paul E."
pubDate: 2026-02-25T00:00:00+00:00
addedAt: 2026-09-11T10:17:29.289258+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/02/25/sfq.html"
tags: ["tech"]
heat: 82
score: 0.44246
readMinutes: 1
---

SFQ: Simple, Stateless, Stochastic Fairness Roll the dice. Paul E. McKenney’s 1990 paper Stochastic Fairness Queuing contains one of my favorite little algorithms for distributed systems. Stochastic Fairness Queuing is a way to stochastically isolate workloads from different customers in a way that significantly mitigates the effects of noisy neighbors, with O(1) queues and O(1) time. McKenney starts by describing Fairness Queuing (or queue per client ): This fairness-queuing algorithm operates by maintaining a separate first-come-first-served (FCFS) queue for each conversation. … Since the queues are serviced in a bit-by-bit round-robin fashion ill-behaved conversations that attempt to use more than their fair share of network resources will face longer delays and larger packet-loss rates than well-behaved conversations that remain within their fair share. That’s a network packet focuse

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
