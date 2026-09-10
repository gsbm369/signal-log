---
title: "Building resilient real-time streaming workers with Amazon DynamoDB leases"
description: "Real-time streaming workers that hold hundreds of persistent WebSocket connections lose data when a worker fails. Learn how to build a WebSocket fleet management system on Amazon ECS and AWS Fargate that uses Amazon Dyna"
pubDate: 2026-09-10T16:14:22+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/building-resilient-real-time-streaming-workers-with-amazon-dynamodb-leases/"
tags: ["aws"]
heat: 69
score: 0.96535
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/09/08/ARCHBLOG-1505-1.png"
imageAlt: "Architecture of the WebSocket fleet: API Gateway and Lambda write events to DynamoDB and SQS, and ECS Fargate workers claim leases and publish metrics to CloudWatch"
---

Real-time streaming workers that hold hundreds of persistent WebSocket connections lose data when a worker fails. Learn how to build a WebSocket fleet management system on Amazon ECS and AWS Fargate that uses Amazon DynamoDB conditional writes as a distributed lease to track ownership, fail over automatically, and deploy with low downtime.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
