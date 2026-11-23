---
title: "Replaying merged changes: how we test whether a knowledge base makes coding agents better"
description: "Introduction Every session, you get a new teammate: a coding agent. It reads code faster than you and has seen more of it than your whole team put together."
pubDate: 2026-11-23T00:00:00+00:00
addedAt: 2026-11-23T15:48:12.678724+00:00
source: "Grab Engineering"
category: company_eng
sourceUrl: "https://engineering.grab.com/replaying-merged-changes-knowledge-base-coding-agents-better"
tags: ["tech"]
heat: 67
score: 0.82274
readMinutes: 1
image: "https://engineering.grab.com/img/coding-agents-better/figure-1a.png"
imageAlt: "Table of knowledge base layers and how agents use each one"
hnPoints: 0
hnComments: 0
buzz: 0
---

Introduction Every session, you get a new teammate: a coding agent. It reads code faster than you and has seen more of it than your whole team put together. What it does not have is any memory of how your service got this way. It can see what the code does. It cannot see why a limit lives in configuration, which nightly job breaks if you touch a shared client, or what an old review thread settled. So it asks, or it guesses. We built a knowledge base to fill that gap. For each backend service, it maps how requests move through the code, what a change could break, which configuration values the code runs with, and why the team made the calls it did. Agents load it before they touch a service. The harder part was knowing whether it helped. A plan that reads well can still be wrong, and every agent session starts from scratch, so you cannot watch an agent improve the way you watch a new hire

*Reproduced from the Grab Engineering feed. No model was used to write this entry — follow the link for the full article.*
