---
title: "Kubernetes v1.37: Pod Certificates and Cluster Trust Bundles"
description: "Pod Certificate / Cluster Trust Bundles Blog Post Kubernetes brings a wealth of features that make it easy to run your production workloads securely and reliably. While aspects like scheduling, health checks and resource"
pubDate: 2026-08-28T18:30:00+00:00
addedAt: 2026-09-11T04:18:17.889704+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/08/28/kubernetes-v1-37-pod-certificates-and-cluster-trust-bundles/"
tags: ["kubernetes"]
heat: 22
score: 0.06703
readMinutes: 1
image: "https://kubernetes.io/blog/2026/08/28/kubernetes-v1-37-pod-certificates-and-cluster-trust-bundles/pod-certificates-architecture.svg"
imageAlt: "Block diagram of an application using Pod Certificates"
---

Pod Certificate / Cluster Trust Bundles Blog Post Kubernetes brings a wealth of features that make it easy to run your production workloads securely and reliably. While aspects like scheduling, health checks and resource limits are probably at the front of your mind, one other important feature of Kubernetes is production identity — how your workload can authenticate to other systems in order to do its job. Up until now, the primary production identity mechanism built into Kubernetes has been service account JWTs (JSON Web Tokens). These are cryptographically-signed tokens, issued by the control plane of your cluster, that let anyone in the world understand who is calling when your workload uses them. In Kubernetes 1.37, the foundations of a new built-in production identity technology have gone GA. Pod Certificates (and the closely-associated Cluster Trust Bundles) build X.509 certificat

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
