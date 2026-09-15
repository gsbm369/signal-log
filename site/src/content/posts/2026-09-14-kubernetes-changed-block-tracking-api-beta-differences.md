---
title: "Kubernetes Changed Block Tracking API - Beta Differences"
description: "Changed Block Tracking (CBT) support for CSI drivers shipped as Alpha in September 2025. With the March 2026 v1.0.0 release of the external-snapshot-metadata project, the feature moved to Beta ."
pubDate: 2026-09-14T18:30:00+00:00
addedAt: 2026-09-15T16:29:51.926354+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/14/csi-changed-block-tracking-beta/"
tags: ["kubernetes", "k8s"]
heat: 87
score: 1.20161
readMinutes: 1
---

Changed Block Tracking (CBT) support for CSI drivers shipped as Alpha in September 2025. With the March 2026 v1.0.0 release of the external-snapshot-metadata project, the feature moved to Beta . If you aren't yet familiar with changed block tracking for storage in Kubernetes, the Alpha announcement covers the motivation, the three primary components (the CSI SnapshotMetadata gRPC service, the SnapshotMetadataService CRD, and the external-snapshot-metadata sidecar), and a walkthrough of how to use the API. CBT currently applies to block volumes; file-volume and network file-share changed-list tracking is not covered by this feature. This post focuses on what is different in Beta. What's new in Beta The main change in that release was the promotion of the SnapshotMetadataService CRD from v1alpha1 to v1beta1 . The CRD used to advertise a driver's metadata service now serves cbt.storage.k8s.

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
