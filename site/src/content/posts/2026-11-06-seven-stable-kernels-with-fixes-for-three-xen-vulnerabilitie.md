---
title: "Seven stable kernels with fixes for three Xen vulnerabilities"
description: "Hot on the heels of the previous two stable kernels , Greg Kroah-Hartman has announced the release of the 7.3.3 , 6.18.62 , 6.12.116 , 6.6.162 , 6.1.192 , 5.15.225 , and 5.10.274 stable kernels. Each one only contains fi"
pubDate: 2026-11-06T18:48:34+00:00
addedAt: 2026-11-06T21:48:54.256394+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1105902/"
tags: ["vulnerab", "cve", "privilege-escalation"]
heat: 77
score: 1.52284
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

Hot on the heels of the previous two stable kernels , Greg Kroah-Hartman has announced the release of the 7.3.3 , 6.18.62 , 6.12.116 , 6.6.162 , 6.1.192 , 5.15.225 , and 5.10.274 stable kernels. Each one only contains fixes for three use-after-free vulnerabilities announced today by the Xen security team. Two of the vulnerabilities could allow an attacker to cause a denial of service (DoS) for the entire Xen host machine with possible information leakage ( CVE-2026-100080 , CVE-2026-100082 ), and one may allow privilege escalation as well as a DoS of the host machine ( CVE-2026-100081 ). Users should, of course, upgrade if they are using Xen.

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
