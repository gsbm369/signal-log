---
title: "Why Is My Kubernetes Job Still Pending? Tracing Kueue Admission with Headlamp"
description: "You submit a Kubernetes Job and wait for its Pods to appear. A minute passes."
pubDate: 2026-10-14T18:35:00+00:00
addedAt: 2026-10-15T03:18:05.350945+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/10/14/tracing-kueue-admission-with-headlamp/"
tags: ["kubernetes"]
heat: 92
score: 1.36547
readMinutes: 1
image: "https://kubernetes.io/blog/2026/10/14/tracing-kueue-admission-with-headlamp/kueue-admission-architecture.svg"
imageAlt: "A Kubernetes Job becomes a Kueue Workload. Kueue evaluates its LocalQueue, ClusterQueue, ResourceFlavor, and optional Cohort before resuming the Job. Headlamp reads these resources through the Kubernetes API."
---

You submit a Kubernetes Job and wait for its Pods to appear. A minute passes. Then another. The Job is still suspended, there are no application logs, and there may not even be a Pod to inspect. In a cluster managed by Kueue , this can be completely normal. Kueue may still be deciding whether the Job can use the requested resources. The useful question is not only “Why is the Pod pending?” It is first “Has Kueue admitted the Workload?” The Kueue plugin for Headlamp brings that investigation into the Headlamp UI. Instead of reconstructing the admission path from several commands and large YAML objects, you can begin with the Workload, read its condition message, and follow links through the LocalQueue, ClusterQueue, ResourceFlavor, and Cohort. This article follows that Headlamp-first path. The command line appears only in a short optional section for reproducing the example. Before you be

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
