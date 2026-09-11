---
title: "Importing a frontend Javascript library without a build system"
description: "I like writing Javascript without a build system and for the millionth time yesterday I ran into a problem where I needed to figure out how to import a Javascript library in my code without using a build system, and it t"
pubDate: 2024-11-18T09:35:42+00:00
addedAt: 2026-09-11T11:06:03.517140+00:00
source: "jvns.ca"
category: deep_dives
sourceUrl: "https://jvns.ca/blog/2024/11/18/how-to-import-a-javascript-library/"
tags: ["tech"]
heat: 48
score: 0.07812
readMinutes: 1
---

I like writing Javascript without a build system and for the millionth time yesterday I ran into a problem where I needed to figure out how to import a Javascript library in my code without using a build system, and it took FOREVER to figure out how to import it because the library s setup instructions assume that you re using a build system. Luckily at this point I ve mostly learned how to navigate this situation and either successfully use the library or decide it s too difficult and switch to a different library, so here s the guide I wish I had to importing Javascript libraries years ago. I m only going to talk about using Javacript libraries on the frontend, and only about how to use them in a no-build-system setup. In this post I m going to talk about: the three main types of Javascript files a library might provide (ES Modules, the classic global variable kind, and CommonJS) how t

*Reproduced from the jvns.ca feed. No model was used to write this entry — follow the link for the full article.*
