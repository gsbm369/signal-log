---
title: "JEP 543 Finalizes Structured Concurrency in JDK 28, Ending Seven Preview Rounds"
description: "JDK 28 finalizes structured concurrency through JEP 543, with no API changes from JDK 27. Teams on JDK 27 only need to drop --enable-preview and recompile."
pubDate: 2026-10-19T14:30:00+00:00
addedAt: 2026-10-20T03:18:31.634929+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/10/jep-543-jdk-28/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["tech"]
heat: 91
score: 0.80625
readMinutes: 1
image: "https://res.infoq.com/news/2026/10/jep-543-jdk-28/en/headerimage/generatedHeaderImage-1792296304479.jpg"
---

JDK 28 finalizes structured concurrency through JEP 543, with no API changes from JDK 27. Teams on JDK 27 only need to drop --enable-preview and recompile. Code written for JDK 25 or 26 must adapt to the R_X exception type parameter, ExecutionException wrapping, and the abstract timeout() joiner callback. By A N M Bazlur Rahman

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
