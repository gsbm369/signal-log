---
title: "PostgreSQL Patches 52 Flaws, Including 22-Year-Old Bug Enabling Authenticated RCE"
description: "A type confusion flaw in PostgreSQL lets a database user who can create objects run code on the server. Updates released yesterday fix it, along with 51 other security flaws."
pubDate: 2026-11-13T16:53:08+00:00
addedAt: 2026-11-14T13:16:15.747484+00:00
source: "The Hacker News"
category: security
sourceUrl: "https://thehackernews.com/2026/11/postgresql-patches-52-flaws-including.html"
tags: ["postgresql", "rce", "cve"]
heat: 85
score: 1.04119
readMinutes: 1
image: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhj8XOS7IKEt2ZhrwwdlDSpQ5hAyI46wHZpPkTQ3_hA6yUtMQpzaM50fm2v9x0O7NCt5z9vdrTsYM3iPOmu9fmmMTQDViu-rQjCfSxfCQhwZQazr4ZYayvEn5MQfUdTBVODtAay6RIaTqJGUj-HVzbtMqNPdNFiQHExhO9sitJX0GrvTx_EhWmslA-87ds/s1600/postgresql.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

A type confusion flaw in PostgreSQL lets a database user who can create objects run code on the server. Updates released yesterday fix it, along with 51 other security flaws. Full protection from this flaw also requires rebuilding any C-language extensions installed on the server. The flaw, tracked as CVE-2026-6460, has a CVSS score of 8.8. Any code run this way has the rights of the operating

*Reproduced from the The Hacker News feed. No model was used to write this entry — follow the link for the full article.*
