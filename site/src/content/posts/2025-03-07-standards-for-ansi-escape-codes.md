---
title: "Standards for ANSI escape codes"
description: "Hello! Today I want to talk about ANSI escape codes."
pubDate: 2025-03-07T00:00:00+00:00
addedAt: 2026-09-11T10:20:27.667284+00:00
source: "jvns.ca"
category: deep_dives
sourceUrl: "https://jvns.ca/blog/2025/03/07/escape-code-standards/"
tags: ["tech"]
heat: 38
score: 0.1187
readMinutes: 1
---

Hello! Today I want to talk about ANSI escape codes. For a long time I was vaguely aware of ANSI escape codes ( that s how you make text red in the terminal and stuff ) but I had no real understanding of where they were supposed to be defined or whether or not there were standards for them. I just had a kind of vague there be dragons feeling around them. While learning about the terminal this year, I ve learned that: ANSI escape codes are responsible for a lot of usability improvements in the terminal (did you know there s a way to copy to your system clipboard when SSHed into a remote machine?? It s an escape code called OSC 52 !) They aren t completely standardized, and because of that they don t always work reliably. And because they re also invisible, it s extremely frustrating to troubleshoot escape code issues. So I wanted to put together a list for myself of some standards that ex

*Reproduced from the jvns.ca feed. No model was used to write this entry — follow the link for the full article.*
