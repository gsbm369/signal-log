---
title: "Customization: Optimizing Compiler Technology for SELF, a Dynamically-Typed Object-Oriented Programming Language (1989)"
description: "Dynamically-typed object-oriented languages please programmers, but their lack of static type information penalizes performance. Our new implementation techniques extract static type information from declaration-free pro"
pubDate: 2026-10-03T20:59:46+00:00
addedAt: 2026-10-04T18:18:46.449999+00:00
source: "Lobsters"
category: aggregators
sourceUrl: "https://dl.acm.org/doi/epdf/10.1145/74818.74831"
tags: ["tech"]
heat: 38
score: 0.33005
readMinutes: 1
---

Dynamically-typed object-oriented languages please programmers, but their lack of static type information penalizes performance. Our new implementation techniques extract static type information from declaration-free programs. Our system compiles several copies of a given procedure, each customized for one receiver type, so that the type of the receiver is bound at compile time. The compiler predicts types that are statically unknown but likely, and inserts run-time type tests to verify its predictions. It splits calls, compiling a copy on each control path, optimized to the specific types on that path. Coupling these new techniques with compile-time message lookup, aggressive procedure inlining, and traditional optimizations has doubled the performance of dynamically-typed object-oriented languages. ACM Comments

*Reproduced from the Lobsters feed. No model was used to write this entry — follow the link for the full article.*
