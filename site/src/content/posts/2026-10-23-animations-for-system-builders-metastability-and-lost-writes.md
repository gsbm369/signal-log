---
title: "Animations for System Builders: Metastability and Lost Writes"
description: "Animations for System Builders: Metastability and Lost Writes Pretty pictures help us learn, maybe? One of the things I love using LLMs for is helping me understand systems better."
pubDate: 2026-10-23T00:00:00+00:00
addedAt: 2026-10-23T21:18:36.349362+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/10/23/animations.html"
tags: ["tech"]
heat: 68
score: 0.87005
readMinutes: 1
---

Animations for System Builders: Metastability and Lost Writes Pretty pictures help us learn, maybe? One of the things I love using LLMs for is helping me understand systems better. In the Strands Decider post I wrote about how I often ask ask me questions to check I understand this . The other technique I’m enjoying right now, and am delighted to see folks around me using too, is building animations. Animations can help us build an intuition for how and why systems work, or how and why they fail. Here’s one example: did you know that a Raft cluster can lose writes if even one of the cluster members has a storage layer that lies about fsync() ? Your browser does not support the video tag. When I built Stability Sim , I wanted to help engineers understand metastable failures better. That worked pretty well on an abstract level (e.g. retries and queues make metastability really easy to trig

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
