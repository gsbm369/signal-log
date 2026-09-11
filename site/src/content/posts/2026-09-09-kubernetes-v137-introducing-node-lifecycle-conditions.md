---
title: "Kubernetes v1.37: Introducing Node Lifecycle Conditions"
description: "Kubernetes has many ways to describe what is happening on a Node. Readiness, taints, Pod state, labels, annotations, and provider-specific APIs each expose part of the picture."
pubDate: 2026-09-09T18:30:00+00:00
addedAt: 2026-09-11T04:05:08.564014+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/09/kubernetes-v1-37-node-lifecycle-conditions/"
tags: ["kubernetes"]
heat: 75
score: 1.07478
readMinutes: 1
---

Kubernetes has many ways to describe what is happening on a Node. Readiness, taints, Pod state, labels, annotations, and provider-specific APIs each expose part of the picture. What has been missing is a shared, Kubernetes-owned way to say that a Node is draining , undergoing maintenance, or undergoing Graceful Node Shutdown . Kubernetes v1.37 introduces five well-known Node conditions that provide that description: DrainInProgress Drained MaintenancePlanned MaintenanceInProgress GracefulNodeShutdownInProgress The new Node lifecycle conditions Condition What it reports DrainInProgress The Node is actively being drained according to the administrator's chosen drain criteria. Drained The Node has reached the drain criteria selected by the administrator. MaintenancePlanned The Node is expected to undergo a change in the future. MaintenanceInProgress The Node is actively undergoing maintenan

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
