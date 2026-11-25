---
title: "Part 2: Generative bidders for ads at Grab"
description: "Introduction Grab runs marketplaces where many important decisions unfold over time, rather than as one-step predictions. Mobility systems need to anticipate how taxi demand and driver supply may evolve across locations "
pubDate: 2026-11-25T00:00:00+00:00
addedAt: 2026-11-25T04:52:46.732997+00:00
source: "Grab Engineering"
category: company_eng
sourceUrl: "https://engineering.grab.com/part-2-ads-simulation-blogpost"
tags: ["tech"]
heat: 72
score: 0.84149
readMinutes: 1
image: "https://engineering.grab.com/img/part-2-ads-simulation/figure-1.png"
imageAlt: "Flowchart of the generative bidder loop. Historical data initializes the bidder, simulated auctions produce trajectories, guardrails decide whether the policy is ready for a live experiment, and live results calibrate the simulator."
hnPoints: 0
hnComments: 0
buzz: 0
---

Introduction Grab runs marketplaces where many important decisions unfold over time, rather than as one-step predictions. Mobility systems need to anticipate how taxi demand and driver supply may evolve across locations and time windows. Food systems need to plan around changing order traffic, merchant capacity, and delivery demand. Ads has the same problem with merchant campaign budgets: traffic quality, user intent, and campaign spend opportunities change throughout the day. Prediction models estimate what may happen next, such as demand, conversion likelihood, or expected engagement. Many Grab use cases need the system to go further: generate possible future trajectories or action plans, evaluate them against business constraints, and choose a safe path forward. That is the problem generative models address. They can propose structured futures, such as demand-supply trajectories, orde

*Reproduced from the Grab Engineering feed. No model was used to write this entry — follow the link for the full article.*
