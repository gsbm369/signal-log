---
title: "Running Apache Spark experiments in my sleep (and on a plane)"
description: "By Prashanth Gedde Narayanaswamy As one of Netflix’s largest and critical data pipelines, member-sessionizer consolidates tens of billions of hourly client events, encompassing user taps, playbacks, and engagement signal"
pubDate: 2026-10-14T19:49:11+00:00
addedAt: 2026-10-15T15:18:08.638798+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8?source=rss----2615bd06b42e---4"
tags: ["tech"]
heat: 60
score: 0.86455
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1020/1*XXIKbAHpGvPtFzHcDL8Kcg.png"
---

By Prashanth Gedde Narayanaswamy As one of Netflix’s largest and critical data pipelines, member-sessionizer consolidates tens of billions of hourly client events, encompassing user taps, playbacks, and engagement signals, into individual viewing sessions per profile. A quick two-week tuning effort spiraled into two months when standard approaches hit a wall. Because the failures only happened at full production scale, each test took hours, limiting me to just three or four attempts daily. The turning point was changing the goal: instead of trying to speed up a single run, I built a way to run and monitor multiple tests at once and track every result. That mindset led to an unconventional setup: kicking off five Spark jobs at once and monitoring them over spotty inflight Wi-Fi during a day-long trip home, while cloud servers handled the actual heavy lifting. This post covers how I set up

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
