---
title: "Atlas Infinite: MongoDB's Disaggregated Architecture"
description: "Atlas Infinite , which dropped in public preview on September 29 alongside MongoDB 9.0, delivers a significant architectural update payload: compute-storage disaggregation. Separating compute from storage is not new , an"
pubDate: 2026-10-11T01:37:26+00:00
addedAt: 2026-10-11T16:31:29.459275+00:00
source: "Murat Demirbas"
category: system_design
sourceUrl: "https://muratbuffalo.blogspot.com/2026/10/atlas-infinite-mongodbs-disaggregated.html"
tags: ["tech"]
heat: 78
score: 0.89336
readMinutes: 1
image: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhW9MLChDtnU9vSEPJ9iFs2VboXMMsEQAsOKOfUla-cMyWXH5FwNO95BXtF8c4sI6E7Q-o02kkf6l563R91bdg_2JHDUHkpSEAJ4Z78vab_EUim3XUQli5Uj4wVVsZAJs8vAbPHJMoBEwpSVHUZqAYEcCMu8b49Awx0sVAypjv-i5p7An8-EGbeTK_PpRU/s72-w640-h360-c/image.png"
---

Atlas Infinite , which dropped in public preview on September 29 alongside MongoDB 9.0, delivers a significant architectural update payload: compute-storage disaggregation. Separating compute from storage is not new , and there are well-known ways to do it. But what makes Atlas Infinite interesting is how MongoDB departs from the standard design to keep WiredTiger's efficiency and to ensure that the shared storage layer never sees customer data unencrypted. I am giving a high level overview of the architecture here distilling from the MongoDB Engineering blog post by Abhishek Chauhan, who led the effort. For detailed coverage, I refer you to that post. It is a great read, and parts 2 and 3 will drop soon. Why not earlier, and why now Disaggregated databases have existed for some time, so why did MongoDB wait? This is mainly because MongoDB didn't need disaggregation to scale out: when a

*Reproduced from the Murat Demirbas feed. No model was used to write this entry — follow the link for the full article.*
