---
title: "The Shift to cgroup v2 in Kubernetes: What You Need to Know"
description: "In Linux, cgroups (control groups) are a kernel feature used for managing system resources. Kubernetes uses cgroups to allocate resources like CPU and memory to containers, ensuring that applications run smoothly without"
pubDate: 2026-10-06T18:00:00+00:00
addedAt: 2026-10-07T16:43:25.780312+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/10/06/kubernetes-cgroups-v2-shift/"
tags: ["kubernetes", "linux", "kernel"]
heat: 85
score: 1.19325
readMinutes: 1
---

In Linux, cgroups (control groups) are a kernel feature used for managing system resources. Kubernetes uses cgroups to allocate resources like CPU and memory to containers, ensuring that applications run smoothly without interfering with each other. With the release of Kubernetes v1.31, support for v1 cgroup management moved into maintenance mode . Support for v2 cgroup management has been stable since Kubernetes v1.25. Compared with cgroup v1, cgroup v2 provides a single unified hierarchy, a more consistent interface, and a stronger foundation for resource isolation and modern resource-management features. Deprecation of cgroup v1 Kubernetes has deprecated cgroup v1 . Starting with Kubernetes v1.35, failCgroupV1 defaults to true , so the kubelet does not start on a cgroup v1 node by default. Administrators can temporarily set failCgroupV1: false in the kubelet configuration file , but r

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
