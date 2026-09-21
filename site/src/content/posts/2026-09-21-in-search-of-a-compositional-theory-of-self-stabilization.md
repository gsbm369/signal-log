---
title: "In Search of a Compositional Theory of Self-Stabilization"
description: "My quest for a principled solution for metastable failures has taken me back to my roots on self-stabilization, as this recent paper related the problem to composition of self-stabilizing systems. But, my literature sear"
pubDate: 2026-09-21T16:55:13+00:00
addedAt: 2026-09-21T21:17:36.839598+00:00
source: "Murat Demirbas"
category: system_design
sourceUrl: "https://muratbuffalo.blogspot.com/2026/09/in-search-of-compositional-theory-of.html"
tags: ["tech"]
heat: 90
score: 0.93302
readMinutes: 1
---

My quest for a principled solution for metastable failures has taken me back to my roots on self-stabilization, as this recent paper related the problem to composition of self-stabilizing systems. But, my literature search for recent work on composing self-stabilizing systems didn't yield anything useful. The layered stabilization idea was already in place by the early 2000s, and nothing fundamental seems to have been added since. Frustrating. So I decided to attack the problem using the concrete example I have. I had composed a rely-guarantee TLA+ model of a retry storm as two components with contracts . That model reproduces metastable failure because the composition that worked from good states failed to work when a large shock removes the base case that let the two conditions hold each other up. Searching for rely-guarantee based composition from every state, turned up a 2017 control

*Reproduced from the Murat Demirbas feed. No model was used to write this entry — follow the link for the full article.*
