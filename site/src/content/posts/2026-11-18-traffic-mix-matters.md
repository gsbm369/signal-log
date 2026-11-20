---
title: "Traffic mix matters"
description: "Traffic mix matters Wanna listen to my mixtape? The preliminary report on last week’s M365 outage contains one statement that really caught my eye: Our normal load testing did not detect the latent issue because [of] the"
pubDate: 2026-11-18T00:00:00+00:00
addedAt: 2026-11-20T03:48:26.615528+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/11/18/workload-mix.html"
tags: ["tech"]
heat: 49
score: 0.76719
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

Traffic mix matters Wanna listen to my mixtape? The preliminary report on last week’s M365 outage contains one statement that really caught my eye: Our normal load testing did not detect the latent issue because [of] the traffic mix and SKUs used in our labs. There’s a lot going on in this report (as there is in any report for a complex system), but I wanted to zoom in on this one issue: traffic mix . It’s important, because its the one thing that makes the difference between a great load test and a complete waste of time. The performance of computer systems is extremely sensitive to workload mix. Let’s start with a simple simulator, looking at a system with a table of locks. Requests arrive with a key, hold the lock for their key for some period of time, and then free the lock and complete. This isn’t an unreasonable mental model of a relational database, where each transaction takes a

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
