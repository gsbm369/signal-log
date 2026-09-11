---
title: "DSQL Vignette: Transactions and Durability"
description: "DSQL Vignette: Transactions and Durability The hard half of a database system? In today’s post, I’m going to look at the other half of what’s under the covers of Aurora DSQL, our new scalable, active-active, SQL database"
pubDate: 2024-12-05T00:00:00+00:00
addedAt: 2026-09-11T11:45:59.580141+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2024/12/05/inside-dsql-writes.html"
tags: ["tech"]
heat: 26
score: 0.07911
readMinutes: 1
image: "https://brooker.co.za/blog/images/1205_read_arch.jpg"
---

DSQL Vignette: Transactions and Durability The hard half of a database system? In today’s post, I’m going to look at the other half of what’s under the covers of Aurora DSQL, our new scalable, active-active, SQL database. If you’d like to learn more about the product first, check out the official documentation , which is always a great place to go for the latest information on Aurora DSQL, and how to fit it into your architecture. Today, we’re going to focus on writes ( INSERTS , UPDATES , etc), and how transaction isolation works in Aurora DSQL. As I wrote about yesterday, reads in Aurora DSQL are done using a multiversion concurrency control (MVCC), allowing them to scale out across many replicas of many storage shards, and across a scalable SQL layer, with no contention or coordination between readers. We’d love to be able to achieve the same properties for writes, but the need to ens

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
