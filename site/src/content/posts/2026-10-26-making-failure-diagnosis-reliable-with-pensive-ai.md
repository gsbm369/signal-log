---
title: "Making Failure Diagnosis Reliable with Pensive AI"
description: "By Praneeth Yenugutala , Victor Dusa , Anastasia Samoilova , Megan Ren , Justin Wei , Marcelo Mayworm At Netflix, data and machine learning practitioners run millions of workloads each day across orchestration systems an"
pubDate: 2026-10-26T17:04:57+00:00
addedAt: 2026-10-26T22:18:30.653498+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/making-failure-diagnosis-reliable-with-pensive-ai-6b0811a1c015?source=rss----2615bd06b42e---4"
tags: ["tech"]
heat: 77
score: 0.89035
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*2TSVpCdPYj4fMMlFPuheCg.png"
---

By Praneeth Yenugutala , Victor Dusa , Anastasia Samoilova , Megan Ren , Justin Wei , Marcelo Mayworm At Netflix, data and machine learning practitioners run millions of workloads each day across orchestration systems and compute engines such as Titus, Spark, Trino, and Druid. On peak days, roughly 100,000 workloads fail. When workloads fail, the failure itself is only the beginning. Someone still needs to find the useful signal in several logs, decide whether the cause sits in their code or the platform, and determine whether to retry, reconfigure, or escalate. Even a small share of difficult failures can consume engineering time, waste compute, and interrupt critical data pipelines. Our first answer to that problem was Pensive , an auto-diagnosis and remediation system in Netflix’s data platform. Pensive collected logs from failed workloads, used regular expressions and hand-authored J

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
