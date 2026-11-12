---
title: "Gang scheduling and topology-aware placement for AI training in Kubernetes"
description: "Distributed AI training workloads impose complex scheduling requirements that Kubernetes s built-in scheduler can t meet. Kubernetes schedules pods individually and independently, but distributed training introduces two "
pubDate: 2026-11-12T12:00:00+00:00
addedAt: 2026-11-12T15:48:06.364900+00:00
source: "CNCF"
category: devops_linux
sourceUrl: "https://www.cncf.io/blog/2026/11/12/gang-scheduling-and-topology-aware-placement-for-ai-training-in-kubernetes/"
tags: ["kubernetes"]
heat: 89
score: 1.35214
readMinutes: 1
image: "https://www.cncf.io/wp-content/uploads/2026/11/image-4.png"
imageAlt: "How a distributed training job moves from submission to pod binding"
hnPoints: 0
hnComments: 0
buzz: 0
---

Distributed AI training workloads impose complex scheduling requirements that Kubernetes s built-in scheduler can t meet. Kubernetes schedules pods individually and independently, but distributed training introduces two requirements that break this model: Pods must land on hardware with...

*Reproduced from the CNCF feed. No model was used to write this entry — follow the link for the full article.*
