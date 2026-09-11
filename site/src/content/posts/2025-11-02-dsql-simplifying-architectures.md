---
title: "DSQL: Simplifying Architectures"
description: "DSQL: Simplifying Architectures Complexity is a choice. While we were designing and building Aurora DSQL , we spent a lot of time thinking about our experience building and running database-backed systems."
pubDate: 2025-11-02T00:00:00+00:00
addedAt: 2026-09-11T11:03:46.193052+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/11/02/thinking-dsql.html"
tags: ["tech"]
heat: 48
score: 0.28412
readMinutes: 1
image: "https://brooker.co.za/blog/images/dsql_single_arch.png"
---

DSQL: Simplifying Architectures Complexity is a choice. While we were designing and building Aurora DSQL , we spent a lot of time thinking about our experience building and running database-backed systems. We saw that building great, fast, cost-effective, highly-available, systems was harder than it needed to be. We wanted to make it easier. Today, I want to discuss some of Aurora DSQL’s features, and how I think they come together to make your life, as an application, service, or website developer, easier. We wanted for our customers what we wanted for ourselves: a relational database that allows us to build great systems with simple architectures. Serverless : The most obvious one is serverlessness. With DSQL you don’t need to pick hardware, manage clusters, design for failover, think about patching engines or systems, monitor CPU and memory, or any of the many other tasks that come wi

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
