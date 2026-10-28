---
title: "A report from the LPC sched_ext microconference"
description: "The Linux Plumbers Conference blog has a report from the sched_ext microconference held in Prague. Three main topics dominated the discussions Priority inversion and how to handle it in sched_ext : lock holder and lock w"
pubDate: 2026-10-28T22:11:43+00:00
addedAt: 2026-10-28T22:18:37.380702+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1103426/"
tags: ["linux"]
heat: 86
score: 1.09131
readMinutes: 1
---

The Linux Plumbers Conference blog has a report from the sched_ext microconference held in Prague. Three main topics dominated the discussions Priority inversion and how to handle it in sched_ext : lock holder and lock waiter preemption, time slice extension, and making proxy execution work together with BPF schedulers. Paravirtualized scheduling : letting the host and guest schedulers cooperate across the VM boundary, with sched_ext as the policy engine on the host. Device and topology-aware scheduling : using hardware feedback (Intel HFI), device/accelerator locality and cache topology to drive task placement.

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
