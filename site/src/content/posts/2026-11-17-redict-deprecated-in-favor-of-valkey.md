---
title: "Redict deprecated in favor of Valkey"
description: "Drew DeVault has announced that Redict , a fork of Redis that was created in response to Redis's 2024 license change , has been deprecated. He recommends switching to Valkey , the permissively licensed Redis fork support"
pubDate: 2026-11-17T16:20:44+00:00
addedAt: 2026-11-17T21:48:37.768777+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1108155/"
tags: ["linux", "redis"]
heat: 73
score: 1.03655
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

Drew DeVault has announced that Redict , a fork of Redis that was created in response to Redis's 2024 license change , has been deprecated. He recommends switching to Valkey , the permissively licensed Redis fork supported by the Linux Foundation. The two projects are mutually compatible, so switching should be as simple as changing which package is installed and renaming the configuration file. I had hoped to rally the Redis diaspora around a copyleft initiative, to protect ourselves from future rug-pulls, and made Redict to serve this purpose. However, with the valkey project's success, and Redis's return to a copyleft license, Redict was not able to build a sustainable community. We recommend that Redict users switch to valkey, which uses a permissive license but has better long-term prospects. We advise against switching back to Redis; though it is once again open source, and copylef

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
