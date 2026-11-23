---
title: "How Grab built Scarlet: the AI teammate that turns a Slack message into a production data pipeline"
description: "Introduction In the blog From firefighting to building , we described the agents our Analytics Data Warehouse (ADW) team built to take routine work off data engineers. Scarlet was the Enhancement Agent in that post."
pubDate: 2026-11-23T00:00:00+00:00
addedAt: 2026-11-23T15:48:12.678777+00:00
source: "Grab Engineering"
category: company_eng
sourceUrl: "https://engineering.grab.com/how-grab-built-scarlet-blog"
tags: ["tech"]
heat: 67
score: 0.82274
readMinutes: 1
image: "https://engineering.grab.com/img/scarlet/figure-1.png"
hnPoints: 0
hnComments: 0
buzz: 0
---

Introduction In the blog From firefighting to building , we described the agents our Analytics Data Warehouse (ADW) team built to take routine work off data engineers. Scarlet was the Enhancement Agent in that post. It read a ticket, wrote the change, and opened a merge request (MR) for an engineer to review. A routine enhancement dropped from about a day to one or two hours. Figure 1. A pipeline change without Scarlet. Then other teams asked for it, and four limits became clear: One team only: Scarlet’s repository and conventions lived in a single system prompt sent on every request. A second team meant forking the bot. No proof the data was right: Scarlet could run a change in a test environment, but nothing checked whether the output data was correct. That hour of manual validation still fell to a person, and it was the step most often skipped. Shared access: Early versions of Scarlet

*Reproduced from the Grab Engineering feed. No model was used to write this entry — follow the link for the full article.*
