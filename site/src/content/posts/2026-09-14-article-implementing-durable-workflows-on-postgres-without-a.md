---
title: "Article: Implementing Durable Workflows on Postgres Without an External Orchestrator"
description: "Postgres can serve as the durable state store and coordination layer for workflows, eliminating the need for an external orchestrator. SKIP LOCKED enables concurrent work processing, primary-key checkpoints enforce idemp"
pubDate: 2026-09-14T11:00:00+00:00
addedAt: 2026-09-14T18:36:46.489603+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/articles/durable-workflows-postgres/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["postgres"]
heat: 90
score: 1.35914
readMinutes: 1
image: "https://res.infoq.com/articles/durable-workflows-postgres/en/headerimage/Implementing-Durable-Workflows-on-Postgres-Without-an-External-Orchestrator-header-1789129413946.jpg"
---

Postgres can serve as the durable state store and coordination layer for workflows, eliminating the need for an external orchestrator. SKIP LOCKED enables concurrent work processing, primary-key checkpoints enforce idempotency, and leases support crash recovery. Workflow sleeps and human approvals can also be persisted as database state and survive restarts. By Raman Varma

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
