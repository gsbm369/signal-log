---
title: "You can run git on object storage if you re-make packfiles"
description: "It sure seems that a bunch of companies are trying to ship a git product of some kind as of late. Wonder why that is."
pubDate: 2026-09-15T00:00:00+00:00
addedAt: 2026-09-19T17:01:05.808834+00:00
source: "Xe Iaso"
category: deep_dives
sourceUrl: "https://www.tigrisdata.com/blog/objgit-packfiles/"
tags: ["tech"]
heat: 81
score: 0.53322
readMinutes: 1
image: "https://xeiaso.net/static/img/objgit-delta-brain.webp"
imageAlt: "Expanding brain meme. Small brain: git stores diffs against an empty folder. Bigger brain: git stores the entire files for every version. Galaxy brain: git stores diffs against an empty folder."
---

It sure seems that a bunch of companies are trying to ship a git product of some kind as of late. Wonder why that is. Either way, I’m building a Git server backed by object storage as an open-source project . It sounded simple enough to start: Git looks like a filesystem, so let’s use a filesystem as a translation layer on top of object storage to make Git speak object storage. This model worked… ok, I guess? But it didn’t work for real-world size repositories, so I needed a different approach. Git stores everything in Objects , so why not store those as objects in Tigris? Turns out Git packfiles and how they intersected with my (admittedly somewhat terrible) filesystem shim were the main reason why it was slow. I ended up having to invent my own packfile format with a columnar store that’s object storage native. This is the fruit of all of my performance analysis, metrics annotations, a

*Reproduced from the Xe Iaso feed. No model was used to write this entry — follow the link for the full article.*
