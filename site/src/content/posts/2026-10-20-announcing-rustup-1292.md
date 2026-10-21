---
title: "Announcing rustup 1.29.2"
description: "The rustup team is happy to announce the release of rustup version 1.29.2. Rustup is the recommended tool to install Rust , a programming language that empowers everyone to build reliable and efficient software."
pubDate: 2026-10-20T00:00:00+00:00
addedAt: 2026-10-21T15:18:36.724441+00:00
source: "Rust Blog"
category: languages
sourceUrl: "https://blog.rust-lang.org/2026/10/20/Rustup-1.29.2/"
tags: ["rust", "cve"]
heat: 57
score: 0.97783
readMinutes: 1
image: "https://www.rust-lang.org/static/images/rust-social.jpg"
---

The rustup team is happy to announce the release of rustup version 1.29.2. Rustup is the recommended tool to install Rust , a programming language that empowers everyone to build reliable and efficient software. What's new in rustup 1.29.2 This is a small release which only updates the rustls-webpki and webpki-root-certs dependencies to address the problematic eMudhra intermediate certificates issue described in CVE-2026-111943 . See also RUSTSEC-2026-0382 . Further details are available in the changelog ! How to update If you have a previous version of rustup installed, getting the new one is as easy as stopping any programs which may be using rustup (e.g. closing your IDE) and running: $ rustup self update Rustup will also automatically update itself at the end of a normal toolchain update: $ rustup update If you don't have it already, you can get rustup from the appropriate page on ou

*Reproduced from the Rust Blog feed. No model was used to write this entry — follow the link for the full article.*
