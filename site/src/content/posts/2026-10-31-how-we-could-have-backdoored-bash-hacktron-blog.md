---
title: "How We Could Have Backdoored Bash (Hacktron blog)"
description: "The Hacktron blog documents how the group was able to compromise the GNU Savannah forge and could have pushed malware into any of the projects hosted there. Using Hacktron, we found that an email address like `touch${IFS"
pubDate: 2026-10-31T14:00:42+00:00
addedAt: 2026-10-31T16:18:33.120916+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1104262/"
tags: ["kernel", "rce"]
heat: 88
score: 1.06862
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

The Hacktron blog documents how the group was able to compromise the GNU Savannah forge and could have pushed malware into any of the projects hosted there. Using Hacktron, we found that an email address like `touch${IFS}/tmp/savane-rce-proof`@attacker.example gave any registered user code execution on its backend. From there, we made our account a superuser, impersonated Bash's maintainer, and confirmed we could add an SSH key with push access to the upstream Bash repository. An unpatched kernel gave us root access and access to a GNU backup server. We reported it to the FSF on May 11, 2026.

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
