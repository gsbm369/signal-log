---
title: "ReadyOn’s Four Walls of tenant isolation on Amazon EKS"
description: "ReadyOn runs a multi-tenant platform on Amazon EKS that handles highly sensitive enterprise data. This post describes their Four Walls model: four independent layers of tenant isolation combining Kubernetes namespaces, K"
pubDate: 2026-09-18T21:33:13+00:00
addedAt: 2026-09-19T10:21:15.910193+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/readyons-four-walls-of-tenant-isolation-on-amazon-eks/"
tags: ["kubernetes"]
heat: 79
score: 0.95203
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/09/10/ARCHBLOG-1562-1.png"
imageAlt: "Diagram of a Tenant A pod on the left and Tenant B resources on the right, separated by four numbered walls; six cross-tenant attack paths each stop at the wall that blocks them, and none reach Tenant B"
---

ReadyOn runs a multi-tenant platform on Amazon EKS that handles highly sensitive enterprise data. This post describes their Four Walls model: four independent layers of tenant isolation combining Kubernetes namespaces, Karpenter node pools, Amazon VPC security groups, and per-tenant Amazon Aurora databases for zero-trust defense in depth.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
