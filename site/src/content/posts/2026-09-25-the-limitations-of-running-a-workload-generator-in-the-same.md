---
title: "The Limitations of Running a Workload Generator In the Same JVM as the System-Under-Test"
description: "When you evaluate a system with a garbage collector and want to understand its tail latency, you often see SPECjbb2015 or DaCapo used. While both offer corrective measures for coordinated omission, only SPECjbb2015 can r"
pubDate: 2026-09-25T00:00:00+00:00
addedAt: 2026-09-25T09:17:33.157602+00:00
source: "Inside Java"
category: languages
sourceUrl: "https://inside.java/2026/09/25/limitations-of-running-a-workload-generator-in-the-same-jvm/"
tags: ["tech"]
heat: 76
score: 0.86615
readMinutes: 1
image: "https://inside.java/resources/social-image--nAgZMYNGE8fqdi2dNsobXsdOYjHge7YemY2jQDyJc0.jpg"
imageAlt: "Inside.java - News and views from members of the Java team at Oracle"
---

When you evaluate a system with a garbage collector and want to understand its tail latency, you often see SPECjbb2015 or DaCapo used. While both offer corrective measures for coordinated omission, only SPECjbb2015 can run the workload generator and backend server in the same JVM, as well as separate them into different JVMs. This post is a deep dive that uses SPECjbb2015's flexibility to explore and highlight the risks of running the workload generator in the same JVM as the backend.

*Reproduced from the Inside Java feed. No model was used to write this entry — follow the link for the full article.*
