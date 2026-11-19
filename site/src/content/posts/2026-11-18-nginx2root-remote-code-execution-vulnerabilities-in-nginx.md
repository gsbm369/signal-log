---
title: "NGINX2Root: Remote Code Execution vulnerabilities in nginx"
description: "Xint is reporting that it has discovered a collection of five critical vulnerabilities in the NGINX web server. The worst flaw, it says, would allow an unauthenticated attacker to execute commands on an affected nginx se"
pubDate: 2026-11-18T16:13:34+00:00
addedAt: 2026-11-19T22:43:39.043120+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1108362/"
tags: ["nginx", "vulnerab", "docker", "linux"]
heat: 86
score: 1.52284
readMinutes: 1
hnPoints: 5
hnComments: 1
buzz: 29
---

Xint is reporting that it has discovered a collection of five critical vulnerabilities in the NGINX web server. The worst flaw, it says, would allow an unauthenticated attacker to execute commands on an affected nginx server with HTTP/2 enabled . The company also reports a local-privilege escalation (LPE) kernel vulnerability , which was introduced in the 4.15 kernel, in the Stream Control Transmission Protocol (SCTP) subsystem. If chained with the NGINX vulnerability, it would allow an attacker to gain root privileges on the host. A kernel patch for this is not yet available. We also obtained a root shell on the host in a setup where nginx was running in a Docker container. On many Linux distributions, the SCTP module is installed by default and the kernel loads it automatically the first time a program opens an SCTP socket. Whether SCTP is reachable on a given host still depends on the

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
