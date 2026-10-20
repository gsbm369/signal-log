---
title: "eMudhra intermediate CA compromise"
description: "Mozilla has announced that it has received a report that private keys associated with eight eMudhra intermediate certificates have been compromised: These keys could allow attackers to issue fraudulent HTTPS certificates"
pubDate: 2026-10-20T14:56:23+00:00
addedAt: 2026-10-20T15:18:32.709027+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1101643/"
tags: ["tech"]
heat: 63
score: 0.94664
readMinutes: 1
---

Mozilla has announced that it has received a report that private keys associated with eight eMudhra intermediate certificates have been compromised: These keys could allow attackers to issue fraudulent HTTPS certificates for websites they do not control. An attacker who could intercept a user's connection could use those certificates to impersonate websites and potentially read or modify traffic. Mozilla has blocked the affected certificates using its OneCRL centralized list of revoked certificates, and has updated the trusted certificate list in Network Security Services (NSS) 3.131.1 . There is a single-page site about the compromise that goes into more detail. According to the site the certificates have also been blocked in Chrome since October 17, Apple devices since the 19th, and Microsoft blocked the certificates on the 20th. There is also a table that displays whether a browser or

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
