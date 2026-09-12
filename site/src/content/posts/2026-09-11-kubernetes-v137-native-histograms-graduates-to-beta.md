---
title: "Kubernetes v1.37: Native Histograms Graduates to Beta"
description: "I'm excited to announce that native histogram support for Kubernetes metrics is graduating to Beta and is enabled by default in Kubernetes v1.37! Native histograms (previously introduced as Alpha in Kubernetes v1.36 unde"
pubDate: 2026-09-11T18:30:00+00:00
addedAt: 2026-09-12T01:04:44.451210+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/11/kubernetes-v1-37-native-histograms-beta/"
tags: ["kubernetes", "observability", "prometheus"]
heat: 100
score: 1.39389
readMinutes: 1
image: "https://kubernetes.io/images/blog/2026-kubernetes-1-37-native-histograms-beta/native-histograms-flow.svg"
imageAlt: "Diagram showing native histogram metric registration, exponential options configuration, and dual exposition flow in Kubernetes components"
---

I'm excited to announce that native histogram support for Kubernetes metrics is graduating to Beta and is enabled by default in Kubernetes v1.37! Native histograms (previously introduced as Alpha in Kubernetes v1.36 under KEP-5808 ) bring high-resolution, low-cardinality observability to Kubernetes metrics. By adopting Prometheus Native Histograms , Kubernetes components now expose latency and duration metrics with far greater accuracy while significantly reducing telemetry storage and scraping overhead. Why move beyond classic histograms? Since the early days of Kubernetes observability, duration and latency metrics (such as API server request latencies or scheduling durations) have relied on classic Prometheus histograms . Classic histograms require metric authors to define a static list of cumulative bucket boundaries ( le labels), such as 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1,

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
