---
title: "Bringing Correctly Rounded Math to Production with LLVM-libc"
description: "As we mentioned in the last cmath blog post, MSVC is using LLVM-libc for compile-time evaluation and runtime execution of math functions when /Zc:cmath is enabled. I invited LLVM-libc contributors Michael Jones and Tue L"
pubDate: 2026-09-16T22:09:50+00:00
addedAt: 2026-09-18T19:09:05.116060+00:00
source: "C++ Team Blog"
category: languages
sourceUrl: "https://devblogs.microsoft.com/cppblog/bringing-correctly-rounded-math-to-production-with-llvm-libc/"
tags: ["tech"]
heat: 64
score: 0.74754
readMinutes: 1
image: "https://devblogs.microsoft.com/cppblog/wp-content/uploads/sites/9/2026/09/round2-1024x788.webp"
imageAlt: "Depicts a number line centered on the rounding midpoint between two representable floating-point values. The approximation interval contains the rounding midpoint."
---

As we mentioned in the last cmath blog post, MSVC is using LLVM-libc for compile-time evaluation and runtime execution of math functions when /Zc:cmath is enabled. I invited LLVM-libc contributors Michael Jones and Tue Ly to write a guest blog post about how they’ve achieved what they’ve achieved. This is that blog post! I hope [ ] The post Bringing Correctly Rounded Math to Production with LLVM-libc appeared first on C++ Team Blog .

*Reproduced from the C++ Team Blog feed. No model was used to write this entry — follow the link for the full article.*
