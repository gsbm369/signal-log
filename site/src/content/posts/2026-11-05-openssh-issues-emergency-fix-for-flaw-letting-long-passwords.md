---
title: "OpenSSH Issues Emergency Fix for Flaw Letting Long Passwords Bypass SSH Auth on Alpine Linux"
description: "Attackers can log in to accounts that have no password, such as SSH key-only accounts, on some Alpine Linux servers running the standard openssh-server package. They need network access to the server, an account name, an"
pubDate: 2026-11-05T16:42:46+00:00
addedAt: 2026-11-06T03:48:41.412489+00:00
source: "The Hacker News"
category: security
sourceUrl: "https://thehackernews.com/2026/11/openssh-issues-emergency-fix-for-flaw.html"
tags: ["linux"]
heat: 64
score: 0.91371
readMinutes: 1
image: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEieaHvS5baW_XG1eAsBsoSp9qRzV179f0WwXoj9k6rUeX4Qa4sxpi3hvpGkgkYNMPzZQH0mvvVAoTooEAgl1G3SyFksmhqNEbDEIEWM83RH47u8qvNyIYclA7z7GUdPJGx8WfJd556iCvvtvsitAYp9M-T46OvuwkaSWwnyhlynEpYax2qyTCACsPbtQLw/s1600/ssh-linux.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

Attackers can log in to accounts that have no password, such as SSH key-only accounts, on some Alpine Linux servers running the standard openssh-server package. They need network access to the server, an account name, and a password between 257 and 1,024 bytes long. OpenSSH, which rates the flaw critical, released version 10.6p2 today to block it. Alpine has published fixed packages for every

*Reproduced from the The Hacker News feed. No model was used to write this entry — follow the link for the full article.*
