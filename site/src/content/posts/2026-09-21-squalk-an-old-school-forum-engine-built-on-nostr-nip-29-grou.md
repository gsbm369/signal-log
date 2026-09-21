---
title: "Squalk: an old-school forum engine built on Nostr (NIP-29 groups, NIP-7D threads)"
description: "I miss classic forums: slow, asynchronous threads that stay readable and searchable for years, instead of knowledge dissolving into chat scrollback. Squalk is my attempt to rebuild that on top of Nostr, an open protocol "
pubDate: 2026-09-21T14:44:12+00:00
addedAt: 2026-09-21T15:17:36.728860+00:00
source: "Lobsters"
category: aggregators
sourceUrl: "https://github.com/dtonon/squalk"
tags: ["tech"]
heat: 64
score: 0.73413
readMinutes: 1
image: "https://opengraph.githubassets.com/da94c1415bb8adb3a909e35a922e1951462bc15124b469a5637b6a1ad569e52c/dtonon/squalk"
imageAlt: "A forum + chat built on Nostr to manage your community - dtonon/squalk"
---

I miss classic forums: slow, asynchronous threads that stay readable and searchable for years, instead of knowledge dissolving into chat scrollback. Squalk is my attempt to rebuild that on top of Nostr, an open protocol where users hold a keypair, posts are signed events, and interchangeable relays store and serve them, instead of a private database. The design in short: a forum is a view over relay-hosted data. Rooms are groups as specified in NIP-29, threads are NIP-7D events, identity is the user's own keypair. The consequence I care about is that the software and the community are decoupled: any other client speaking the same specs (Flotilla, Nostrord) can read and write the same conversations, and if my deployment disappears the history and identities survive on the relay. Technical bits that might interest this crowd: one SvelteKit codebase builds either as a static SPA or as a ser

*Reproduced from the Lobsters feed. No model was used to write this entry — follow the link for the full article.*
