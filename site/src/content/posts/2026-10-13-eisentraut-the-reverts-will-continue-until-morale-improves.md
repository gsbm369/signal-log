---
title: "Eisentraut: The reverts will continue until morale improves"
description: "PostgreSQL core team member Peter Eisentraut has written a blog post reflecting on the \" unusually high number of features \" that have been taken out of the upcoming PostgreSQL 19 release since the beta period began. Som"
pubDate: 2026-10-13T13:21:34+00:00
addedAt: 2026-10-13T16:25:24.323360+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1100182/"
tags: ["postgresql", "llm"]
heat: 79
score: 1.06077
readMinutes: 1
---

PostgreSQL core team member Peter Eisentraut has written a blog post reflecting on the " unusually high number of features " that have been taken out of the upcoming PostgreSQL 19 release since the beta period began. Some of the reverted features had significant architectural defects that would have been hard to fix quickly and during beta. But there was also a long tail of relatively harmless issues involving various edge cases. In past times, many of these would not have surfaced until much later and we would have fixed them bit by bit over the subsequent five years. But with LLM-assisted code review, these kinds of things can get found much faster, and then you're staring at a list of like forty defect reports. And even if each of them requires only a three-line fix on average, there is a fixed overhead to dealing with each of these, and then you run out of time. Most if not all of th

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
