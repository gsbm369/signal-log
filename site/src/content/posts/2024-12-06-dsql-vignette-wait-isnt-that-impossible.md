---
title: "DSQL Vignette: Wait! Isn't That Impossible?"
description: "DSQL Vignette: Wait! Isn’t That Impossible?"
pubDate: 2024-12-06T00:00:00+00:00
addedAt: 2026-09-11T11:45:59.580082+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2024/12/06/inside-dsql-cap.html"
tags: ["tech"]
heat: 26
score: 0.07941
readMinutes: 1
image: "https://brooker.co.za/blog/images/1206_mr_arch.jpg"
---

DSQL Vignette: Wait! Isn’t That Impossible? Laws of physics are real. In today’s post, I’m going to look at how Aurora DSQL is designed for availability, and how we work within the constraints of the laws of physics. If you’d like to learn more about the product first, check out the official documentation , which is always a great place to go for the latest information on Aurora DSQL, and how to fit it into your architecture. In yesterday’s post, I mentioned that Aurora DSQL is designed to remain available, durable, and strongly consistent even in the face of infrastructure failures and network partitions. In this post, we’re going to dive a little deeper into DSQL’s architecture, focussing on multi-region active-active. Aurora DSQL is designed both for single-region applications (looking for a fast, serverless, scalable, relational database), and multi-region active-active applications

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
