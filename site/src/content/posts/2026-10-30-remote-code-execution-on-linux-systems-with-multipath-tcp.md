---
title: "Remote code execution on Linux systems with multipath TCP"
description: "On October 27, LLM provider Anthropic reported on a remotely exploitable use-after-free bug affecting systems with multipath TCP listeners open. The bug works by triggering a response to a retransmitted SYN packet at the"
pubDate: 2026-10-30T15:45:27+00:00
addedAt: 2026-10-30T16:18:33.223208+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1104192/"
tags: ["linux", "kernel", "llm", "anthropic"]
heat: 100
score: 1.55922
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

On October 27, LLM provider Anthropic reported on a remotely exploitable use-after-free bug affecting systems with multipath TCP listeners open. The bug works by triggering a response to a retransmitted SYN packet at the same moment that the TCP connection is established in another thread, causing the first thread to access the connection's options structure after the second thread has freed it. The first thread can then disclose kernel memory or cause a buffer overflow, writing an attacker-controlled payload. The fix was to only free the structure after an RCU grace period . On October 29, the Go security team advised that all programs written in Go use multipath TCP by default , so many systems may be unknowingly vulnerable. And, of course, there is always the possibility of related bugs in other sections of the TCP stack. Users may be wise to update to a patched kernel as soon as one

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
