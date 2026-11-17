---
title: "Presentation: Scaling LLM-Based Ranking Systems for Latency-Critical Search & Recommendation Workloads"
description: "Sundara Raman Ramachandran shares how LinkedIn productionizes LLM ranking under strict P99 latency SLAs. He discusses distilling a 7B model down to 400M parameters, compressing job contexts into single-token embeddings f"
pubDate: 2026-11-17T11:00:00+00:00
addedAt: 2026-11-17T15:48:32.105197+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/presentations/scale-llm-ranking-systems-linkedin/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["llm", "python", "embedding"]
heat: 100
score: 1.37496
readMinutes: 1
image: "https://res.infoq.com/presentations/scale-llm-ranking-systems-linkedin/en/mediumimage/SundaraRamanRamachandran-medium-1793279019345.jpeg"
hnPoints: 0
hnComments: 0
buzz: 0
---

Sundara Raman Ramachandran shares how LinkedIn productionizes LLM ranking under strict P99 latency SLAs. He discusses distilling a 7B model down to 400M parameters, compressing job contexts into single-token embeddings for a 10x throughput leap, and eliminating hidden system bottlenecks - from custom flash attention masks to Python GIL workarounds, gc.freeze, and non-blocking CUDA memory copies. By Sundara Raman Ramachandran

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
