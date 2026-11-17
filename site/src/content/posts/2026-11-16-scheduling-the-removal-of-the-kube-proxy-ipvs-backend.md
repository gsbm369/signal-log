---
title: "Scheduling the removal of the kube-proxy IPVS backend"
description: "The ipvs backend for kube-proxy was an experiment in providing a service proxy implementation with better performance than the iptables backend. While it succeeded in that goal, the kernel IPVS API has turned out to be a"
pubDate: 2026-11-16T18:35:00+00:00
addedAt: 2026-11-17T03:48:36.348716+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/11/16/ipvs-removal/"
tags: ["kubernetes", "kernel"]
heat: 77
score: 0.94705
readMinutes: 1
image: "https://kubernetes.io/blog/2026/11/16/ipvs-removal/ipvs-vs-nftables.svg"
imageAlt: "kube-proxy ipvs-vs-nftables first packet latency, at various percentiles, in clusters of various sizes"
hnPoints: 0
hnComments: 0
buzz: 0
---

The ipvs backend for kube-proxy was an experiment in providing a service proxy implementation with better performance than the iptables backend. While it succeeded in that goal, the kernel IPVS API has turned out to be a bad match for the Kubernetes Services API, and the ipvs backend was never able to implement all of the edge cases of Kubernetes Service functionality correctly. In Kubernetes 1.29, the project introduced the nftables backend for kube-proxy, which became GA in 1.33. Part of the plan behind adding the nftables backend was the idea that it would eventually replace both the iptables and ipvs backends. Because the ipvs backend in particular is complex, not 100% feature complete, and architecturally quite different from the other two backends (and thus more work to maintain), Kubernetes SIG Network decided to officially deprecate it as of Kubernetes 1.35 . Although it currentl

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
