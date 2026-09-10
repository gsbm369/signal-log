---
title: "Validating multi-Region DR for Terraform Enterprise with AWS FIS"
description: "Learn how AWS, HashiCorp, and Athenahealth designed and chaos-tested a multi-Region disaster recovery strategy for Terraform Enterprise on AWS. This post walks through three-phase AWS Fault Injection Service experiments "
pubDate: 2026-09-09T21:05:02+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/validating-multi-region-dr-for-terraform-enterprise-with-aws-fis/"
tags: ["terraform", "aws"]
heat: 98
score: 1.73485
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/09/08/ARCHBLOG-1480-1.png"
imageAlt: "Multi-Region active-passive DR architecture for Terraform Enterprise with bidirectional S3 replication and a Route 53 health check."
---

Learn how AWS, HashiCorp, and Athenahealth designed and chaos-tested a multi-Region disaster recovery strategy for Terraform Enterprise on AWS. This post walks through three-phase AWS Fault Injection Service experiments across Amazon EC2, Aurora, and Amazon S3, the 12-14 minute recovery times achieved, and the state file dependency pitfall to avoid.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
