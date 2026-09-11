---
title: "Kubernetes v1.37: etcd RangeStream Cuts Memory Use on Large List Reads"
description: "I am excited to announce that etcd RangeStream is graduating to beta in Kubernetes v1.37. Paired with etcd v3.7, it reduces the memory the API server and etcd need to read a large collection, and makes peak usage more pr"
pubDate: 2026-09-01T18:30:00+00:00
addedAt: 2026-09-11T04:15:18.672156+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/01/kubernetes-v1-37-etcd-range-stream/"
tags: ["kubernetes"]
heat: 36
score: 0.16899
readMinutes: 1
---

I am excited to announce that etcd RangeStream is graduating to beta in Kubernetes v1.37. Paired with etcd v3.7, it reduces the memory the API server and etcd need to read a large collection, and makes peak usage more predictable. The cost of large reads The API server serves most list and watch requests from its in-memory watch cache. Populating that cache requires reading a resource's full state from etcd, at startup and on every re-initialization. For a resource with many objects, or large ones, such as Pods, that read is expensive. The API server already paginated these reads, asking etcd for a fixed number of keys at a time rather than the whole collection at once. But a page bounded by key count has no awareness of object size, so a page of large objects can still be very large. That makes memory usage hard to predict, and a bad combination of object size and concurrent reads can b

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
