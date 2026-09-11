---
title: "Kubernetes v1.37: Scale Workloads to Zero with HorizontalPodAutoscaler"
description: "Kubernetes v1.37 includes API support for horizontal autoscaling of workloads down to zero replicas. This feature is now Beta and enabled by default."
pubDate: 2026-09-02T18:30:00+00:00
addedAt: 2026-09-11T04:15:18.672105+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/02/kubernetes-v1-37-hpa-scale-to-zero-beta/"
tags: ["kubernetes"]
heat: 42
score: 0.21291
readMinutes: 1
---

Kubernetes v1.37 includes API support for horizontal autoscaling of workloads down to zero replicas. This feature is now Beta and enabled by default. A HorizontalPodAutoscaler (HPA) that uses a suitable object metric or external metric can now scale a workload to zero replicas, then bring it back when the metric changes. Before v1.37, you needed an add-on or external component, or you had to enable the Alpha feature gate, to scale from zero. It is now part of core Kubernetes. Scaling to zero removes the last idle Pod from workloads such as queue consumers and batch processors. The savings are largest when each Pod reserves expensive resources, including dedicated CPUs or GPUs. The trade-off is cold-start time: the HPA must observe the metric, schedule a Pod, and start the application. This works well when work can wait in a durable queue. Kubernetes Services do not buffer requests while

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
