---
title: "No More Blue Fridays"
description: "In the future, computers will not crash due to bad software updates, even those updates that involve kernel code. In the future, these updates will push eBPF code."
pubDate: 2024-07-21T14:00:00+00:00
addedAt: 2026-09-11T10:52:16.178322+00:00
source: "Brendan Gregg"
category: deep_dives
sourceUrl: "http://www.brendangregg.com/blog//2024-07-22/no-more-blue-fridays.html"
tags: ["linux", "kernel", "ebpf"]
heat: 18
score: 0.05664
readMinutes: 1
---

In the future, computers will not crash due to bad software updates, even those updates that involve kernel code. In the future, these updates will push eBPF code. Friday July 19th provided an unprecedented example of the inherent dangers of kernel programming, and has been called the largest outage in the history of information technology. Windows computers around the world encountered blue-screens-of-death and boot loops, causing outages for hospitals, airlines, banks, grocery stores, media broadcasters, and more. This was caused by a config update by a security company for their widely used product that included a kernel driver on Windows systems. The update caused the kernel driver to try to read invalid memory , an error type that will crash the kernel. For Linux systems, the company behind this outage was already in the process of adopting eBPF, which is immune to such crashes. Onc

*Reproduced from the Brendan Gregg feed. No model was used to write this entry — follow the link for the full article.*
