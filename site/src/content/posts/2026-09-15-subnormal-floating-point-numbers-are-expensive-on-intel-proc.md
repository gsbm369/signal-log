---
title: "Subnormal floating-point numbers are expensive… on Intel processors"
description: "We represent floating-point numbers using the IEEE standard. For very small numbers, the standard uses special subnormal numbers."
pubDate: 2026-09-15T12:54:32+00:00
addedAt: 2026-09-19T17:01:05.808716+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/09/15/subnormal-floating-point-numbers-are-expensive-on-intel-processors/"
tags: ["tech"]
heat: 93
score: 0.66164
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/09/Gemini_Generated_Image_gh1asmgh1asmgh1a-150x150.jpg"
---

We represent floating-point numbers using the IEEE standard. For very small numbers, the standard uses special subnormal numbers. Unfortunately, they have a reputation of making operations slow. Thus video game programmers and machine learning specialists sometimes avoid computing with subnormal numbers for performance. How slow are they? Let me measure. I wrote a small C++ Continue reading Subnormal floating-point numbers are expensive on Intel processors

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
