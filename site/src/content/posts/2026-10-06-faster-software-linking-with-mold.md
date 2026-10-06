---
title: "Faster software linking with mold"
description: "When you build a program, the compiler turns each source file into an object file. Then a linker stitches all the object files and libraries into one executable."
pubDate: 2026-10-06T08:00:20+00:00
addedAt: 2026-10-06T18:24:02.115526+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/10/06/linking-node-js-with-mold/"
tags: ["linux"]
heat: 75
score: 1.10173
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/10/Gemini_Generated_Image_8cr2v98cr2v98cr2-150x150.jpg"
---

When you build a program, the compiler turns each source file into an object file. Then a linker stitches all the object files and libraries into one executable. On Linux, the default linker is usually GNU ld (also called bfd). The GNU binutils also ship gold, an alternative linker that was designed to be faster. Continue reading Faster software linking with mold

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
