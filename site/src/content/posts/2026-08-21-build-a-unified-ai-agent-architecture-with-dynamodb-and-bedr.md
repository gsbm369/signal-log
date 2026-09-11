---
title: "Build a unified AI agent architecture with DynamoDB and Bedrock"
description: "With native vector search in Amazon DynamoDB, you can store vector embeddings alongside your operational data in a single table. This post shows how to build a unified AI agent architecture where an Amazon Bedrock agent "
pubDate: 2026-08-21T18:19:23+00:00
addedAt: 2026-09-11T06:56:54.630002+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/build-a-unified-ai-agent-architecture-with-dynamodb-and-bedrock/"
tags: ["embedding"]
heat: 55
score: 0.3538
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/08/21/ARCHBLOG-1687-1.jpg"
imageAlt: "Architecture diagram showing a user query flowing to an Amazon Bedrock agent, which invokes action group Lambda functions that call the DynamoDB SearchVectors API and standard CRUD APIs, with DynamoDB Streams triggering an embedding pipeline Lambda that generates vectors with Amazon Titan Text Embeddings V2"
---

With native vector search in Amazon DynamoDB, you can store vector embeddings alongside your operational data in a single table. This post shows how to build a unified AI agent architecture where an Amazon Bedrock agent uses one DynamoDB table for both structured lookups and semantic search, with a DynamoDB Streams pipeline that keeps embeddings in sync.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
