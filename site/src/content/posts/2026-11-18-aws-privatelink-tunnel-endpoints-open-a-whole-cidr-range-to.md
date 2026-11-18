---
title: "AWS PrivateLink Tunnel Endpoints Open a Whole CIDR Range to Another Account"
description: "AWS has detailed tunnel endpoints, a PrivateLink endpoint type that gives a consumer VPC access to an entire network segment in another account rather than one resource at a time, over an overlapping address space and wi"
pubDate: 2026-11-18T09:29:00+00:00
addedAt: 2026-11-18T09:48:34.372734+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/aws-privatelink-tunnel-endpoints/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["aws"]
heat: 100
score: 1.40064
readMinutes: 1
image: "https://res.infoq.com/news/2026/11/aws-privatelink-tunnel-endpoints/en/headerimage/generatedHeaderImage-1794476042263.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

AWS has detailed tunnel endpoints, a PrivateLink endpoint type that gives a consumer VPC access to an entire network segment in another account rather than one resource at a time, over an overlapping address space and with consumer-initiated connections only. The consumer must wrap traffic in GENEVE; only TCP and DNS pass, and access logs cannot attribute traffic to a workload behind the endpoint. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
