---
title: "Scaling Kubernetes Workloads with Node Swap"
description: "Memory is often the first hard limit a Kubernetes cluster hits. Nodes run out of RAM long before they run out of CPU, and the new wave of agentic AI workloads makes this worse."
pubDate: 2026-10-05T18:00:00+00:00
addedAt: 2026-10-06T18:24:02.115574+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/10/05/scaling-kubernetes-workloads-with-node-swap/"
tags: ["kubernetes", "kernel", "python", "benchmark"]
heat: 78
score: 1.17414
readMinutes: 1
image: "https://kubernetes.io/blog/2026/10/05/scaling-kubernetes-workloads-with-node-swap/node-swap-chart.svg"
---

Memory is often the first hard limit a Kubernetes cluster hits. Nodes run out of RAM long before they run out of CPU, and the new wave of agentic AI workloads makes this worse. These workloads demand large memory footprints to start up and run untrusted code, then sit idle waiting for the next prompt. That idle but resident memory is expensive, and it caps how many pods a node can hold. This is where swap helps. Kubernetes support for running nodes with swap enabled reached General Availability in v1.34, and by backing that swap with fast NVMe solid state drives (SSDs), a node can page out dormant memory and pack in far more pods. This post explains how we benchmarked that approach across three workloads, including CI/CD kernel builds, sandboxed headless browsers, and isolated Python runtimes; we found density gains of up to 3×, often with little or no latency cost. The node density prob

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
