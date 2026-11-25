---
title: "Meaningful Human-in-the-Loop Checking of GenAI Synthesis for Restricted Languages"
description: "When the only comment on a PR is \"LGTM\", due diligence has not been done. A glance is not understanding."
pubDate: 2026-11-24T22:11:31+00:00
addedAt: 2026-11-25T04:52:46.735788+00:00
source: "Murat Demirbas"
category: system_design
sourceUrl: "https://muratbuffalo.blogspot.com/2026/11/meaningful-human-in-loop-checking-of.html"
tags: ["llm"]
heat: 83
score: 1.06278
readMinutes: 1
image: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgQy1u-kWFglEfAJ2OYEIhEXZC_X14MOxXS4IELOycuIk7cJIX5_ahesF0tNh3Ezde6LeTrpaN7pfCHy0OB_jfPdfSW75pkVtBxEzWfIiEx2lxDqN4QCYBsYW7l6SJ7ij2oyUCOcbPJRK5ktxfQi2l3gzWWyMFiC0FlX426PbmfIlLBiQq0tDmuHpGM-9I/s72-w640-h176-c/Screenshot%202026-11-24%20at%202.05.48%E2%80%AFPM.png"
hnPoints: 4
hnComments: 0
buzz: 26
---

When the only comment on a PR is "LGTM", due diligence has not been done. A glance is not understanding. Understanding has levels, and we almost always overestimate ours. But the LGTM stamps the code as correct anyway. Make no mistake (pun intended), this is also true for LLM-generated code, even with so-called "correct-by-construction" approaches. Why does verification catch anything at all? Because of redundancy. You write the specification carefully and then write the implementation separately, and the verification check finds the places where the two disagree. LLM code synthesis throws that away. It derives the implementation from the specification, so the two can almost never disagree. Correct-by-construction becomes a dangerous misnomer. If the specification is wrong, the implementation is wrong in exactly the same way. Better models will not fix this. Any move from natural languag

*Reproduced from the Murat Demirbas feed. No model was used to write this entry — follow the link for the full article.*
