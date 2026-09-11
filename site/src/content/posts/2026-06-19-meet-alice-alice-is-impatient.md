---
title: "Meet Alice. Alice is impatient"
description: "Meet Alice. Alice is impatient."
pubDate: 2026-06-19T00:00:00+00:00
addedAt: 2026-09-11T04:18:17.890405+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/06/19/waiting.html"
tags: ["tech"]
heat: 89
score: 0.68698
readMinutes: 1
---

Meet Alice. Alice is impatient. What do you mean? Meet Alice. Alice uses your web service. Alice, like most humans, measures her time in seconds and minutes. Alice says your service is slow. You tell Alice that the mean request to your service completes in 100ms, but Alice says that her mean wait time is 1s. You’re both right. Meet Alex. Alex uses your web service. Alex, like most humans, measures his time in seconds and minutes. Alex says that when you have outages, they last a long time and he gets really annoyed. You tell Alex that your MTTR is less than 1 minute. Alex says that he sees the mean outage lasting 1 hour. Again, you’re both right. What’s going on? What’s going on is that you’re measuring time in requests, or in outages, and Alex and Alice are measuring time in seconds and minutes. When you have a long pause or a long outage, Alex and Alice sample that outage multiple time

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
