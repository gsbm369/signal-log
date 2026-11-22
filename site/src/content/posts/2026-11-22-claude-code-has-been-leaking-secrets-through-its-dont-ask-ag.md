---
title: "Claude Code Has Been Leaking Secrets Through Its \"Don't Ask Again\" Feature"
description: "Agentic security firm Apiiro found that Claude Code has been exposing secrets in public repositories due to how it stores them in local file on developers' machines to implement \"Don't Ask Again\". The company identified "
pubDate: 2026-11-22T11:00:00+00:00
addedAt: 2026-11-22T15:48:12.172338+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/claude-code-leaking-secrets/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["claude"]
heat: 96
score: 1.375
readMinutes: 1
image: "https://res.infoq.com/news/2026/11/claude-code-leaking-secrets/en/headerimage/linux-6-12-real-time-1795344939763.jpeg"
hnPoints: 0
hnComments: 0
buzz: 0
---

Agentic security firm Apiiro found that Claude Code has been exposing secrets in public repositories due to how it stores them in local file on developers' machines to implement "Don't Ask Again". The company identified 1,122 secrets in claude/settings.local.json files and another 1,160 in git history, in the shared settings.json, and in agent chat transcripts stored in repos. By Sergio De Simone

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
