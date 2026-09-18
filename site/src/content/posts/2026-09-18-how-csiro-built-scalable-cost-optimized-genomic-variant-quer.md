---
title: "How CSIRO built scalable, cost-optimized genomic variant querying on AWS"
description: "Learn how researchers at CSIRO, Australia's national science agency, built Serverless Beacon (sBeacon), a scalable serverless solution for securely querying genomic variant data on AWS. sBeacon implements the GA4GH Beaco"
pubDate: 2026-09-18T14:35:42+00:00
addedAt: 2026-09-18T19:09:05.114703+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-csiro-built-scalable-cost-optimized-genomic-variant-querying-on-aws/"
tags: ["aws"]
heat: 93
score: 1.38939
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/09/09/Figure-1-Data-Onboarding.png"
imageAlt: "Data onboarding architecture for sBeacon, showing genomic data location submitted to an API Gateway endpoint, AWS Lambda functions handling indexing, metadata written to Amazon S3 in ORC format, CSIRO Ontoserver building the ontology index, and Amazon Athena building the metadata tables."
---

Learn how researchers at CSIRO, Australia's national science agency, built Serverless Beacon (sBeacon), a scalable serverless solution for securely querying genomic variant data on AWS. sBeacon implements the GA4GH Beacon standard using Amazon S3, AWS Lambda, Amazon DynamoDB, and Amazon Athena to support production-scale clinical and research applications.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
