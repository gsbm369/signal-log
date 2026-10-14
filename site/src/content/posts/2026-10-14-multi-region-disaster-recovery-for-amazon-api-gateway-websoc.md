---
title: "Multi-region disaster recovery for Amazon API Gateway WebSocket APIs"
description: "Learn how to build multi-region disaster recovery for Amazon API Gateway WebSocket APIs. This design pattern combines Amazon Route 53 DNS failover, Amazon DynamoDB Global Tables, a canary health probe, and client-side re"
pubDate: 2026-10-14T14:31:55+00:00
addedAt: 2026-10-14T15:18:06.808513+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/multi-region-disaster-recovery-for-amazon-api-gateway-websocket-apis/"
tags: ["tech"]
heat: 70
score: 0.84866
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/10/12/ARCHBLOG-1349-1-2.png"
imageAlt: "Architecture diagram showing a client connecting through a Route 53 failover policy to the primary Region us-east-1, which runs API Gateway WebSocket, Lambda, and DynamoDB, with an Amazon EventBridge rule triggering a canary health check and a CloudWatch alarm that drives the Route 53 health check; DynamoDB Global Tables replicate to the secondary Region us-west-2 for failover"
---

Learn how to build multi-region disaster recovery for Amazon API Gateway WebSocket APIs. This design pattern combines Amazon Route 53 DNS failover, Amazon DynamoDB Global Tables, a canary health probe, and client-side reconnection logic to reconnect clients and restore session state automatically during a regional failover.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
