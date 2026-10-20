---
title: "Go will reject certificate chains containing eight distrusted SPKIs"
description: "I downloaded the CA cert data from https://www.ccadb.org/resources and it seems to be affecting 16 certs, all from eMudhra. I complied the list here https://gist.github.com/mendymm/ff7a9fd00339260b4d2dbdcb0f489b57 Commen"
pubDate: 2026-10-20T03:10:23+00:00
addedAt: 2026-10-20T09:18:29.808647+00:00
source: "Lobsters"
category: aggregators
sourceUrl: "https://github.com/golang/go/commit/90617fb7ceb59cf08bee7826bb51b8c8fb8c11de"
tags: ["tech"]
heat: 82
score: 0.5922
readMinutes: 1
image: "https://opengraph.githubassets.com/061ad726258b95ec6a94417876d036e7c09a02188f0e7831a0e5d4102be97977/golang/go/commit/90617fb7ceb59cf08bee7826bb51b8c8fb8c11de"
imageAlt: "Filter a set of intermediates from chains returned by calls to Verify.
These chains are identified via SHA-256 SPKI hashes.

Fixes CVE-2026-111943
For golang/go#82345
Fixes golang/go#82349

Change-..."
---

I downloaded the CA cert data from https://www.ccadb.org/resources and it seems to be affecting 16 certs, all from eMudhra. I complied the list here https://gist.github.com/mendymm/ff7a9fd00339260b4d2dbdcb0f489b57 Comments

*Reproduced from the Lobsters feed. No model was used to write this entry — follow the link for the full article.*
