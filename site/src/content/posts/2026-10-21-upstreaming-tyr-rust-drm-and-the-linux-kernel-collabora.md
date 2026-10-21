---
title: "Upstreaming Tyr: Rust, DRM, and the Linux Kernel (Collabora)"
description: "The Collabora blog provides an update on Tyr , a driver for Arm Mali GPUs. One of our biggest challenges has been developing Tyr while the Rust kernel abstractions and driver interfaces are also being developed."
pubDate: 2026-10-21T14:58:56+00:00
addedAt: 2026-10-21T15:18:36.723553+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1102024/"
tags: ["linux", "kernel", "rust", "arm"]
heat: 100
score: 2.50963
readMinutes: 1
---

The Collabora blog provides an update on Tyr , a driver for Arm Mali GPUs. One of our biggest challenges has been developing Tyr while the Rust kernel abstractions and driver interfaces are also being developed. As the driver interfaces are naturally revised and improved, we have rewritten Tyr several times to adapt to the larger Rust ecosystem. This not only makes progress much slower than it would be with a mature API, but also stalls progress for capabilities, such as job scheduling, while the abstraction is properly designed, reviewed, tested, and merged upstream. But working in this evolving environment is also precisely where Tyr is able to provide the most value. As a user of these new Rust abstractions, Tyr helps to expose their requirements and limitations.

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
