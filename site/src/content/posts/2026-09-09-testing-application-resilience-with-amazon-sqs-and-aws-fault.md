---
title: "Testing application resilience with Amazon SQS and AWS Fault Injection Service"
description: "Learn how to use AWS Fault Injection Service and AWS Systems Manager Automation to run progressive chaos experiments against Amazon SQS queues. Validate that your retry logic, circuit breakers, and dead-letter queues act"
pubDate: 2026-09-09T21:33:59+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/testing-application-resilience-with-amazon-sqs-and-aws-fault-injection-service/"
tags: ["aws"]
heat: 84
score: 1.33273
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/08/18/ARCHBLOG-1426-1.png"
imageAlt: "Producer service sends to an SQS queue, a consumer service reads from it, a dead-letter queue attaches to the source queue, and CloudWatch collects metrics"
---

Learn how to use AWS Fault Injection Service and AWS Systems Manager Automation to run progressive chaos experiments against Amazon SQS queues. Validate that your retry logic, circuit breakers, and dead-letter queues actually work under failure before a real outage hits production.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
