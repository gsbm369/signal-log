---
title: "Snapshot Isolation vs Serializability"
description: "Snapshot Isolation vs Serializability Getting into some fundamentals. In my re:Invent talk on the internals of Aurora DSQL I mentioned that I think snapshot isolation is a sweet spot in the database isolation spectrum fo"
pubDate: 2024-12-17T00:00:00+00:00
addedAt: 2026-09-11T11:45:59.580026+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2024/12/17/occ-and-isolation.html"
tags: ["tech"]
heat: 27
score: 0.08285
readMinutes: 1
---

Snapshot Isolation vs Serializability Getting into some fundamentals. In my re:Invent talk on the internals of Aurora DSQL I mentioned that I think snapshot isolation is a sweet spot in the database isolation spectrum for most kinds of applications. Today, I want to dive in a little deeper into why I think that, and some of the trade-offs of going stronger and weaker. This post is going to be a little deeper than the last few. If you’re not deeply familiar with SQL’s isolation levels, I recommend checking out Crooks et al’s Seeing is Believing: A Client-Centric Specification of Database Isolation , Berenson et al’s A Critique of ANSI SQL Isolation Levels , or Adya et al’s Generalized Isolation Level Definitions . Specifically, I’m going to talk about one very specific mental model of transaction isolation: read-write conflicts, and write-write conflicts. Let’s start our journey with a tr

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
