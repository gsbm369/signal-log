---
title: "Kubernetes v1.37: Advancing Workload-Aware Scheduling"
description: "AI/ML and complex batch workloads continue to push the boundaries of Kubernetes scheduling. Following the foundational workload-centric enhancements introduced in previous releases, Kubernetes v1.37 delivers the next maj"
pubDate: 2026-09-08T18:30:00+00:00
addedAt: 2026-09-11T04:05:08.564067+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/"
tags: ["kubernetes"]
heat: 65
score: 0.85305
readMinutes: 1
---

AI/ML and complex batch workloads continue to push the boundaries of Kubernetes scheduling. Following the foundational workload-centric enhancements introduced in previous releases, Kubernetes v1.37 delivers the next major milestone in the Workload-Aware Scheduling (WAS) journey. In this release, the core Workload and PodGroup APIs—enabling gang scheduling—along with Workload-Aware Preemption (WAP) and shared DRA ResourceClaims for PodGroups, all graduate to Beta, solidifying their role in the Kubernetes ecosystem. To address the hierarchical scheduling requirements of modern high-performance distributed workloads, v1.37 introduces the new CompositePodGroup API. This new API allows expressing multi-level topology constraints, gang scheduling, and preemption policies for complex, heterogeneous groups of Pods. Crucially, this architectural expansion unlocks native scheduling support for ad

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
