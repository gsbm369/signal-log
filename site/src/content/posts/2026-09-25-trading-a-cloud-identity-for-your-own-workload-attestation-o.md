---
title: "Trading a Cloud Identity for Your Own: Workload Attestation on Managed Compute"
description: "By Dhruv Pratap Introduction Organizations that have been around for a while usually run two identity systems side by side. One belongs to the cloud provider: IAM roles, instance profiles, execution roles."
pubDate: 2026-09-25T16:01:03+00:00
addedAt: 2026-09-25T21:51:03.058762+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/trading-a-cloud-identity-for-your-own-workload-attestation-on-managed-compute-516d5a29b252?source=rss----2615bd06b42e---4"
tags: ["aws"]
heat: 92
score: 1.02262
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*eIWpHw7J_6qZCuaffD0lQQ.png"
---

By Dhruv Pratap Introduction Organizations that have been around for a while usually run two identity systems side by side. One belongs to the cloud provider: IAM roles, instance profiles, execution roles. The other is your own, and it is the one your internal services actually check when they decide whether to answer a request. On infrastructure you build yourself, you can bootstrap your own identity however you like. On managed compute you cannot. The provider hands your process a cloud identity and nothing else. This post describes how we close that gap for Apache Spark workloads running on Amazon EMR. A workload that starts with only an AWS identity has to end up holding a first-class internal identity. Doing the exchange is straightforward. Making it trustworthy is the part that took the design work. Very little of what follows is specific to Spark or to EMR. Two identity systems In

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
