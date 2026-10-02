---
title: "Demoting i686 Windows targets to std-only"
description: "With Rust 1.100.0, the following changes to 32-bit Windows targets will happen: i686-pc-windows-msvc Tier 1 with host tools target will be demoted to Tier 1 without host tools. i686-pc-windows-gnu Tier 2 with host tools "
pubDate: 2026-10-02T00:00:00+00:00
addedAt: 2026-10-02T10:55:50.067142+00:00
source: "Rust Blog"
category: languages
sourceUrl: "https://blog.rust-lang.org/2026/10/02/demoting-i686-windows-targets-to-std-only/"
tags: ["rust"]
heat: 86
score: 1.09929
readMinutes: 1
image: "https://www.rust-lang.org/static/images/rust-social.jpg"
---

With Rust 1.100.0, the following changes to 32-bit Windows targets will happen: i686-pc-windows-msvc Tier 1 with host tools target will be demoted to Tier 1 without host tools. i686-pc-windows-gnu Tier 2 with host tools target will be demoted to Tier 2 without host tools. Builds of the standard library will continue to be distributed, but host tools such as the compiler will be no longer available. i686-pc-windows-msvc as a Tier 1 target still undergoes CI testing. To build 32-bit Windows binaries, cross-compiling from a still-supported host toolchain (such as a 64-bit Windows ones) will be required from now on. Background Desktop and Server 32-bit only x86 CPUs are no longer sold for over 15 years, and general 32-bit Windows support has ended in October 2025. This means that the development platforms these targets are meant for hardly exist these days, and even if they do exist they typ

*Reproduced from the Rust Blog feed. No model was used to write this entry — follow the link for the full article.*
