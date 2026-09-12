---
title: "Kubernetes access via an identity provider: Public client, not confidential"
description: "Access control belongs on the same day-zero checklist as networking and storage. On most on-prem clusters, it never makes the list."
pubDate: 2026-09-08T11:30:00+00:00
addedAt: 2026-09-12T01:19:02.731308+00:00
source: "CNCF"
category: devops_linux
sourceUrl: "https://www.cncf.io/blog/2026/09/08/kubernetes-access-via-an-identity-provider-public-client-not-confidential/"
tags: ["kubernetes", "networking"]
heat: 90
score: 0.61391
readMinutes: 1
image: "https://www.cncf.io/wp-content/uploads/2026/09/image-1.png"
imageAlt: "Figure 1: kubectl authenticates against the identity provider, then presents the resulting token to kube-apiserver, which validates it and hands it off to RBAC."
---

Access control belongs on the same day-zero checklist as networking and storage. On most on-prem clusters, it never makes the list. The Identity Gap Managed cloud Kubernetes ships IAM or SSO integration out of the box....

*Reproduced from the CNCF feed. No model was used to write this entry — follow the link for the full article.*
