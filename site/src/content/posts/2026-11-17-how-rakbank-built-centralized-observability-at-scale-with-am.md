---
title: "How Rakbank built centralized observability at scale with Amazon OpenSearch Service"
description: "Rakbank re-platformed logging for its retail digital banking workloads on a cross-account, Multi-AZ Amazon OpenSearch Service design that ingests ~150 GB/day through Fluent Bit, using hot/UltraWarm/cold tiering and Amazo"
pubDate: 2026-11-17T16:03:22+00:00
addedAt: 2026-11-17T21:48:37.767831+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-rakbank-built-centralized-observability-at-scale-with-amazon-opensearch-service/"
tags: ["observability"]
heat: 87
score: 1.38596
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/11/11/ARCHBLOG-1730-1.jpg"
imageAlt: "Cross-account architecture showing Amazon EKS pods sending logs through Fluent Bit over AWS Transit Gateway to a Multi-AZ OpenSearch Service domain with Amazon S3 archival"
hnPoints: 0
hnComments: 0
buzz: 0
---

Rakbank re-platformed logging for its retail digital banking workloads on a cross-account, Multi-AZ Amazon OpenSearch Service design that ingests ~150 GB/day through Fluent Bit, using hot/UltraWarm/cold tiering and Amazon S3 archival for 7-year compliance retention and ~55% cost savings over an all-hot cluster.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
