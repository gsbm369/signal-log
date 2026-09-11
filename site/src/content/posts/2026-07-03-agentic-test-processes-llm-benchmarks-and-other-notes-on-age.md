---
title: "Agentic test processes, LLM benchmarks, and other notes on agentic coding from Galapagos Island"
description: "I've been using AI fairly heavily since last November and the whole thing is a funny experience . An agent will do something that, if a human did it, you'd immediately fire them."
pubDate: 2026-07-03T00:00:00+00:00
addedAt: 2026-09-11T04:05:08.563333+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/ai-coding/"
tags: ["llm", "benchmark", "gpt"]
heat: 93
score: 1.55887
readMinutes: 1
---

I've been using AI fairly heavily since last November and the whole thing is a funny experience . An agent will do something that, if a human did it, you'd immediately fire them. My reaction, of course, is to act as if this is great and spin up a thousand agents so they can do even more of that. Mid-last year, I had GPT (maybe 5.0 or 5.1) try to find the source of a bug . Naturally, this code didn't have tests and git bisect wouldn't work, and it was a UI interaction bug for which I'm not even really qualified to write a test for, so I asked Codex to bisect between dates X and Y to find the commit that introduced this bug. Codex immediately told me the offending commit was after this date range (which couldn't possibly be correct). On telling Codex this was wrong, it then told me some commit that was obviously also not the offending commit once or twice. On telling it those were wrong, i

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
