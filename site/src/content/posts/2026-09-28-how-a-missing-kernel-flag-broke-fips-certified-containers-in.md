---
title: "How a missing kernel flag broke FIPS-certified containers in managed Kubernetes"
description: "A customer building a FedRAMP-compliant deployment found that Ubuntu Pro 22.04 FIPS container images were silently failing on standard, mainline Linux kernels, the kind used by managed Kubernetes environments such as AWS"
pubDate: 2026-09-28T09:59:02+00:00
addedAt: 2026-09-28T18:20:57.734034+00:00
source: "Ubuntu"
category: devops_linux
sourceUrl: "https://ubuntu.com//blog/fixing-fips-kernel-flag"
tags: ["kubernetes", "kernel", "linux", "aws"]
heat: 80
score: 1.38859
readMinutes: 1
image: "https://ubuntu.com/wp-content/uploads/894c/support-cover.png"
---

A customer building a FedRAMP-compliant deployment found that Ubuntu Pro 22.04 FIPS container images were silently failing on standard, mainline Linux kernels, the kind used by managed Kubernetes environments such as AWS EKS and Fargate. The fix required a patch that preserved FIPS compliance without triggering months of recertification. This post explains what happened, why [ ]

*Reproduced from the Ubuntu feed. No model was used to write this entry — follow the link for the full article.*
