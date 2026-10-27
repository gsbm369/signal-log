---
title: "Announcing the Workload Conformance Working Group"
description: "We are excited to announce that the Kubernetes community now has a Workload Conformance Working Group . The working group is writing a shared standard for how workloads behave at runtime on Kubernetes."
pubDate: 2026-10-27T04:30:00+00:00
addedAt: 2026-10-27T16:18:30.636796+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/10/27/announcing-workload-conformance-wg/"
tags: ["kubernetes"]
heat: 73
score: 0.92379
readMinutes: 1
---

We are excited to announce that the Kubernetes community now has a Workload Conformance Working Group . The working group is writing a shared standard for how workloads behave at runtime on Kubernetes. To get it right, we need input from the people who build those workloads and from the people who run the clusters they're deployed on. Why workloads need a shared standard Certified Kubernetes tests the cluster, and Kubernetes AI Conformance tests whether a cluster can run AI and ML workloads. Nothing comparable exists for the workloads themselves, so cluster operators still check each application by hand before routine maintenance or a Kubernetes upgrade. The problems they find are familiar. A routine node drain is often how you discover that an application can't tolerate disruption. An upgrade can break an application that still depends on a removed API version . Others show up in day-to

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
