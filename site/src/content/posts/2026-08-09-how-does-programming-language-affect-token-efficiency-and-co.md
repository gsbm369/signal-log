---
title: "How does programming language affect token efficiency and correctness?"
description: "This somewhat widely cited post (I keep seeing it cited, anyway) suggests that dynamic languages and/or languages that represent things more concisely are more token efficient. It seems to be cited enough that LLM search"
pubDate: 2026-08-09T00:00:00+00:00
addedAt: 2026-09-11T04:05:08.563859+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/pl-tokens/"
tags: ["rust", "llm"]
heat: 70
score: 0.9615
readMinutes: 1
---

This somewhat widely cited post (I keep seeing it cited, anyway) suggests that dynamic languages and/or languages that represent things more concisely are more token efficient. It seems to be cited enough that LLM search results agree. For example, when I searched for dynamic vs static language token cost (no quotes), Google's AI summary opened with Dynamically typed languages generally have a lower LLM token cost than traditional statically typed languages because omitting explicit type declarations makes the code more compact. Google's AI cited the same post, which suggests that some concise dynamic languages have maybe 1/2 to 1/3 the token cost of static languages like Rust, Go, C++, etc. The author says There was a very meaningful gap of 2.6x between C (the least token efficient language I compared) and Clojure (the most efficient). And then they later tried J, saying It dominates at

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
