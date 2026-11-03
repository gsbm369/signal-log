---
title: "Announcing rustup 1.29.3"
description: "The rustup team has published a new point release of rustup, 1.29.3. Rustup is the recommended tool to install Rust , a programming language that empowers everyone to build reliable and efficient software."
pubDate: 2026-11-03T00:00:00+00:00
addedAt: 2026-11-03T16:18:36.486894+00:00
source: "Rust Blog"
category: languages
sourceUrl: "https://blog.rust-lang.org/2026/11/03/Rustup-1.29.3/"
tags: ["rust"]
heat: 76
score: 1.07517
readMinutes: 1
image: "https://www.rust-lang.org/static/images/rust-social.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

The rustup team has published a new point release of rustup, 1.29.3. Rustup is the recommended tool to install Rust , a programming language that empowers everyone to build reliable and efficient software. What's new in rustup 1.29.3 This new patch release has fixed some minor regressions over the previous one: Fixed "Illegal instruction" error on certain x86_64 CPUs without SSE4.1. pr#5162 Fixed " lock() not supported" error on Solaris. pr#5167 Further details are available in the changelog ! How to update If you have a previous version of rustup installed, getting the new one is as easy as stopping any programs which may be using rustup (e.g. closing your IDE) and running: $ rustup self update Rustup will also automatically update itself at the end of a normal toolchain update: $ rustup update For this particular release, if you have encountered any issues during self-update, you may t

*Reproduced from the Rust Blog feed. No model was used to write this entry — follow the link for the full article.*
