---
title: "Quoting Prompting Claude Fable 5.2"
description: "Claude Fable 5.2 responds closely to what the prompt says about who owns the code it works on. In Anthropic’s testing on small coding tasks, when a prompt said nothing about ownership or presented the code base as someon"
pubDate: 2026-11-10T05:34:14+00:00
addedAt: 2026-11-10T09:48:36.051255+00:00
source: "Simon Willison"
category: ai
sourceUrl: "https://simonwillison.net/2026/Nov/10/prompting-claude-fable-52/"
tags: ["claude", "anthropic"]
heat: 83
score: 1.47448
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

Claude Fable 5.2 responds closely to what the prompt says about who owns the code it works on. In Anthropic’s testing on small coding tasks, when a prompt said nothing about ownership or presented the code base as someone else’s, the model tended to add to the existing structure, even when that repeated existing code. [...] If you want the model to improve the structure as it works, say that the code is its own: This codebase is yours: what it's for and how it's built are your call, and you'll keep building on it. In Anthropic’s testing on small coding tasks, the model merged repeated code in about half of the tries with this sentence, and in under a tenth of the tries without it. Prompting Claude Fable 5.2 , Anthropic documentation Tags: prompt-engineering , anthropic , generative-ai , ai , llms , claude-mythos-fable

*Reproduced from the Simon Willison feed. No model was used to write this entry — follow the link for the full article.*
