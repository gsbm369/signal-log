---
title: "How DeepL keeps closest-exit routing during maintenance with AWS Cloud WAN"
description: "DeepL runs a multi-Region hybrid network across multiple AWS Regions and AWS Direct Connect locations. See how DeepL drains a single Direct Connect link for planned maintenance without packet loss or cross-Region rerouti"
pubDate: 2026-11-09T20:15:09+00:00
addedAt: 2026-11-09T21:48:37.766748+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-deepl-keeps-closest-exit-routing-during-maintenance-with-aws-cloud-wan/"
tags: ["aws"]
heat: 72
score: 1.39801
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/10/29/ARCHBLOG-1591-1.png"
imageAlt: "DeepL’s hybrid architecture: AWS Regions connected through an AWS Cloud WAN core network, a Direct Connect gateway, three Direct Connect locations, and two on-premises data centers advertising the same /16"
hnPoints: 0
hnComments: 0
buzz: 0
---

DeepL runs a multi-Region hybrid network across multiple AWS Regions and AWS Direct Connect locations. See how DeepL drains a single Direct Connect link for planned maintenance without packet loss or cross-Region rerouting, using AWS Cloud WAN and an on-premises AS_PATH prepend so every other Region keeps its closest-exit routing.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
