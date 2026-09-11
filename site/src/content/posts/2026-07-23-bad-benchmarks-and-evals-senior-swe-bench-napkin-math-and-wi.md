---
title: "Bad benchmarks and evals: Senior SWE-Bench, napkin math, and winter tires"
description: "We're going to look at three different kinds of benchmarks, one set of calculations for baseline numbers for performance napkin math estimates, one set of AI model evals, and one on car tires. To build my intuition for t"
pubDate: 2026-07-23T00:00:00+00:00
addedAt: 2026-09-11T04:05:08.563521+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/exercise-7/"
tags: ["benchmark"]
heat: 83
score: 1.29212
readMinutes: 1
image: "https://danluu.com/images/exercise-7/deep-swe.webp"
imageAlt: "DeepSWE leaderboard plotting score against average cost per task for various models and effort levels"
---

We're going to look at three different kinds of benchmarks, one set of calculations for baseline numbers for performance napkin math estimates, one set of AI model evals, and one on car tires. To build my intuition for things, I like thinking about them before seeing the explanation, so these are presented with the benchmark information first and the explanation later in case you want to think about your answer before seeing my thoughts. 29. A friend of mine is reviewing performance orders of magnitude to prep for computer performance interviews and found that https://github.com/sirupsen/napkin-math (5.4k stars) was the top hit. The README's tables include: Napkin Math performance estimates Operation Latency Throughput 1 MiB 1 GiB Sequential Memory R/W (64 bytes) 0.5 ns ├ Single Thread 20 GiB/s 50 μs 50 ms ├ Threaded 200 GiB/s 5 μs 5 ms Network Same-Zone 10 GiB/s 100 μs 100 ms ├ Inside V

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
