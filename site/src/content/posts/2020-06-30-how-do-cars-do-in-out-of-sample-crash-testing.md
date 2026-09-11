---
title: "How do cars do in out-of-sample crash testing?"
description: "Any time you have a benchmark that gets taken seriously, some people will start gaming the benchmark. Some famous examples in computing are the CPU benchmark specfp and video game benchmarks."
pubDate: 2020-06-30T07:06:34+00:00
addedAt: 2026-09-11T21:25:45.639850+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/car-safety/"
tags: ["kernel", "benchmark", "gpu"]
heat: 5
score: 0.00018
readMinutes: 1
---

Any time you have a benchmark that gets taken seriously, some people will start gaming the benchmark. Some famous examples in computing are the CPU benchmark specfp and video game benchmarks. With specfp, Sun managed to increase its score on 179.art (a sub-benchmark of specfp) by 12x with a compiler tweak that essentially re-wrote the benchmark kernel, which increased the Sun UltraSPARC ’s overall specfp score by 20%. At times, GPU vendors have added specialized benchmark-detecting code to their drivers that lowers image quality during benchmarking to produce higher benchmark scores. Of course, gaming the benchmark isn't unique to computing and we see people do this in other fields . It’s not surprising that we see this kind of behavior since improving benchmark scores by cheating on benchmarks is much cheaper (and therefore higher ROI) than improving benchmark scores by actually improvi

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
