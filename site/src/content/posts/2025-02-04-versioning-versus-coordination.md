---
title: "Versioning versus Coordination"
description: "Versioning versus Coordination Spoiler: Versioning Wins. Today, we’re going to build a little database system."
pubDate: 2025-02-04T00:00:00+00:00
addedAt: 2026-09-11T11:27:53.290111+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/02/04/versioning.html"
tags: ["tech"]
heat: 34
score: 0.10006
readMinutes: 1
image: "https://brooker.co.za/blog/images/db_architecture.png"
---

Versioning versus Coordination Spoiler: Versioning Wins. Today, we’re going to build a little database system. For availability, latency, and scalability, we’re going to divide our data into multiple shards, have multiple replicas of each shard, and allow multiple concurrent queries. As a block diagram, it’s going to look something like this: Next, borrowing heavily from Hermitage , we’re going to run some SQL. begin; -- T0 create table test (id int primary key, value int); -- T0 insert into test (id, value) values (1, 10), (2, 20), (3, 30); -- T0 commit; -- T0 So far so good. We’ve inserted three rows into our database. Next, we’re going to run two concurrent transactions (from two different connections, call them T1 and T2 ), like so: begin; -- T2 begin; -- T1 select * from test where id = 1; -- T1. A: We want this to show 1 = 10. update test set value = value + 2; -- T2 select * from

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
