---
title: "OpenTofu 1.13 Lets Module Authors Reduce Unknown Values at Plan Time"
description: "OpenTofu 1.13 adds convert and assume... functions that let module authors give the planner type and value hints for unknown values, so more expressions resolve during tofu plan."
pubDate: 2026-10-26T21:26:00+00:00
addedAt: 2026-10-26T22:18:30.654856+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/opentofu-1-13-unknown-values/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 74
score: 0.84694
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/opentofu-1-13-unknown-values/en/headerimage/header-1792823798248.jpeg"
---

OpenTofu 1.13 adds convert and assume... functions that let module authors give the planner type and value hints for unknown values, so more expressions resolve during tofu plan. If a value unknown during planning later violates a guarantee, OpenTofu reports an error during apply. By Mark Silvester

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
