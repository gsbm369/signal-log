---
title: "Announcing Rust 1.99.1"
description: "The Rust team has published a new point release of Rust, 1.99.1. Rust is a programming language that is empowering everyone to build reliable and efficient software."
pubDate: 2026-10-15T00:00:00+00:00
addedAt: 2026-10-15T21:18:18.884700+00:00
source: "Rust Blog"
category: languages
sourceUrl: "https://blog.rust-lang.org/2026/10/15/Rust-1.99.1/"
tags: ["rust"]
heat: 98
score: 1.51118
readMinutes: 1
image: "https://www.rust-lang.org/static/images/rust-social.jpg"
---

The Rust team has published a new point release of Rust, 1.99.1. Rust is a programming language that is empowering everyone to build reliable and efficient software. If you have a previous version of Rust installed via rustup, getting Rust 1.99.1 is as easy as: rustup update stable If you don't have it already, you can get rustup from the appropriate page on our website. What's in 1.99.1 Rust 1.99.1 fixes the following regressions from prior releases: Missing symbol wcslen : Some Rust targets were getting link errors for missing wcslen , and that function is now present in Rust's compiler-builtins library as a fallback. The LLVM loop-idiom-wcslen pass may introduce calls to wcslen as an optimization, and some Rust targets did not have that function readily available in libc or elsewhere. The UEFI targets in particular were broken for any project using std , as some of these calls were in

*Reproduced from the Rust Blog feed. No model was used to write this entry — follow the link for the full article.*
