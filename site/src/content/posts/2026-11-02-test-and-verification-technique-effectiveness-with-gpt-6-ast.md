---
title: "Test and verification technique effectiveness with GPT-6 Astra"
description: "When we looked at how well agents used test/verification techniques in August 1 , we saw that GPT-5.6 Sol generally did what you might call a caricature of various techniques when asked to use a technique or library such"
pubDate: 2026-11-02T00:00:00+00:00
addedAt: 2026-11-06T21:48:54.256140+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/astra-testing/"
tags: ["gpt"]
heat: 59
score: 0.96407
readMinutes: 1
hnPoints: 4
hnComments: 0
buzz: 26
---

When we looked at how well agents used test/verification techniques in August 1 , we saw that GPT-5.6 Sol generally did what you might call a caricature of various techniques when asked to use a technique or library such as TDD, QuickCheck, Lean 4, etc.; not specifying any particular test method (which we'll call Default) resulted in many worthless unit tests, which was one of the best performing conditions because asking agents to test in specific ways mostly made them worse. In that eval, we gave agents the Zstd RFC and asked them to implement Zstd (with an addendum for how they should test for all conditions other than Default). On re-running the same eval with GPT-6 Astra, we see two big differences: Astra's capability has increased by enough that we need a more difficult eval (on the Zstd implementation eval, almost every condition gets 100% correctness almost every time on medium r

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
