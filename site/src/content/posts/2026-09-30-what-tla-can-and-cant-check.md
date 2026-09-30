---
title: "What TLA+ can and can't check"
description: "Last week Boris Cherny, the inventor of Claude Code, mentioned that Opus was able to use TLA+ 1 to find race conditions in code. And now everybody on the internet is talking about formal verification."
pubDate: 2026-09-30T13:27:03+00:00
addedAt: 2026-09-30T15:17:36.065611+00:00
source: "Hillel Wayne"
category: deep_dives
sourceUrl: "https://buttondown.com/hillelwayne/archive/what-tla-can-and-cant-check/"
tags: ["claude"]
heat: 71
score: 1.1413
readMinutes: 1
image: "https://image-generator.buttondown.email/api/emphasize-subject?subject=What%20TLA%2B%20can%20and%20can%27t%20check&amp;author=Computer%20Things&amp;date=2026-09-30&amp;img="
---

Last week Boris Cherny, the inventor of Claude Code, mentioned that Opus was able to use TLA+ 1 to find race conditions in code. And now everybody on the internet is talking about formal verification. As a long-time educator ( 1 2 ) and advocate of TLA+, this is really exciting! TLA+ is great at designing complex concurrent systems and making sure they're bug-free. 2 As a long-time advocate of level-headedness, this new euphoria worries me. I read a lot of people saying that formal methods will solve the problem of agentic software development once and for all, and that's nonsense. Enough words have been spilled about the weaknesses of TLA+ in terms of what it can guarantee, like how correct designs don't automatically translate into correct code . So I'd like to focus on a different limitation for this newsletter: to verify a property, we need to have a property to verify! So what are t

*Reproduced from the Hillel Wayne feed. No model was used to write this entry — follow the link for the full article.*
