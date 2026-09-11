---
title: "Using `make` to compile C programs (for non-C-programmers)"
description: "I have never been a C programmer but every so often I need to compile a C/C++ program from source. This has been kind of a struggle for me: for a long time, my approach was basically install the dependencies, run make , "
pubDate: 2025-06-10T00:00:00+00:00
addedAt: 2026-09-11T10:20:27.667073+00:00
source: "jvns.ca"
category: deep_dives
sourceUrl: "https://jvns.ca/blog/2025/06/10/how-to-compile-a-c-program/"
tags: ["linux", "sqlite"]
heat: 52
score: 0.1968
readMinutes: 1
---

I have never been a C programmer but every so often I need to compile a C/C++ program from source. This has been kind of a struggle for me: for a long time, my approach was basically install the dependencies, run make , if it doesn t work, either try to find a binary someone has compiled or give up . Hope someone else has compiled it worked pretty well when I was running Linux but since I ve been using a Mac for the last couple of years I ve been running into more situations where I have to actually compile programs myself. So let s talk about what you might have to do to compile a C program! I ll use a couple of examples of specific C programs I ve compiled and talk about a few things that can go wrong. Here are three programs we ll be talking about compiling: paperjam sqlite qf (a pager you can run to quickly open files from a search with rg -n THING | qf ) step 1: install a C compiler

*Reproduced from the jvns.ca feed. No model was used to write this entry — follow the link for the full article.*
