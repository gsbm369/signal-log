---
title: "Show HN: Coldframe, a honeypot that poses as a supermarket fridge controller"
description: "I built Coldframe, a honeypot that pretends to be a supermarket refrigeration controller. Inspired by the events on industrial fridge installations in the past weeks, I wanted to see what people would try against a convi"
pubDate: 2026-11-07T17:27:30+00:00
addedAt: 2026-11-08T15:48:30.969430+00:00
source: "Hacker News Best"
category: aggregators
sourceUrl: "https://github.com/hedgerow-dev/coldframe"
tags: ["nginx", "python"]
heat: 41
score: 0.34044
readMinutes: 1
image: "https://opengraph.githubassets.com/9e5a002a4c781cf135c857f7f24073d80134dba1ce272838ae9f66024afc92d6/hedgerow-dev/coldframe"
imageAlt: "Low-interaction honeypot for supermarket refrigeration controllers (Danfoss AK-SM 800A, Dixell XWEB 500) - hedgerow-dev/coldframe"
hnPoints: 261
hnComments: 62
buzz: 90
---

I built Coldframe, a honeypot that pretends to be a supermarket refrigeration controller. Inspired by the events on industrial fridge installations in the past weeks, I wanted to see what people would try against a convincing fake. To learn more about this I built a honeypot that resembled perfectly the Danfoss AK-SM 800A and Dixell XWEB interfaces. Both of them are recognized on Shodan as real ones (an not as honeypots). It’s one Python file using only the standard library, and it builds on eppser/danfoss-ak-sm-decoy and public research by Synacktiv, Claroty and Ironhackers. Things that were fun to get right: - Matching real units. I used Shodan records of real devices to match header order, page titles, certificate fields and TLS versions. The Danfoss persona sends nginx headers in the same order as a real AK-SM 800A. The Dixell persona sends no Server header and pads its page to exact

*Reproduced from the Hacker News Best feed. No model was used to write this entry — follow the link for the full article.*
