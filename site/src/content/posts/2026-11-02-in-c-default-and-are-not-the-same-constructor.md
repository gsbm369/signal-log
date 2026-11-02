---
title: "In C++, = default and {} are not the same constructor"
description: "You can write an empty default constructor as span() = default or as span() {}. It can have remarkable effects on performance."
pubDate: 2026-11-02T12:48:59+00:00
addedAt: 2026-11-02T16:18:31.628403+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/11/02/default-and-braces-are-not-the-same-constructor/"
tags: ["tech"]
heat: 69
score: 0.9857
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/11/cppinit-cover-150x150.jpg"
hnPoints: 2
hnComments: 0
buzz: 18
---

You can write an empty default constructor as span() = default or as span() {}. It can have remarkable effects on performance. struct span { const char *p; int len; const char *end; span() = default; // or span() {} span(const char *s, int n) : p(s), len(n), end(s + n) {} }; The constructor Continue reading In C++, = default and {} are not the same constructor

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
