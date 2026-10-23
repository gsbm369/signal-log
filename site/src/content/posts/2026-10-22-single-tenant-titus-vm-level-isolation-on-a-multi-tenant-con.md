---
title: "Single-tenant Titus: VM-level isolation on a multi-tenant container platform"
description: "Samartha Chandrashekar Nick Parker You click play on a Friday night, and in the second that follows, dozens of services answer in milliseconds. Most of them run on Titus, our internal container platform."
pubDate: 2026-10-22T22:19:12+00:00
addedAt: 2026-10-23T03:18:32.347275+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/single-tenant-titus-vm-level-isolation-on-a-multi-tenant-container-platform-6d8b1909d163?source=rss----2615bd06b42e---4"
tags: ["kubernetes", "kernel", "aws"]
heat: 100
score: 1.0244
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/0*4IREcZPdQdbU43hA.png"
---

Samartha Chandrashekar Nick Parker You click play on a Friday night, and in the second that follows, dozens of services answer in milliseconds. Most of them run on Titus, our internal container platform. Titus is, in essence, a Kubernetes-based container hosting platform: we keep both the control plane and the data plane (the container hosts that actually run containers) patched and up to date, so application teams get a consistent and reliable container experience. They hand us a container, and we run it, with no host, cluster, or kernel to own. Titus launches millions of containers every week across tens of thousands of EC2 instances in multiple AWS regions. It is multi-tenant by default: many containers from many teams share each host. That density is what makes container compute efficient, and it is why Titus has been the default home for so much of Netflix’s compute for years. For m

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
