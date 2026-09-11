---
title: "\"Rules\" that terminal programs follow"
description: "Recently I ve been thinking about how everything that happens in the terminal is some combination of: Your operating system s job Your shell s job Your terminal emulator s job The job of whatever program you happen to be"
pubDate: 2024-12-12T09:28:22+00:00
addedAt: 2026-09-11T10:52:16.178264+00:00
source: "jvns.ca"
category: deep_dives
sourceUrl: "https://jvns.ca/blog/2024/11/26/terminal-rules/"
tags: ["linux"]
heat: 26
score: 0.09854
readMinutes: 1
---

Recently I ve been thinking about how everything that happens in the terminal is some combination of: Your operating system s job Your shell s job Your terminal emulator s job The job of whatever program you happen to be running (like top or vim or cat ) The first three (your operating system, shell, and terminal emulator) are all kind of known quantities if you re using bash in GNOME Terminal on Linux, you can more or less reason about how how all of those things interact, and some of their behaviour is standardized by POSIX. But the fourth one ( whatever program you happen to be running ) feels like it could do ANYTHING. How are you supposed to know how a program is going to behave? This post is kind of long so here s a quick table of contents: programs behave surprisingly consistently these are meant to be descriptive, not prescriptive it s not always obvious which rules are the progr

*Reproduced from the jvns.ca feed. No model was used to write this entry — follow the link for the full article.*
