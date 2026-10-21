---
title: "Netflix Bridges AWS IAM and Internal Identity with Workload Attestation"
description: "Netflix has developed a workload attestation mechanism for Apache Spark jobs running on Amazon EMR. The design combines AWS IAM identity with signed claims from Netflix’s control plane before issuing short-lived internal"
pubDate: 2026-10-21T13:45:00+00:00
addedAt: 2026-10-21T15:18:36.724947+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/netflix-workload-attestation-aws/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["aws"]
heat: 70
score: 1.39352
readMinutes: 1
image: "https://www.infoq.com/styles/static/images/logo/logo_bigger.jpg"
---

Netflix has developed a workload attestation mechanism for Apache Spark jobs running on Amazon EMR. The design combines AWS IAM identity with signed claims from Netflix’s control plane before issuing short-lived internal X.509 certificates, allowing managed compute workloads to authenticate to internal services without directly injecting credentials. By Leela Kumili

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
