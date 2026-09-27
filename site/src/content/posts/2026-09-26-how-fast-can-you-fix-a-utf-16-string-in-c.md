---
title: "How fast can you fix a UTF-16 string in C#?"
description: "C# strings are UTF-16. Most characters are one 16-bit code unit."
pubDate: 2026-09-26T16:53:53+00:00
addedAt: 2026-09-27T19:24:43.027993+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/09/26/how-fast-can-you-fix-a-utf-16-string-in-c/"
tags: ["tech"]
heat: 72
score: 0.89638
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/09/utf16-cover-150x150.jpg"
imageAlt: "How fast can you fix a UTF-16 string in C#"
---

C# strings are UTF-16. Most characters are one 16-bit code unit. Characters outside the basic multilingual plane, emoji included, take two: a high surrogate (U+D800 to U+DBFF) followed by a low surrogate (U+DC00 to U+DFFF). A surrogate with the wrong neighbor, or with none, is ill-formed. You should never send an ill-formed string to disk Continue reading How fast can you fix a UTF-16 string in C#?

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
