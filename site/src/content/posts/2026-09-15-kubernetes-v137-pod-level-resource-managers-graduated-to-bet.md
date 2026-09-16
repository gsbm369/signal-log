---
title: "Kubernetes v1.37: Pod-Level Resource Managers graduated to Beta"
description: "With the release of Kubernetes v1.37, the Pod-Level Resource Managers feature has graduated to Beta status (disabled by default)! First introduced as an Alpha feature in Kubernetes v1.36 , this enhancement builds on Pod-"
pubDate: 2026-09-15T18:30:00+00:00
addedAt: 2026-09-16T16:17:48.937116+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/15/kubernetes-v1-37-pod-level-resource-managers-beta/"
tags: ["kubernetes"]
heat: 80
score: 1.20393
readMinutes: 1
---

With the release of Kubernetes v1.37, the Pod-Level Resource Managers feature has graduated to Beta status (disabled by default)! First introduced as an Alpha feature in Kubernetes v1.36 , this enhancement builds on Pod-Level Resources by equipping Kubelet's Topology Manager, CPU Manager, and Memory Manager to use Pod-level resource declarations ( .spec.resources ) directly when making hardware placement decisions. Bringing pod-level resources to node managers Before this feature, obtaining exclusive NUMA-aligned CPU cores or memory for latency-critical applications forced cluster operators into an all-or-nothing choice: assign integer resource requests to every container in the Pod, or forfeit exclusive NUMA alignment entirely. For modern workloads running lightweight sidecars (such as logging agents or telemetry exporters), allocating dedicated physical cores to auxiliary containers wa

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
