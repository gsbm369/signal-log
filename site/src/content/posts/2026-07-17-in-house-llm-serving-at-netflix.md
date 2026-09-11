---
title: "In-House LLM Serving at Netflix"
description: "By AI Platform’s Model Runtime team and Inference team Introduction Most organizations consume LLMs through hosted APIs. Netflix went further — we run the full stack ourselves, from model deployment through inference, in"
pubDate: 2026-07-17T21:32:39+00:00
addedAt: 2026-09-11T10:52:16.177628+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/in-house-llm-serving-at-netflix-a5a8e799ea2c?source=rss----2615bd06b42e---4"
tags: ["llm", "inference"]
heat: 25
score: 0.09488
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*GKGOrp0xddZwHomMhiSeCA.png"
---

By AI Platform’s Model Runtime team and Inference team Introduction Most organizations consume LLMs through hosted APIs. Netflix went further — we run the full stack ourselves, from model deployment through inference, inside our existing production environment rather than a separate ML silo. Some of those decisions weren’t obvious, and a few revealed their trade-offs only under production load. This post focuses on the choices where alternatives were seriously considered: engine selection, model packaging, API surface design, deployment strategy, and output constraints enforcement. The goal is to share not just what was built, but why — and what production revealed that the design phase didn’t anticipate. Architecture Overview Member-scale ML at Netflix is fronted by a unified JVM-based serving system that handles the end-to-end flow for downstream consumers: routing and A/B test logic,

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
