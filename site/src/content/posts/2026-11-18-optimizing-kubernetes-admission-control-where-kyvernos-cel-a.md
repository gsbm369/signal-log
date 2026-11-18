---
title: "Optimizing Kubernetes admission control: Where Kyverno’s CEL admission cost actually goes"
description: "Kyverno s CEL (Common Expression Language)-based engines exist to evaluate policy expressions. So when we profiled the admission path, we expected to find the bulk of the cost in CEL evaluation."
pubDate: 2026-11-18T12:30:00+00:00
addedAt: 2026-11-18T15:48:33.095876+00:00
source: "CNCF"
category: devops_linux
sourceUrl: "https://www.cncf.io/blog/2026/11/18/optimizing-kubernetes-admission-control-where-kyvernos-cel-admission-cost-actually-goes/"
tags: ["kubernetes"]
heat: 75
score: 1.35856
readMinutes: 1
image: "https://www.cncf.io/wp-content/uploads/2026/11/image-14.jpg"
imageAlt: "Figure 1: heap profile of the ValidatingPolicy engine handling admission requests"
hnPoints: 0
hnComments: 0
buzz: 0
---

Kyverno s CEL (Common Expression Language)-based engines exist to evaluate policy expressions. So when we profiled the admission path, we expected to find the bulk of the cost in CEL evaluation. It was not there. About 86%...

*Reproduced from the CNCF feed. No model was used to write this entry — follow the link for the full article.*
