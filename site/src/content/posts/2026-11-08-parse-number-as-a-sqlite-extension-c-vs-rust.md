---
title: "parse_number() as a SQLite extension: C vs Rust"
description: "Research: parse_number() as a SQLite extension: C vs Rust I was out walking the dog when I got curious about how easy/difficult it would be to write a SQLite C extension that adds a parse_number() function for turning st"
pubDate: 2026-11-08T22:26:00+00:00
addedAt: 2026-11-09T03:48:28.810718+00:00
source: "Simon Willison"
category: ai
sourceUrl: "https://simonwillison.net/2026/Nov/8/sqlite-parse-number-c-vs-rust/"
tags: ["sqlite", "rust", "claude"]
heat: 100
score: 1.89
readMinutes: 1
hnPoints: 2
hnComments: 0
buzz: 18
---

Research: parse_number() as a SQLite extension: C vs Rust I was out walking the dog when I got curious about how easy/difficult it would be to write a SQLite C extension that adds a parse_number() function for turning strings like -$1,234.56 or '12.5%' into numeric values that could be summed and sorted. I fired up regular Claude chat (Opus 5.5) and prompted : I'm thinking about a SQLite custom function 'parse_number(value)' that strips ',', '$', '£' and '%', handles a leading '-', and returns 'NULL' for anything it can’t parse Explore the difference between building this as a SQLite extension in C v.s. in Rust - I want to compare performance and code complexity and size of the resulting .so (or whatever) file This gave me a solid starting point - the Rust extension was 321 KB (using Rusqlite ) and 298 KB (using sqlite-loadable-rs ), while the C extension was 14 KB. But the Rust extensio

*Reproduced from the Simon Willison feed. No model was used to write this entry — follow the link for the full article.*
