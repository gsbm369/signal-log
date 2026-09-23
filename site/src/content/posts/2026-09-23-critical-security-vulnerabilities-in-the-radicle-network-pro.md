---
title: "Critical security vulnerabilities in the Radicle network protocol"
description: "The Radicle peer-to-peer code-collaboration project has disclosed two critical vulnerabilities in the network protocol used by Radicle nodes. The first flaw is that the network protocol used by Radicle \" does not give th"
pubDate: 2026-09-23T14:20:46+00:00
addedAt: 2026-09-23T19:10:58.634764+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1096200/"
tags: ["vulnerab", "exploit"]
heat: 86
score: 1.49622
readMinutes: 1
---

The Radicle peer-to-peer code-collaboration project has disclosed two critical vulnerabilities in the network protocol used by Radicle nodes. The first flaw is that the network protocol used by Radicle " does not give the confidentiality it was expected to give ", which allows anyone who can observe the network between two nodes to read the data exchanged. The second is that peer authentication is broken and allows impersonation, so an attacker can spoof their Node ID and read private repositories they should not be able to read. In practice, the two flaws are most useful when they can be exploited together: an attacker on the path sees the Node IDs at both ends of a connection, and both are normally on the allow-list. That attacker can read whatever is exchanged while they watch, and can then use a Node ID they saw to fetch the whole repository on demand. The realistic threat is anyone

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
