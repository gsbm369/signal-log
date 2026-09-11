---
title: "AI Flame Graphs"
description: "Imagine halving the resource costs of AI and what that could mean for the planet and the industry -- based on extreme estimates such savings could reduce the total US power usage by over 10% by 2030 1 . At Intel we've be"
pubDate: 2024-10-28T13:00:00+00:00
addedAt: 2026-09-11T10:20:27.667361+00:00
source: "Brendan Gregg"
category: deep_dives
sourceUrl: "http://www.brendangregg.com/blog//2024-10-29/ai-flame-graphs.html"
tags: ["kernel", "gpu", "data-center"]
heat: 31
score: 0.08292
readMinutes: 1
image: "https://www.brendangregg.com/blog/images/2024/matrixAIflamegraph.png"
---

Imagine halving the resource costs of AI and what that could mean for the planet and the industry -- based on extreme estimates such savings could reduce the total US power usage by over 10% by 2030 1 . At Intel we've been creating a new analyzer tool to help reduce AI costs called AI Flame Graphs : a visualization that shows an AI accelerator or GPU hardware profile along with the full software stack, based on my CPU flame graphs . Our first version is available to customers in the Intel Tiber AI Cloud as a preview for the Intel Data Center GPU Max Series (previously called Ponte Vecchio). Here is an example: Simple example: SYCL matrix multiply microbenchmark (Click for interactive SVG .) The green frames are the actual instructions running on the AI or GPU accelerator, aqua shows the source code for these functions, and red (C), yellow (C++), and orange (kernel) show the CPU code path

*Reproduced from the Brendan Gregg feed. No model was used to write this entry — follow the link for the full article.*
