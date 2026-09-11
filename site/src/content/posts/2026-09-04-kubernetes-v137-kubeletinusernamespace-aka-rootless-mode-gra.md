---
title: "Kubernetes v1.37: KubeletInUserNamespace (aka Rootless mode) Graduates to Beta"
description: "Kubernetes v1.37 promotes the KubeletInUserNamespace feature gate to beta. With this feature enabled, all of the node components (kubelet, CRI and OCI runtimes, CNI plugins, and kube-proxy) can run as a non-root user on "
pubDate: 2026-09-04T18:30:00+00:00
addedAt: 2026-09-11T04:05:08.564278+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/"
tags: ["kubernetes", "linux"]
heat: 37
score: 0.33854
readMinutes: 1
---

Kubernetes v1.37 promotes the KubeletInUserNamespace feature gate to beta. With this feature enabled, all of the node components (kubelet, CRI and OCI runtimes, CNI plugins, and kube-proxy) can run as a non-root user on the host, using a Linux user namespace . This technique is also known as rootless mode . The work started as an experiment in 2018, and was merged into Kubernetes v1.22 (2021) as an alpha feature (Kubernetes Enhancement Proposal KEP-2033 ). This feature should not be confused with user namespaces for pods ( hostUsers: false with the UserNamespacesSupport feature gate, GA since v1.36), which puts pods in user namespaces but still runs the node components as root. These two features do not conflict. Moreover, they can be combined to nest Kubernetes inside Kubernetes without resorting to the full privileged: true . Why run the node components in a user namespace? Because the

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
