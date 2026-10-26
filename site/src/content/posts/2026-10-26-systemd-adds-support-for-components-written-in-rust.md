---
title: "Systemd adds support for components written in Rust"
description: "Christian Brauner has announced that he has merged support for writing leaf components of systemd in Rust. Rust will be used only for new leaf components, existing code is not being ported to Rust and nothing that other "
pubDate: 2026-10-26T15:13:59+00:00
addedAt: 2026-10-26T16:18:33.241644+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1102970/"
tags: ["systemd", "rust"]
heat: 100
score: 2.02148
readMinutes: 1
---

Christian Brauner has announced that he has merged support for writing leaf components of systemd in Rust. Rust will be used only for new leaf components, existing code is not being ported to Rust and nothing that other components depend on is written in Rust. Brauner said that the project would like to move forward with Rust support in core systemd, " but there are several blockers in Rust's support for dynamic libraries which prevents us from doing that without massively bloating every binary we build ". Assuming all goes well, it seems likely this work will appear in the systemd v263 release expected in December.

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
