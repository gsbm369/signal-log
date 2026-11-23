---
title: "JEP 545 Moves ZGC Memory Preparation off the Startup Path in JDK 28"
description: "JEP 545, Faster Startup and Warmup with ZGC, has been integrated into JDK 28, moving heap memory preparation onto concurrent worker threads. ZGC now pre-touches memory as it expands and upgrades small pages to large ones"
pubDate: 2026-11-23T15:30:00+00:00
addedAt: 2026-11-23T15:48:12.680263+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/jep-545-jdk-28/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["linux"]
heat: 74
score: 0.97629
readMinutes: 1
image: "https://res.infoq.com/news/2026/11/jep-545-jdk-28/en/headerimage/generatedHeaderImage-1795265408975.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

JEP 545, Faster Startup and Warmup with ZGC, has been integrated into JDK 28, moving heap memory preparation onto concurrent worker threads. ZGC now pre-touches memory as it expands and upgrades small pages to large ones on Linux 6.1 and later, but the 2 MB initial heap behind the JEP's 38% startup and 90% warmup gains requires the adaptive heap sizing flag from JEP 546, which is off by default. By A N M Bazlur Rahman

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
