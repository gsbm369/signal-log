---
title: "Node.js Fixes 16 Flaws, Including HTTP/2 Bugs That Crash Servers and Leak Other Connections' Data"
description: "A flaw fixed in Node.js this week lets unauthenticated clients crash servers that use the runtime's built-in HTTP/2 support on the 24.x and 26.x release lines. A second HTTP/2 flaw can cause a server to send a client pie"
pubDate: 2026-11-12T08:20:37+00:00
addedAt: 2026-11-12T09:48:34.673342+00:00
source: "The Hacker News"
category: security
sourceUrl: "https://thehackernews.com/2026/11/nodejs-fixes-16-flaws-including-http2.html"
tags: ["tech"]
heat: 60
score: 0.63641
readMinutes: 1
image: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhD-9bYYTxb5WmvOmftwsTAe5hDcHyjm12YlQj320OhT6WqICBOe0D6nQf-PPslE-I0c0r8xvZdTAXfyPwGQxHWRiQ5HSIPEZGEiNrE15ygDNZCRzzVvGugdRlIq6IARQf38iJG-MN-uo7MvdXXcA0wXIGDm0-olouPSw_SbBm2-2CYGHb4uHgtREv2ycI/s1600/nodeks.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

A flaw fixed in Node.js this week lets unauthenticated clients crash servers that use the runtime's built-in HTTP/2 support on the 24.x and 26.x release lines. A second HTTP/2 flaw can cause a server to send a client pieces of its memory, including responses intended for other connections. Fixed versions were released for all three supported lines: 22.23.5, 24.22.3, and 26.13.1. The crash

*Reproduced from the The Hacker News feed. No model was used to write this entry — follow the link for the full article.*
