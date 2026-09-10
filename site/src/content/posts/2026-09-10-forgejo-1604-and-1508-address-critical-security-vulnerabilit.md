---
title: "Forgejo 16.0.4 and 15.0.8 address critical security vulnerability"
description: "The Forgejo software-forge project has announced the release of versions 16.0.4 and 15.0.8 , which fixes two security vulnerabilities. One is a critical flaw that would allow remote-code execution (RCE): When generating "
pubDate: 2026-09-10T20:05:50+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1093671/"
tags: ["vulnerab", "rce"]
heat: 91
score: 1.53456
readMinutes: 1
---

The Forgejo software-forge project has announced the release of versions 16.0.4 and 15.0.8 , which fixes two security vulnerabilities. One is a critical flaw that would allow remote-code execution (RCE): When generating a new repository from a template repository, Forgejo clones the template repository, removes the .git folder, performs variable template expansion on files listed in .forgejo/template , and initializes a new git repository. During this process, variable template expansion could be misused in order to create a new .git folder, which git would adopt and incorporate during its initialization of a new git repository. A malicious template repository could be used to read arbitrary data from the Forgejo host, and to execute arbitrary processes on the Forgejo host, as a remote code execution attack. To address this issue, after variable expansion is completed, any existing .git

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
