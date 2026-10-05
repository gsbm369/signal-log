---
title: "Strands Decider: Why Not an Encoder?"
description: "Strands Decider: Why Not an Encoder? Expertise level: exhausted."
pubDate: 2026-10-04T00:00:00+00:00
addedAt: 2026-10-05T17:33:25.488018+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/10/04/encoders.html"
tags: ["llm"]
heat: 73
score: 0.92037
readMinutes: 1
image: "https://brooker.co.za/blog/images/bidi_jevbench_accuracy_brier.svg"
---

Strands Decider: Why Not an Encoder? Expertise level: exhausted. As I admitted in my last post , I am very much not an expert model developer. What follows is likely to be, at least partially, inaccurate. I have tried to be careful and quantitative, to partially balance a lack of deep expertise. Since we launched strands-decider-2B last week, a couple of people have asked me why it’s a modified LLM and not an encoder (like BERT ). Their instinct seems to be that bidirectional (i.e. each token’s representation is built from tokens before and after it) is likely to out-perform causal (i.e. only before tokens are used). This is the same reason encoders are widely used as classifiers. This is also a fair question, because if you squint at it right, we’re abusing a decoder as an encoder. To test this hypothesis, I compared five designs: v19 is the final design for Qwen3.5-based strands-decide

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
