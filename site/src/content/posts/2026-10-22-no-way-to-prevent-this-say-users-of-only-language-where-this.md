---
title: "\"No way to prevent this\" say users of only language where this regularly happens"
description: "In the hours following the release of CVE-2026-93479 for the project NGINX , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix a heap buffer overflow "
pubDate: 2026-10-22T00:00:00+00:00
addedAt: 2026-10-22T21:18:35.529395+00:00
source: "Xe Iaso"
category: deep_dives
sourceUrl: "https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-93479/"
tags: ["nginx", "cve", "vulnerab"]
heat: 82
score: 0.89523
readMinutes: 1
image: "https://stickers.xeiaso.net/sticker/cadey/coffee"
imageAlt: "Cadey is coffee"
---

In the hours following the release of CVE-2026-93479 for the project NGINX , site reliability workers and systems administrators scrambled to desperately rebuild and patch all their systems to fix a heap buffer overflow in worker script evaluation triggered by crafted requests when regex map captures are referenced before the map output, or when a non-cacheable variable is used in certain string expressions, causing worker restarts and potentially code execution if ASLR is disabled or bypassed. This is due to the affected components being written in C, the only programming language where these vulnerabilities regularly happen. This was a terrible tragedy, but sometimes these things just happen and there's nothing anyone can do to stop them, said programmer Mr. Mariano Franecki, echoing statements expressed by hundreds of thousands of programmers who use the only language where 90% of the

*Reproduced from the Xe Iaso feed. No model was used to write this entry — follow the link for the full article.*
