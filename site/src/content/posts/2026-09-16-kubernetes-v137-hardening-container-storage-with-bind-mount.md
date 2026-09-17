---
title: "Kubernetes v1.37: Hardening Container Storage with Bind Mount Options and EmptyDir Permissions"
description: "Kubernetes v1.37 brings important storage security features: emptyDir permission modes and bind mount options. They help application programmers and security professionals implement rigorous security policies, for exampl"
pubDate: 2026-09-16T18:30:00+00:00
addedAt: 2026-09-17T10:17:47.916914+00:00
source: "Kubernetes Blog"
category: devops_linux
sourceUrl: "https://kubernetes.io/blog/2026/09/16/kubernetes-v1-37-hardening-container-storage/"
tags: ["kubernetes", "linux"]
heat: 82
score: 1.27552
readMinutes: 1
---

Kubernetes v1.37 brings important storage security features: emptyDir permission modes and bind mount options. They help application programmers and security professionals implement rigorous security policies, for example, prohibiting deletion of files across containers or execution of arbitrary binaries from writable volumes, directly in Kubernetes without any complicated circumvention. Linux storage and permission fundamentals Before diving into the new Kubernetes features, let us briefly review the low-level Linux security mechanisms that make them possible. Bind mount flags When Linux mounts or remounts a directory, Virtual File System (VFS) flags control what actions are permitted on that filesystem: noexec : Do not permit direct execution of any binaries on the mounted filesystem. nosuid : Do not allow set-user-identifier or set-group-identifier bits to take effect. nodev : Do not

*Reproduced from the Kubernetes Blog feed. No model was used to write this entry — follow the link for the full article.*
