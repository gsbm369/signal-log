---
title: "Part 1: Simulation-first AI experimentation for ads at Grab"
description: "Introduction Ads delivery at Grab is increasingly an artificial intelligence (AI) decisioning problem. Every ad opportunity requires the system to infer user intent, predict engagement, balance advertiser returns, platfo"
pubDate: 2026-11-18T00:00:00+00:00
addedAt: 2026-11-23T09:48:10.559535+00:00
source: "Grab Engineering"
category: company_eng
sourceUrl: "https://engineering.grab.com/part-1-ads-simulation-blogpost"
tags: ["tech"]
heat: 53
score: 0.65032
readMinutes: 1
image: "https://engineering.grab.com/img/part-1-ads-simulation/figure-1.png"
imageAlt: "Workflow diagram of an ad auction from opportunity to budget update"
hnPoints: 0
hnComments: 0
buzz: 0
---

Introduction Ads delivery at Grab is increasingly an artificial intelligence (AI) decisioning problem. Every ad opportunity requires the system to infer user intent, predict engagement, balance advertiser returns, platform revenue, and user engagement, respect campaign budgets, and decide which ads should appear in a highly constrained product surface. As our ads systems become more complex, the range of bidding, ranking, and pacing strategies we need to evaluate grows with them. To continue improving quickly and safely, our approach to experimentation had to evolve: test more hypotheses offline, filter them against business and user guardrails, and reserve live traffic for the most promising ideas. Live A/B tests remain the gold standard for testing changes, but they consume real traffic, take time to gather clear signals, and expose users and advertisers’ budgets to unproven ideas. At

*Reproduced from the Grab Engineering feed. No model was used to write this entry — follow the link for the full article.*
