---
title: "What Fekete's Anomaly Can Teach Us About Isolation"
description: "What Fekete’s Anomaly Can Teach Us About Isolation Is it just fancy write skew? In the first draft of yesterday’s post , the example I used was one that showed Fekete’s anomaly."
pubDate: 2025-02-05T00:00:00+00:00
addedAt: 2026-09-11T11:27:53.290013+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/02/05/feketes.html"
tags: ["tech"]
heat: 34
score: 0.10044
readMinutes: 1
image: "https://brooker.co.za/blog/images/feketes_anomaly.svg"
---

What Fekete’s Anomaly Can Teach Us About Isolation Is it just fancy write skew? In the first draft of yesterday’s post , the example I used was one that showed Fekete’s anomaly. After drafting, I realized the example distracted too much from the story. But there’s still something I want to say about the anomaly, and so now we’re here. What is Fekete’s anomaly? It’s an example of a snapshot isolation behavior first described in Fekete, O’Neil, and O’Neil’s paper A Read-Only Transaction Anomaly Under Snapshot Isolation . The first time I read about it, I found it spooky. As in five stages of grief spooky. But the more I’ve thought about it, the more I think it’s just a great teaching example. To understand the anomaly, let’s talk about two people. We’ll call the Pat and Betty . Pat and Betty share a pair of bank accounts - a savings account and a current account. They bank at Alan’s bank,

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
