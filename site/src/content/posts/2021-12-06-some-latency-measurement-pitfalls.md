---
title: "Some latency measurement pitfalls"
description: "This is a pseudo-transcript (actual words modified to be more readable than a 100% faithful transcription) of a short lightning talk I did at Twitter a year or two ago, on pitfalls of how we use latency metrics (with the"
pubDate: 2021-12-06T00:00:00+00:00
addedAt: 2026-09-11T11:45:59.579800+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/latency-pitfalls/"
tags: ["tech"]
heat: 5
score: 0.00117
readMinutes: 1
image: "https://danluu.com/images/latency-pitfalls/service-1.webp"
imageAlt: "Graph showing large difference between latency measured at the client vs. at the server"
---

This is a pseudo-transcript (actual words modified to be more readable than a 100% faithful transcription) of a short lightning talk I did at Twitter a year or two ago, on pitfalls of how we use latency metrics (with the actual service names anonymized per a comms request). Since this presentation, significant progress has been made on this on the infra side, so the situation is much improved over what was presented, but I think this is still relevant since, from talking to folks at peer companies, many folks are facing similar issues. We frequently use tail latency metrics here at Twitter. Most frequently, service owners want to get cluster-wide or Twitter-wide latency numbers for their services. Unfortunately, the numbers that service owners tend to use differ from what we'd like to measure due some historical quirks in our latency measurement setup: Opaque, uninstrumented, latency Lac

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
