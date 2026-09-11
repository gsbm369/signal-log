---
title: "How a global payment processor preserved AWS RAM shares and Lake Formation permissions during an AWS Organizations migra"
description: "When AWS accounts move between organizations, organization-bound AWS RAM resource shares break and control-plane access is lost. Learn how a global payment processor used temporary bridge shares to preserve AWS Lake Form"
pubDate: 2026-08-24T15:23:21+00:00
addedAt: 2026-09-11T04:15:18.671217+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-a-global-payment-processor-preserved-aws-ram-shares-and-lake-formation-permissions-during-an-aws-organizations-migration/"
tags: ["aws"]
heat: 77
score: 0.58863
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/08/17/ARCHBLOG-1650-1.png"
imageAlt: "Migration wave structure. Stage one covers fourteen non-production waves across eight months, none of which crossed an organization boundary. Stage two covers sixteen production waves: one pilot wave, twelve scheduled waves on a weekly cadence, and three contingency waves. The transitional service agreement expires inside the contingency window, leaving only the first contingency week usable."
---

When AWS accounts move between organizations, organization-bound AWS RAM resource shares break and control-plane access is lost. Learn how a global payment processor used temporary bridge shares to preserve AWS Lake Formation permissions across a 382-account AWS Organizations migration, then restored the original shares as the durable source of truth.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
