---
title: "Kubernetes v1.37: DRA Updates"
description: "Kubernetes 1.37 is here and Dynamic Resource Allocation (DRA) keeps pushing past where it started! This release brings DRA Extended Resource support to GA, a milestone the team has been building toward for three straight"
pubDate: 2026-09-03T18:30:00+00:00
addedAt: 2026-09-11T04:15:18.672049+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/03/kubernetes-v1-37-dra-updates/"
tags: ["kubernetes", "gpu"]
heat: 48
score: 0.26825
readMinutes: 1
---

Kubernetes 1.37 is here and Dynamic Resource Allocation (DRA) keeps pushing past where it started! This release brings DRA Extended Resource support to GA, a milestone the team has been building toward for three straight releases. Several more features graduate to Beta or GA. A fresh batch of alpha features rounds out the release. I'll dive into what's new for DRA in Kubernetes 1.37! What's stable in 1.37 DRA Extended Resource support has graduated to GA. This is the mechanism that lets DRA drivers satisfy requests made through the traditional extended resource API, think example.com/gpu in a Pod spec, without requiring a separate device plugin alongside the DRA driver. An extended resource name can be set directly on a DeviceClass, and Pods requesting it get matched to a device through DRA with no ResourceClaim needed on the workload's part. It's been on a steady path since KEP acceptan

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
