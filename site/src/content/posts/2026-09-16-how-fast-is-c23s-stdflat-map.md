---
title: "How fast is C++23’s std::flat_map?"
description: "C++23 added a new type to the standard library: std::flat_map. There is also a std::flat_set and other variants, but let me focus on std::flat_map."
pubDate: 2026-09-16T20:26:36+00:00
addedAt: 2026-09-19T16:58:10.138025+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/09/16/how-fast-is-c23s-stdflat_map/"
tags: ["tech"]
heat: 66
score: 0.75373
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/09/Capture-decran-le-2026-09-16-a-16.20.19-e1789590380973-150x150.png"
---

C++23 added a new type to the standard library: std::flat_map. There is also a std::flat_set and other variants, but let me focus on std::flat_map. A flat map is a sorted vector of keys next to a vector of values. A query is a binary search over the sorted keys. You need a recent standard library: Continue reading How fast is C++23 s std::flat_map?

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
