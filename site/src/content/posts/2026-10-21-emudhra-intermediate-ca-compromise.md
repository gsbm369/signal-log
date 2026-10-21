---
title: "eMudhra Intermediate CA Compromise"
description: "Private keys for eight eMudhra intermediate CA certificates have been compromised, allowing attackers to forge certificates for any site. The keys were revealed due to low entropy, not through a known breach."
pubDate: 2026-10-21T17:30:00+00:00
addedAt: 2026-10-21T21:18:33.252645+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/emudhra-ca-compromise/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["breach"]
heat: 76
score: 0.96227
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/emudhra-ca-compromise/en/headerimage/weak-link-1792602361259.jpeg"
---

Private keys for eight eMudhra intermediate CA certificates have been compromised, allowing attackers to forge certificates for any site. The keys were revealed due to low entropy, not through a known breach. Browsers blocked them using revocation lists, but other software had to remove the emSign ECC G3 root. Unpatched systems remain exposed to forged certificates, including client auth and mTLS. By Chris Swan

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
