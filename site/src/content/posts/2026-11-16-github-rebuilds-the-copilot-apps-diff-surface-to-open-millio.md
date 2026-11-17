---
title: "GitHub Rebuilds the Copilot App's Diff Surface to Open Million-Line Pull Requests Without Jank"
description: "GitHub engineers rebuilt the diff view in the Copilot app to handle a pull request with 2,200 files, over a million changed lines and 400 inline comments. The design separates fixed-height code rows from variable-height "
pubDate: 2026-11-16T10:32:00+00:00
addedAt: 2026-11-17T03:48:36.350163+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/github-pull-requests-rebuild/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 70
score: 0.79153
readMinutes: 1
image: "https://res.infoq.com/news/2026/11/github-pull-requests-rebuild/en/headerimage/generatedHeaderImage-1794747791339.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

GitHub engineers rebuilt the diff view in the Copilot app to handle a pull request with 2,200 files, over a million changed lines and 400 inline comments. The design separates fixed-height code rows from variable-height comment blocks, which are measured in batches near the viewport. Performance is checked through CI budgets and automated app runs. By Daniel Curtis

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
