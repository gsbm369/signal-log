---
title: "How Google Traced GKE API Timeouts to a Linux Kernel TCP Bug"
description: "Google recently detailed how three interacting bugs across Google Kubernetes Engine (GKE), Private Service Connect, and the Linux kernel caused intermittent Kubernetes API connectivity failures, blocking around 800 devel"
pubDate: 2026-11-21T09:44:00+00:00
addedAt: 2026-11-21T19:18:13.668503+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/gke-kernel-network-bug/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["linux", "kernel", "kubernetes"]
heat: 92
score: 1.75677
readMinutes: 1
image: "https://res.infoq.com/news/2026/11/gke-kernel-network-bug/en/headerimage/generatedHeaderImage-1794082671635.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

Google recently detailed how three interacting bugs across Google Kubernetes Engine (GKE), Private Service Connect, and the Linux kernel caused intermittent Kubernetes API connectivity failures, blocking around 800 developers from deploying to production. By Renato Losio

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
