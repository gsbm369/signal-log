---
title: "AWS Nitro Sandboxes Put Each EKS Pod in Its Own MicroVM with One RuntimeClass Field"
description: "AWS has launched Nitro Sandboxes, running each opted-in EKS pod, ECS task or EC2 workload in its own Firecracker microVM with a separate kernel, enabled by one runtimeClassName field at no extra charge. A confidential mo"
pubDate: 2026-11-16T09:07:00+00:00
addedAt: 2026-11-16T09:48:29.287205+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/aws-nitro-sandboxes-eks/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["aws", "kernel", "gpu"]
heat: 83
score: 1.39852
readMinutes: 1
image: "https://res.infoq.com/news/2026/11/aws-nitro-sandboxes-eks/en/headerimage/generatedHeaderImage-1794301940782.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

AWS has launched Nitro Sandboxes, running each opted-in EKS pod, ECS task or EC2 workload in its own Firecracker microVM with a separate kernel, enabled by one runtimeClassName field at no extra charge. A confidential mode adds attestation-gated key release. The documentation lists the trade-offs: no GPU passthrough, at most five sandboxes per vCPU, and half the compute on SMT instances. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
