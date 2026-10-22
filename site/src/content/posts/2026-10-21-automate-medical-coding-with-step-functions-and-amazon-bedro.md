---
title: "Automate medical coding with Step Functions and Amazon Bedrock AgentCore"
description: "Learn how to combine deterministic orchestration with bounded agentic reasoning using AWS Step Functions and the Amazon Bedrock AgentCore harness. This medical coding workflow escalates cheapest-first: a safety block-lis"
pubDate: 2026-10-21T21:26:23+00:00
addedAt: 2026-10-22T03:18:33.053356+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/automate-medical-coding-with-step-functions-and-amazon-bedrock-agentcore/"
tags: ["aws"]
heat: 75
score: 0.96574
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/10/19/ARCHBLOG-1619-1.png"
imageAlt: "A vertical workflow with seven numbered steps. A study term starts a Step Functions execution (1). A CheckDirect Lambda function runs a direct lookup against Aurora PostgreSQL with pgvector (2). On a miss, the workflow invokes the AgentCore harness agent (3), which calls two MCP tools through the AgentCore Gateway (4): get_study_info and search_dictionary. The tools query Aurora. The workflow routes on the agent’s score (5), and a WriteBack Lambda function writes the outcome to Aurora (6). Amazon CloudWatch records agent traces (7)."
---

Learn how to combine deterministic orchestration with bounded agentic reasoning using AWS Step Functions and the Amazon Bedrock AgentCore harness. This medical coding workflow escalates cheapest-first: a safety block-list, then exact matching, then an AI agent only for terms that need judgment, keeping every routing decision auditable.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
