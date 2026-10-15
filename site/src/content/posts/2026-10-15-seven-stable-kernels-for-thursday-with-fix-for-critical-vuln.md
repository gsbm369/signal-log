---
title: "Seven stable kernels for Thursday with fix for critical vulnerability"
description: "Greg Kroah-Hartman has announced the release of the 7.2.11 , 6.18.57 , 6.12.113 , 6.6.159 , 6.1.190 , 5.15.223 , and 5.10.272 stable kernels. This series includes, among other things, a fix for a critical vulnerability ("
pubDate: 2026-10-15T13:01:31+00:00
addedAt: 2026-10-15T15:18:08.638846+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1100611/"
tags: ["vulnerab", "cve"]
heat: 84
score: 1.53355
readMinutes: 1
---

Greg Kroah-Hartman has announced the release of the 7.2.11 , 6.18.57 , 6.12.113 , 6.6.159 , 6.1.190 , 5.15.223 , and 5.10.272 stable kernels. This series includes, among other things, a fix for a critical vulnerability ( CVE-2026-99999 ). The flaw in skb_checksum_help() would allow an IPv4 packet with bad checksum metadata to " corrupt the network header and cause a bunch of mischief " in the words of patch author Michael S. Tsirkin. As usual, all users are advised to upgrade.

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
