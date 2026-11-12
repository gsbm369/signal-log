---
title: "How Zillow runs 100 million daily notifications on AWS Step Functions"
description: "Zillow sends more than 100 million personalized notifications a day, each as a short-lived AWS Step Functions Express workflow. See how the Comms Experience team replaced more than 10 campaign generators with one configu"
pubDate: 2026-11-11T23:25:00+00:00
addedAt: 2026-11-12T03:48:39.731650+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-zillow-runs-100-million-daily-notifications-on-aws-step-functions/"
tags: ["aws"]
heat: 79
score: 1.38985
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/11/11/ARCHBLOG-1607-1.png"
imageAlt: "Original architecture: each campaign generator carries its own copy of the workflow, data models, and business rules"
hnPoints: 0
hnComments: 0
buzz: 0
---

Zillow sends more than 100 million personalized notifications a day, each as a short-lived AWS Step Functions Express workflow. See how the Comms Experience team replaced more than 10 campaign generators with one configuration-driven orchestration platform and a library of reusable content modules.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
