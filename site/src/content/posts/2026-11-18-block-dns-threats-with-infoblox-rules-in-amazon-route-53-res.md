---
title: "Block DNS threats with Infoblox rules in Amazon Route 53 Resolver DNS Firewall"
description: "Infoblox Threat Defense is now available in preview in Amazon Route 53 Resolver DNS Firewall, providing partner-managed DNS threat intelligence. Learn how to add an Infoblox managed rule to a rule group, test it in alert"
pubDate: 2026-11-18T18:35:14+00:00
addedAt: 2026-11-20T15:48:35.103483+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/block-dns-threats-with-infoblox-rules-in-amazon-route-53-resolver-dns-firewall/"
tags: ["tech"]
heat: 64
score: 0.7743
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/11/13/ARCHBLOG-1774-1.png"
imageAlt: "Architecture diagram. Inside an Amazon VPC, Amazon EC2 workloads send DNS queries to Amazon Route 53 Resolver. Route 53 Resolver sends each query for inspection to Route 53 DNS Firewall. DNS Firewall evaluates the query against a DNS Firewall rule group that contains the Infoblox managed rule, which is set to ALERT and later BLOCK. DNS Firewall matches are recorded in query logs that are delivered to Amazon CloudWatch Logs, which sits outside the VPC. Also outside the VPC, Infoblox sends threat intelligence to the Infoblox managed rule, and AWS Marketplace supplies the managed rules to the rule group."
hnPoints: 0
hnComments: 0
buzz: 0
---

Infoblox Threat Defense is now available in preview in Amazon Route 53 Resolver DNS Firewall, providing partner-managed DNS threat intelligence. Learn how to add an Infoblox managed rule to a rule group, test it in alert mode, monitor matches, and move to blocking.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
