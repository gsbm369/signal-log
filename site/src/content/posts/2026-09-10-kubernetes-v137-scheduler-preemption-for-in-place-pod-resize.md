---
title: "Kubernetes v1.37: Scheduler Preemption for In-Place Pod Resize (Alpha)"
description: "In Kubernetes, resource allocation has historically been a static decision made during a Pod's initial scheduling and placement. With the graduation of the core in-Place Pod resize feature to General Availability in v1.3"
pubDate: 2026-09-10T18:30:00+00:00
addedAt: 2026-09-11T04:01:47.864412+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/10/kubernetes-v1-37-scheduler-preemption-for-in-place-pod-resize-alpha/"
tags: ["kubernetes"]
heat: 100
score: 1.35482
readMinutes: 1
---

In Kubernetes, resource allocation has historically been a static decision made during a Pod's initial scheduling and placement. With the graduation of the core in-Place Pod resize feature to General Availability in v1.35, application developers and cluster operators gained the powerful ability to dynamically adjust CPU and memory allocations of running containers without incurring disruptive restarts or application downtime. However, in-place resizing introduced a unique resource scheduling gap: if a running Pod requested a resource scale-up that exceeded the host node's allocatable headroom, the Kubelet was forced to mark the request as Deferred . The Pod would remain parked in this state indefinitely, waiting for resources on the node to naturally free up. To bridge this scheduling gap, Kubernetes v1.37 introduces scheduler preemption for in-place Pod resize (Alpha), behind the InPlac

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
