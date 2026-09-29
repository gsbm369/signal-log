---
title: "Python Workers Reach GA on Cloudflare, with Questions About Cold Starts and Upstream Maintenance"
description: "Cloudflare has made Python Workers generally available, built on PEP 783 and on socket syscalls implemented over the Workers connect API. The announcement carries no performance figures."
pubDate: 2026-09-29T06:33:00+00:00
addedAt: 2026-09-29T18:17:27.591144+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/09/cloudflare-python-workers-ga/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["cloudflare", "python"]
heat: 99
score: 1.7411
readMinutes: 1
image: "https://www.infoq.com/styles/static/images/logo/logo_bigger.jpg"
---

Cloudflare has made Python Workers generally available, built on PEP 783 and on socket syscalls implemented over the Workers connect API. The announcement carries no performance figures. A urllib3 maintainer questioned who supports the upstream work afterwards, and Wasmer's founder asked for cold-start numbers, citing about 1.027 seconds from Cloudflare's own earlier post. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
