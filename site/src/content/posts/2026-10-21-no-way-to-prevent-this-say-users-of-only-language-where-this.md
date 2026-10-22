---
title: "\"No way to prevent this\" say users of only language where this regularly happens"
description: "In the hours following the release of CVE-2026-94300 for the project BIND 9 named , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix memory corruptio"
pubDate: 2026-10-21T00:00:00+00:00
addedAt: 2026-10-22T03:18:33.053426+00:00
source: "Xe Iaso"
category: deep_dives
sourceUrl: "https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-94300/"
tags: ["cve", "vulnerab"]
heat: 70
score: 0.87334
readMinutes: 1
image: "https://files.xeiaso.net/hero/sad-business-man.jpg"
---

In the hours following the release of CVE-2026-94300 for the project BIND 9 named , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix memory corruption in named triggered by replaying captured GSS-TSIG-signed UDP messages while the negotiated TSIG key remains valid, potentially allowing remote code execution when combined with crafted queries to an attacker-controlled zone. This is due to the affected components being written in C, the only programming language where these vulnerabilities regularly happen. This was a terrible tragedy, but sometimes these things just happen and there's nothing anyone can do to stop them, said programmer Queen Aniya Rippin, echoing statements expressed by hundreds of thousands of programmers who use the only language where 90% of the world's memory safety vulnerabilities have occurred in

*Reproduced from the Xe Iaso feed. No model was used to write this entry — follow the link for the full article.*
