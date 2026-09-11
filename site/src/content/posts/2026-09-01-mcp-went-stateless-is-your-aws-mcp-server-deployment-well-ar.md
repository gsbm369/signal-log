---
title: "MCP went stateless: Is your AWS MCP server deployment well-architected?"
description: "On July 28, 2026, MCP made its protocol core stateless, removing the initialize handshake and session header. This post maps the MCP 2026-07-28 specification to the AWS Well-Architected Agentic AI Lens, pillar by pillar,"
pubDate: 2026-09-01T13:09:19+00:00
addedAt: 2026-09-11T04:05:08.563117+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/mcp-went-stateless-is-your-aws-mcp-server-deployment-well-architected/"
tags: ["aws"]
heat: 66
score: 0.87098
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/08/27/ARCHBLOG-1666-1.png"
imageAlt: "Diagram mapping MCP 2026-07-28 protocol changes to the six Well-Architected Agentic AI Lens pillars"
---

On July 28, 2026, MCP made its protocol core stateless, removing the initialize handshake and session header. This post maps the MCP 2026-07-28 specification to the AWS Well-Architected Agentic AI Lens, pillar by pillar, and shows why the stateless design lets you delete the sticky sessions and session stores your MCP servers needed on AWS.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
