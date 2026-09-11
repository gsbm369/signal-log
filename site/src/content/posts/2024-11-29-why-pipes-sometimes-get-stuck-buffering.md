---
title: "Why pipes sometimes get \"stuck\": buffering"
description: "Here s a niche terminal problem that has bothered me for years but that I never really understood until a few weeks ago. Let s say you re running this command to watch for some specific output in a log file: tail -f /som"
pubDate: 2024-11-29T08:23:31+00:00
addedAt: 2026-09-11T11:03:46.192352+00:00
source: "jvns.ca"
category: deep_dives
sourceUrl: "https://jvns.ca/blog/2024/11/29/why-pipes-get-stuck-buffering/"
tags: ["tech"]
heat: 23
score: 0.08149
readMinutes: 1
---

Here s a niche terminal problem that has bothered me for years but that I never really understood until a few weeks ago. Let s say you re running this command to watch for some specific output in a log file: tail -f /some/log/file | grep thing1 | grep thing2 If log lines are being added to the file relatively slowly, the result I d see is nothing! It doesn t matter if there were matches in the log file or not, there just wouldn t be any output. I internalized this as uh, I guess pipes just get stuck sometimes and don t show me the output, that s weird , and I d handle it by just running grep thing1 /some/log/file | grep thing2 instead, which would work. So as I ve been doing a terminal deep dive over the last few months I was really excited to finally learn exactly why this happens. why this happens: buffering The reason why pipes get stuck sometimes is that it s VERY common for programs

*Reproduced from the jvns.ca feed. No model was used to write this entry — follow the link for the full article.*
