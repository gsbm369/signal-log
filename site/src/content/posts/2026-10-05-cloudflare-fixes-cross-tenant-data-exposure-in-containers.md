---
title: "Cloudflare Fixes Cross-Tenant Data Exposure in Containers"
description: "Cloudflare has disclosed a cross-tenant data exposure vulnerability in Containers and Sandboxes, caused by thin-provisioned storage pools configured to skip zeroing reused blocks. Researchers recovered directory structur"
pubDate: 2026-10-05T08:48:00+00:00
addedAt: 2026-10-05T17:33:25.487666+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/cloudflare-cross-tenant-exposure/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare", "sqlite", "vulnerab", "exploit"]
heat: 92
score: 1.35274
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/cloudflare-cross-tenant-exposure/en/headerimage/generatedHeaderImage-1790844732167.jpg"
---

Cloudflare has disclosed a cross-tenant data exposure vulnerability in Containers and Sandboxes, caused by thin-provisioned storage pools configured to skip zeroing reused blocks. Researchers recovered directory structures, database pages and complete SQLite databases across four continents. Cloudflare remediated it and found no evidence of exploitation. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
