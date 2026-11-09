---
title: "Extending LLDB to Debug Applications That Span CPUs and GPUs"
description: "We built a vendor-neutral accelerator plugin architecture in lldb-server for debugging applications that span CPUs and GPUs. It separates shared debugger infrastructure from hardware-specific device control."
pubDate: 2026-11-09T17:00:12+00:00
addedAt: 2026-11-09T21:48:37.766848+00:00
source: "Meta Engineering"
category: company_eng
sourceUrl: "https://engineering.fb.com/2026/11/09/developer-tools/extending-lldb-to-debug-applications-that-span-cpus-and-gpus/"
tags: ["gpu"]
heat: 61
score: 1.08173
readMinutes: 1
image: "https://engineering.fb.com/wp-content/uploads/2026/11/Extending-LLDB.png"
hnPoints: 0
hnComments: 0
buzz: 0
---

We built a vendor-neutral accelerator plugin architecture in lldb-server for debugging applications that span CPUs and GPUs. It separates shared debugger infrastructure from hardware-specific device control. The design represents the CPU and GPU as separate debugger processes while presenting them in one debugging session. Modern AI applications rarely execute in one place. A workload can [...] Read More... The post Extending LLDB to Debug Applications That Span CPUs and GPUs appeared first on Engineering at Meta .

*Reproduced from the Meta Engineering feed. No model was used to write this entry — follow the link for the full article.*
