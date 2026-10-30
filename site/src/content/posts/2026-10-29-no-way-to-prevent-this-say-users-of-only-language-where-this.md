---
title: "\"No way to prevent this\" say users of only language where this regularly happens"
description: "In the hours following the release of CVE-2026-98432 for the project Linux , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix a use-after-kfree where"
pubDate: 2026-10-29T00:00:00+00:00
addedAt: 2026-10-30T04:18:35.918225+00:00
source: "Xe Iaso"
category: deep_dives
sourceUrl: "https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-98432/"
tags: ["linux", "cve", "vulnerab"]
heat: 95
score: 0.86975
readMinutes: 1
image: "https://files.xeiaso.net/hero/sad-business-man.jpg"
---

In the hours following the release of CVE-2026-98432 for the project Linux , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix a use-after-kfree where retransmitting a crafted connection request while finishing the handshake of that same connection causes funny things to happen up to and including arbitrary code execution. This is due to the affected components being written in C, the only programming language where these vulnerabilities regularly happen. This was a terrible tragedy, but sometimes these things just happen and there's nothing anyone can do to stop them, said programmer Prince Julien Hoppe, echoing statements expressed by hundreds of thousands of programmers who use the only language where 90% of the world's memory safety vulnerabilities have occurred in the last 50 years, and whose projects are 20 times

*Reproduced from the Xe Iaso feed. No model was used to write this entry — follow the link for the full article.*
