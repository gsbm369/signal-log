---
title: "How a missing build flag made btop crash on Fedora with AMD GPUs"
description: "In July 2026, I opened btop on my Fedora 44 machine and the program died before drawing the first screen. The terminal returned this line: btop: src/rocm_smi.cc:136: uint64_t get_multiplier_from_str(char): Assertion `fal"
pubDate: 2026-11-25T08:00:00+00:00
addedAt: 2026-11-25T09:47:38.503251+00:00
source: "Fedora Magazine"
category: devops_linux
sourceUrl: "https://fedoramagazine.org/how-a-missing-build-flag-made-btop-crash-on-fedora-with-amd-gpus/"
tags: ["amd"]
heat: 87
score: 1.13524
readMinutes: 1
image: "https://fedoramagazine.org/wp-content/uploads/2026/11/debug_feature_image-300x127.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

In July 2026, I opened btop on my Fedora 44 machine and the program died before drawing the first screen. The terminal returned this line: btop: src/rocm_smi.cc:136: uint64_t get_multiplier_from_str(char): Assertion `false' failed. Aborted (core dumped) This article tells the story about how an ordinary user carried a fix into Fedora, and how you can do [ ]

*Reproduced from the Fedora Magazine feed. No model was used to write this entry — follow the link for the full article.*
