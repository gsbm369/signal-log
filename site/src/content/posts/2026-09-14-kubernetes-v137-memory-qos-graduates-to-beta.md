---
title: "Kubernetes v1.37: Memory QoS Graduates to Beta"
description: "Memory QoS has graduated to Beta in Kubernetes v1.37 and is now enabled by default. On Linux nodes running cgroup v2, the feature uses the memory controller to give the kernel better guidance on how to treat container me"
pubDate: 2026-09-14T18:30:00+00:00
addedAt: 2026-09-15T16:29:51.926438+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/14/kubernetes-v1-37-memory-qos-graduates-to-beta/"
tags: ["kubernetes", "linux", "kernel"]
heat: 87
score: 1.20161
readMinutes: 1
---

Memory QoS has graduated to Beta in Kubernetes v1.37 and is now enabled by default. On Linux nodes running cgroup v2, the feature uses the memory controller to give the kernel better guidance on how to treat container memory. It was first introduced as Alpha in v1.22, and expanded in v1.36 with tiered memory reservation. This post covers what changed in v1.37, what the Beta promotion means for cluster operators, and how to configure the feature. What changed in v1.37 Memory QoS is Beta and enabled by default The MemoryQoS feature gate is now Beta in v1.37. This means every v1.37 kubelet has the feature gate turned on without any configuration change. Turning on the feature by default is safe because the default kubelet configuration does not enable memory throttling or memory reservation. No memory.high , memory.min , or memory.low values are written to cgroups unless you explicitly conf

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
