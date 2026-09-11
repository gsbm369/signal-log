---
title: "Kubernetes v1.37: Storage Version Migration Enabled by Default"
description: "I am excited that storage version migration (SVM) has graduated to General Availability (GA) in Kubernetes v1.37! After a number of releases of work and testing, the built-in StorageVersionMigration API ( storagemigratio"
pubDate: 2026-08-31T18:30:00+00:00
addedAt: 2026-09-11T04:18:17.889652+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/08/31/kubernetes-v1-37-storage-version-migration-ga/"
tags: ["kubernetes", "k8s"]
heat: 33
score: 0.13406
readMinutes: 1
---

I am excited that storage version migration (SVM) has graduated to General Availability (GA) in Kubernetes v1.37! After a number of releases of work and testing, the built-in StorageVersionMigration API ( storagemigration.k8s.io/v1 ) and control plane controller are now fully stable and enabled by default across all v1.37 Kubernetes clusters. The problem with stale storage versions In Kubernetes, stored API resources are written using a specific storage version (schema representation). The way Kubernetes interacts with object storage fundamentally requires mutation of a resource in order to ensure that the latest storage version is used for all resources. This creates problems when you want to change the storage version of a resource. One example of a scenario where you may want to change the storage version of a resource is when you are promoting a CRD to drop an older API version (such

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
