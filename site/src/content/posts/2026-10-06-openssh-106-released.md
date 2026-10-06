---
title: "OpenSSH 10.6 released"
description: "Version 10.6 of OpenSSH has been released. The announcement notes that the OpenSSH team has been receiving a large number of AI-assisted security bug reports."
pubDate: 2026-10-06T13:42:48+00:00
addedAt: 2026-10-06T18:24:02.115700+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1098980/"
tags: ["tech"]
heat: 67
score: 0.90811
readMinutes: 1
---

Version 10.6 of OpenSSH has been released. The announcement notes that the OpenSSH team has been receiving a large number of AI-assisted security bug reports. " We very much welcome these reports, especially when combined with human triage, analysis, test-cases and particularly when accompanied by proposed fixes ". As a result, the project expects to be making more frequent releases to get updates to users more quickly rather than batching the bug fixes until the next planned release. Notable changes in this release include enabling the hybrid post-quantum ssh-mldsa44-ed25519 signature algorithm, addition of a -p option for sftp 's lmkdir / mkdir commands, as well as disabling the LZ77 dictionary coder in ssh and sshd to mitigate side-channel leaks (which will result in reduced effectiveness of the Compression option). The scp -R option, which allows copies between two remote hosts, is b

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
