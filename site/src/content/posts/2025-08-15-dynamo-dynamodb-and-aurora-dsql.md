---
title: "Dynamo, DynamoDB, and Aurora DSQL"
description: "Dynamo, DynamoDB, and Aurora DSQL Names are hard, ok? People often ask me about the architectural relationship between Amazon Dynamo (as described in the classic 2007 SOSP paper), Amazon DynamoDB (the serverless distribu"
pubDate: 2025-08-15T00:00:00+00:00
addedAt: 2026-09-11T11:06:03.517826+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/08/15/dynamo-dynamodb-dsql.html"
tags: ["aws"]
heat: 95
score: 0.24103
readMinutes: 1
---

Dynamo, DynamoDB, and Aurora DSQL Names are hard, ok? People often ask me about the architectural relationship between Amazon Dynamo (as described in the classic 2007 SOSP paper), Amazon DynamoDB (the serverless distributed NoSQL database from AWS), and Aurora DSQL (the serverless distributed SQL database from AWS). There’s a ton to say on the topic, but I’ll start off on comparing how the systems achieve a few key properties. The key references for this post are: For Dynamo, Dynamo: Amazon’s Highly Available Key-value Store from SOSP’07. For DynamoDB, Amazon DynamoDB: A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service from ATC’22, Distributed Transactions at Scale in Amazon DynamoDB from ATC’23, and Lessons learned from 10 years of DynamoDB from the Amazon Science blog. For DSQL, my blog series on DSQL . Durability The databases we’re looking at offer different

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
