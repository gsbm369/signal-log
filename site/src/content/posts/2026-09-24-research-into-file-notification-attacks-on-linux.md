---
title: "Research into file-notification attacks on Linux"
description: "Sudheendra Raghav Neela, a member of a group of researchers from Graz University of Technology , has announced the release of research into file-notification attacks that would allow spying on user activity on Android, L"
pubDate: 2026-09-24T17:40:36+00:00
addedAt: 2026-09-24T18:07:10.624904+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1096431/"
tags: ["linux", "vulnerab"]
heat: 85
score: 1.56087
readMinutes: 1
---

Sudheendra Raghav Neela, a member of a group of researchers from Graz University of Technology , has announced the release of research into file-notification attacks that would allow spying on user activity on Android, Linux, macOS, and Windows. The group has published a paper with details on the research as well as a web site with demonstrations of the vulnerabilities. On Linux, an attacker can use inotifywatch to monitor a directory to conduct an inter-keystroke timing attack even if they do not have read access to the files within a directory. The group also discovered a method to conduct a UI-redress attack (or " clickjacking " attack) on KDE 5 and KDE 6 by monitoring /usr/bin/pkexec to detect when Polkit spawns an authentication prompt. An attacker could draw a fake password window on top of the real window to collect a user's credentials. Both of these flaws are still present today

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
