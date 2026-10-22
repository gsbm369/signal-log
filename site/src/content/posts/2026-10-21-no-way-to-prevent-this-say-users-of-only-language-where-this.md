---
title: "\"No way to prevent this\" say users of only language where this regularly happens"
description: "In the hours following the release of CVE-2026-107891 for the project musl , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix multiple integer overfl"
pubDate: 2026-10-21T00:00:00+00:00
addedAt: 2026-10-22T15:18:32.895624+00:00
source: "Xe Iaso"
category: deep_dives
sourceUrl: "https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-107891/"
tags: ["cve", "vulnerab"]
heat: 71
score: 0.83116
readMinutes: 1
image: "https://files.xeiaso.net/hero/sad-business-man.jpg"
---

In the hours following the release of CVE-2026-107891 for the project musl , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix multiple integer overflows in regcomp() when compiling untrusted regular expressions, leading to undersized allocations and possible out-of-bounds heap writes, denial of service, and arbitrary code execution. This is due to the affected components being written in C, the only programming language where these vulnerabilities regularly happen. This was a terrible tragedy, but sometimes these things just happen and there's nothing anyone can do to stop them, said programmer Dr. Otho Conroy, echoing statements expressed by hundreds of thousands of programmers who use the only language where 90% of the world's memory safety vulnerabilities have occurred in the last 50 years, and whose projects are 2

*Reproduced from the Xe Iaso feed. No model was used to write this entry — follow the link for the full article.*
