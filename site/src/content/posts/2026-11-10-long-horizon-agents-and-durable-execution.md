---
title: "Long-horizon agents and durable execution"
description: "Long-horizon agents can automate complex tasks that take days or weeks to complete and involve multiple exchanges with people and external systems. Many things can go wrong during this time, including process crashes, ne"
pubDate: 2026-11-10T14:10:00+00:00
addedAt: 2026-11-10T15:48:42.660125+00:00
source: "Martin Fowler"
category: system_design
sourceUrl: "https://martinfowler.com/articles/durable-execution-agents.html"
tags: ["tech"]
heat: 63
score: 0.99325
readMinutes: 1
image: "https://martinfowler.com/articles/durable-execution-agents/card.png"
hnPoints: 3
hnComments: 0
buzz: 22
---

Long-horizon agents can automate complex tasks that take days or weeks to complete and involve multiple exchanges with people and external systems. Many things can go wrong during this time, including process crashes, network failures, and unanticipated real-world behavior. Kiran Prakash explains durable execution: an emerging pattern that helps agents recover from these failures and move towards their goal. In this programming model, the runtime keeps a record of the result of each step that interacts with the outside world so that, when a failure occurs, the program runs again, completed steps are skipped, and the program's state is rebuilt from the record. more…

*Reproduced from the Martin Fowler feed. No model was used to write this entry — follow the link for the full article.*
