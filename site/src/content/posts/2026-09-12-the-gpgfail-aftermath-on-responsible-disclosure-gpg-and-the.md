---
title: "The gpg.fail aftermath: On responsible disclosure, GPG, and the state of security in 2026 [32:37]"
description: "slides In 2025, I [the speaker] found and disclosed a bunch of vulnerabilities in GPG, the most used PGP implementation, and held a talk at 39c3 about it. Some of the bugs ended up getting fixed."
pubDate: 2026-09-12T17:24:59+00:00
addedAt: 2026-09-12T22:18:15.665815+00:00
source: "Lobsters"
category: aggregators
sourceUrl: "https://media.ccc.de/v/2026-728-the-gpg-fail-aftermath-on-responsible-disclosure-gpg-and-the-state-of-security-in-2026"
tags: ["vulnerab"]
heat: 75
score: 0.71455
readMinutes: 1
image: "https://static.media.ccc.de/media/conferences/mrmcd/mrmcd26/728-0f4e284f-25df-5c1b-a4e0-0ef4d5ff00b8_preview.jpg"
---

slides In 2025, I [the speaker] found and disclosed a bunch of vulnerabilities in GPG, the most used PGP implementation, and held a talk at 39c3 about it. Some of the bugs ended up getting fixed. This talk describes the adventure and aftermath of getting there, shows some novel ones, and talks about the state of security in 2026. May contain zero-days =) Until May 2025, I liked PGP, and the GNU Privacy Guard. I poked at it in my free time a lot. One day, that suddenly changed, when I flew too close to the sun and ended up uncovering a vulnerability that allows you to easily spoof a PGP signature when opened naively with the GPG tool. Fast-forward a couple of months, the one vulnerability turned into several independent ones, up to memory corruption in the basic PGP message parser, affecting almost all PGP-related workflows. I disclosed these a few weeks before 39c3 in December 2025. And

*Reproduced from the Lobsters feed. No model was used to write this entry — follow the link for the full article.*
