---
title: "Resilience testing your agents on Amazon Bedrock AgentCore"
description: "When an AI agent's tools fail or return corrupted data, does it fail safe or confidently fabricate an answer? Learn how to inject tool-level faults (cancelled calls, corrupted responses, stripped fields) into a Strands a"
pubDate: 2026-11-18T20:06:14+00:00
addedAt: 2026-11-19T22:43:39.042430+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/resilience-testing-your-agents-on-amazon-bedrock-agentcore/"
tags: ["observability", "aws"]
heat: 64
score: 0.92527
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/11/13/ARCHBLOG-1610-1.png"
imageAlt: "Architecture diagram: AWS FIS triggers an SSM Automation action that writes chaos parameters under /chaos/{runtime_id}/ in Parameter Store, which the agent’s runtime controller reads on each invocation to inject the configured faults"
hnPoints: 0
hnComments: 0
buzz: 0
---

When an AI agent's tools fail or return corrupted data, does it fail safe or confidently fabricate an answer? Learn how to inject tool-level faults (cancelled calls, corrupted responses, stripped fields) into a Strands agent on Amazon Bedrock AgentCore using AWS Fault Injection Service, and build the observability to tell a safe failure from a silent one.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
