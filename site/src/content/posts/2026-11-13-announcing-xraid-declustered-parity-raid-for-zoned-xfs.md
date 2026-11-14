---
title: "Announcing XRAID: declustered parity RAID for zoned XFS"
description: "Christoph Hellwig has announced the initial public release of XRAID declustered parity RAID that is integrated into XFS. The two primary aims of XRAID are to support parity RAID on zoned devices like SMR hard drives, and"
pubDate: 2026-11-13T14:39:47+00:00
addedAt: 2026-11-13T15:47:51.281809+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1107473/"
tags: ["tech"]
heat: 68
score: 0.93973
readMinutes: 1
hnPoints: 2
hnComments: 0
buzz: 18
---

Christoph Hellwig has announced the initial public release of XRAID declustered parity RAID that is integrated into XFS. The two primary aims of XRAID are to support parity RAID on zoned devices like SMR hard drives, and to provide a fast RAID implementation without inherent data integrity problems. XRAID, just like zoned XFS also works on conventional hard drives and SSDs. Optimizing for SSD performance has not been a focus, but even without that, writes are up to 20 times faster than mdraid. [...] Work on XRAID has been ongoing for a year and a half, and while we aren't anywhere near ready for an upstream submission, we are interested in feedback and testing from a wider audience now. The current implementation supports zero to 2 parities. We did experiments with the SnapRAID parity library to support 3 and more parities, and while that is not included in the current version, support f

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
