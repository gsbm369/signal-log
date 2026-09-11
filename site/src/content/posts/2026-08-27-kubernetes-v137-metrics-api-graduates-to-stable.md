---
title: "Kubernetes v1.37: Metrics API graduates to stable"
description: "Kubernetes v1.37 promotes the metrics.k8s.io API to stable ( v1 ). This API provides CPU and memory usage for nodes and Pods, and is the API behind commands such as kubectl top and resource-metrics-based autoscaling."
pubDate: 2026-08-27T18:30:00+00:00
addedAt: 2026-09-11T04:18:17.889757+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/08/27/kubernetes-v1-37-metrics-api-ga/"
tags: ["kubernetes", "k8s"]
heat: 19
score: 0.0532
readMinutes: 1
---

Kubernetes v1.37 promotes the metrics.k8s.io API to stable ( v1 ). This API provides CPU and memory usage for nodes and Pods, and is the API behind commands such as kubectl top and resource-metrics-based autoscaling. For cluster operators and application developers, this graduation means that the API now has the stability guarantees associated with a Kubernetes stable API. The v1 API has the same resource types and fields as v1beta1 ; this is an API-version graduation, not a change to the metrics that are collected or returned. A long-lived API reaches stable The resource Metrics API was introduced as alpha in Kubernetes v1.6 and became beta in v1.8. It has remained unchanged and has been used in production for years by clients including the HorizontalPodAutoscaler (HPA) and kubectl top . Kubernetes v1.37 formally graduates that proven API to metrics.k8s.io/v1 . The API exposes two resou

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
