---
title: "Telling your number parser what to expect"
description: "Our fast_float library parses numbers such as -731.51 into binary floating-point values. It is part of GCC s C++ standard library, among others."
pubDate: 2026-11-10T12:44:09+00:00
addedAt: 2026-11-10T15:48:42.657526+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/11/10/telling-your-number-parser-what-to-expect/"
tags: ["tech"]
heat: 63
score: 0.98741
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/11/tunefastfloat-feature-150x150.jpg"
hnPoints: 1
hnComments: 0
buzz: 11
---

Our fast_float library parses numbers such as -731.51 into binary floating-point values. It is part of GCC s C++ standard library, among others. It is fast: often a few nanoseconds per number. Parsing a number means making decisions. Is there a sign? How many digits are there? Where is the decimal point? Is the processor rounding Continue reading Telling your number parser what to expect

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
