---
title: "DSQL Vignette: Reads and Compute"
description: "DSQL Vignette: Reads and Compute The easy half of a database system? In today’s post, I’m going to look at half of what’s under the covers of Aurora DSQL, our new scalable, active-active, SQL database."
pubDate: 2024-12-04T00:00:00+00:00
addedAt: 2026-09-11T11:52:51.185920+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2024/12/04/inside-dsql.html"
tags: ["tech"]
heat: 30
score: 0.0788
readMinutes: 1
image: "https://brooker.co.za/blog/images/1204_aurora.png"
---

DSQL Vignette: Reads and Compute The easy half of a database system? In today’s post, I’m going to look at half of what’s under the covers of Aurora DSQL, our new scalable, active-active, SQL database. If you’d like to learn more about the product first, check out the official documentation , which is always a great place to go for the latest information on Aurora DSQL, and how to fit it into your architecture. Today, we’re going to focus on running SQL and doing transactional reads. But first, let’s talk scalability. One of the most interesting things in DSQL’s architecture is that we can scale compute (SQL execution), read throughput, write throughput, and storage space independently. At a fundamental level, scaling compute in a database system requires disaggregation of storage and compute. If you stick storage and compute together, you end up needing to scale one to scale the other,

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
