---
title: "Doom GPU Flame Graphs"
description: "AI Flame Graphs are now open source and include Intel Battlemage GPU support, which means it can also generate full-stack GPU flame graphs for providing new insights into gaming performance, especially when coupled with "
pubDate: 2025-04-30T14:00:00+00:00
addedAt: 2026-09-11T10:17:29.288638+00:00
source: "Brendan Gregg"
category: deep_dives
sourceUrl: "http://www.brendangregg.com/blog//2025-05-01/doom-gpu-flame-graphs.html"
tags: ["gpu"]
heat: 57
score: 0.24167
readMinutes: 1
image: "https://www.brendangregg.com/blog/images/2025/flamescopes1.png"
---

AI Flame Graphs are now open source and include Intel Battlemage GPU support, which means it can also generate full-stack GPU flame graphs for providing new insights into gaming performance, especially when coupled with FlameScope (an older open source project of mine). Here's an example of GZDoom, and I'll start with flame scopes for both CPU and GPU utilization, with details annotated: (Here are the raw CPU and GPU versions.) FlameScope shows a subsecond-offset heatmap of profile samples, where each column is one second (in this example, made up of 50 x 20ms blocks) and the color depth represents the number of samples, revealing variance and perturbation that you can select to generate a flame graph just for that time range. Update: the row size can be ajusted (it is limited by the sample rate captured in the profile), e.g., you could generate 60 rows to match 60fps games. Putting thes

*Reproduced from the Brendan Gregg feed. No model was used to write this entry — follow the link for the full article.*
