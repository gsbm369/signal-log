---
title: "CSIRO Uses Serverless Architecture to Query 100x More Genomic Variants on AWS"
description: "CSIRO has developed Serverless Beacon, a serverless architecture for querying genomic variants without copying VCF files into a central database. The system combines Amazon S3, Lambda, Athena and DynamoDB, using metadata"
pubDate: 2026-10-23T14:30:00+00:00
addedAt: 2026-10-23T15:18:27.621882+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/csiro-serverless-genomic-variant/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["aws"]
heat: 87
score: 1.39784
readMinutes: 1
image: "https://www.infoq.com/styles/static/images/logo/logo_bigger.jpg"
---

CSIRO has developed Serverless Beacon, a serverless architecture for querying genomic variants without copying VCF files into a central database. The system combines Amazon S3, Lambda, Athena and DynamoDB, using metadata indexes and HTTP byte range requests to query compressed genomic regions. Tests reported 1.52 second average latency for 10,000 base pair queries. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
