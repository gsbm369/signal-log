---
title: "\"No way to prevent this\" say users of only language where this regularly happens"
description: "In the hours following the release of CVE-2026-123633 and CVE-2026-123007 for the project NGINX , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix an"
pubDate: 2026-11-18T00:00:00+00:00
addedAt: 2026-11-18T15:48:33.095790+00:00
source: "Xe Iaso"
category: deep_dives
sourceUrl: "https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-123633/"
tags: ["nginx", "cve", "vulnerab"]
heat: 59
score: 0.91579
readMinutes: 1
image: "https://files.xeiaso.net/hero/sad-business-man.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

In the hours following the release of CVE-2026-123633 and CVE-2026-123007 for the project NGINX , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix an HTTP/2 connection use-after-free during reverse-proxy processing when connection slots run low, alongside an HTTP/2 flow-control integer underflow that leads to an out-of-bounds memory copy over TLS, both of which can allow unauthenticated remote code execution on affected servers with HTTP/2 enabled. This is due to the affected components being written in C, the only programming language where these vulnerabilities regularly happen. This was a terrible tragedy, but sometimes these things just happen and there's nothing anyone can do to stop them, said programmer Dr. Deontae Rempel, echoing statements expressed by hundreds of thousands of programmers who use the only lan

*Reproduced from the Xe Iaso feed. No model was used to write this entry — follow the link for the full article.*
