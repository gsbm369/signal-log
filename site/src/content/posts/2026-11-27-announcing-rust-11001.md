---
title: "Announcing Rust 1.100.1"
description: "The Rust team has published a new point release of Rust, 1.100.1. Rust is a programming language that is empowering everyone to build reliable and efficient software."
pubDate: 2026-11-27T00:00:00+00:00
addedAt: 2026-11-28T10:38:23.475162+00:00
source: "Rust Blog"
category: languages
sourceUrl: "https://blog.rust-lang.org/2026/11/27/Rust-1.100.1/"
tags: ["rust"]
heat: 86
score: 1.43027
readMinutes: 1
image: "https://www.rust-lang.org/static/images/rust-social.jpg"
hnPoints: 3
hnComments: 1
buzz: 22
---

The Rust team has published a new point release of Rust, 1.100.1. Rust is a programming language that is empowering everyone to build reliable and efficient software. If you have a previous version of Rust installed via rustup, getting Rust 1.100.1 is as easy as: $ rustup update stable If you don't have it already, you can get rustup from the appropriate page on our website. If you'd like to help us out by testing future releases, you might consider updating locally to use the beta channel ( rustup default beta ) or the nightly channel ( rustup default nightly ). Please report any bugs you might come across! What's in 1.100.1 Rust 1.100.1 fixes a regression where some types were not inferred as having Iterator impls . We reverted a change to the unstable const version of Iterator in Rust 1.100.0, which cannot actually be used by stable code, but accidentally prevented some types with val

*Reproduced from the Rust Blog feed. No model was used to write this entry — follow the link for the full article.*
