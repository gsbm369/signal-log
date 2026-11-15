---
title: "Strata — memory is explicit I/O"
description: "I've long thought about how we're influenced by CPU architectures, and importantly, their ISAs. In a discussion at a meetup, I brought up a topic that interested me for a while: how would an ISA that exposes memory and c"
pubDate: 2026-11-15T21:19:52+00:00
addedAt: 2026-11-15T21:48:30.460690+00:00
source: "Lobsters"
category: aggregators
sourceUrl: "https://yrashk.com/strata/"
tags: ["llm"]
heat: 72
score: 0.84687
readMinutes: 1
hnPoints: 2
hnComments: 0
buzz: 18
---

I've long thought about how we're influenced by CPU architectures, and importantly, their ISAs. In a discussion at a meetup, I brought up a topic that interested me for a while: how would an ISA that exposes memory and cache interactions in a more explicit way (because if you think about it, memory is very much I/O), as opposed to being smart and predictive on its own? An obscure interest, of course. Nevertheless, I wanted to build a quick prototype after that. What ended up transpiring was a bit larger. A multicore architecture with tiered stores, capabilities, a JIT'd emulator, Verilog RTL with a simulator, a small microkernel OS, UI, JIT Forth, an assembler in its own assembly, a bootstrapping C99 compiler, a few games, a visual debugger, and a few other things. (This also shows just how far a directed LLM process can go in little time) Comments

*Reproduced from the Lobsters feed. No model was used to write this entry — follow the link for the full article.*
