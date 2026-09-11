---
title: "In defense of simple architectures"
description: "Wave is a $1.7B company with 70 engineers 1 whose product is a CRUD app that adds and subtracts numbers. In keeping with this, our architecture is a standard CRUD app architecture, a Python monolith on top of Postgres."
pubDate: 2022-04-06T00:00:00+00:00
addedAt: 2026-09-11T11:27:00.665467+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/simple-architectures/"
tags: ["postgres", "python"]
heat: 5
score: 0.00214
readMinutes: 1
---

Wave is a $1.7B company with 70 engineers 1 whose product is a CRUD app that adds and subtracts numbers. In keeping with this, our architecture is a standard CRUD app architecture, a Python monolith on top of Postgres. Starting with a simple architecture and solving problems in simple ways where possible has allowed us to scale to this size while engineers mostly focus on work that delivers value to users. Stackoverflow scaled up a monolith to good effect ( 2013 architecture / 2016 architecture ), eventually getting acquired for $1.8B. If we look at traffic instead of market cap, Stackoverflow is among the top 100 highest traffic sites on the internet (for many other examples of valuable companies that were built on top of monoliths, see the replies to this Twitter thread . We don’t have a lot of web traffic because we’re a mobile app, but Alexa still puts our website in the top 75k even

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
