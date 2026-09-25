---
title: "Kubernetes v1.37: Tracking When a PersistentVolumeClaim Was Last Used (Beta)"
description: "Kubernetes v1.37 promotes the PersistentVolumeClaimUnusedSinceTime feature gate to Beta (enabled by default). With this feature, the PersistentVolumeClaim (PVC) protection controller adds an Unused condition to each PVC,"
pubDate: 2026-09-21T18:30:00+00:00
addedAt: 2026-09-25T03:06:50.337047+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/21/kubernetes-v1-37-pvc-last-used-time/"
tags: ["kubernetes"]
heat: 66
score: 0.68341
readMinutes: 1
---

Kubernetes v1.37 promotes the PersistentVolumeClaimUnusedSinceTime feature gate to Beta (enabled by default). With this feature, the PersistentVolumeClaim (PVC) protection controller adds an Unused condition to each PVC, telling you whether any running pod currently references it — no custom tooling or cross-referencing required. For the API definition of PVC conditions, see the PersistentVolumeClaim API reference . Read on to learn how the Unused condition works and how to use it. Why track PVC usage? In large-scale Kubernetes clusters, it is common for users to create PVCs and then delete the associated pods without cleaning up the storage, because Kubernetes does not automatically delete PVCs when their pods are removed (to protect against accidental data loss). Over time, these orphaned PVCs may accumulate, silently consuming storage capacity and driving up cloud costs. Before Kubern

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
