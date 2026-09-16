---
title: "Show HN: Capsule – Single-file web apps that save their data into SQLite"
description: "Hey HN, I always had the problem that building HTML pages is really simple now, but trying to save data required hosting it somewhere, and sharing it afterwards was not easy. Over the last few months, I've been building "
pubDate: 2026-09-15T13:31:40+00:00
addedAt: 2026-09-16T00:35:31.226857+00:00
source: "Hacker News Best"
category: aggregators
sourceUrl: "https://withcapsule.app/"
tags: ["sqlite", "rust"]
heat: 65
score: 0.75435
readMinutes: 1
image: "https://withcapsule.app/og-image.png"
---

Hey HN, I always had the problem that building HTML pages is really simple now, but trying to save data required hosting it somewhere, and sharing it afterwards was not easy. Over the last few months, I've been building an app called Capsule (it’s also the file extension name) written in Rust with Tauri 2.0 that allows packing an HTML app and its data into a single SQLite file. The HTML file and any related assets are directly embedded in the database. User data can either be saved as a localStorage key/value store or via a MongoDB-inspired collections API as documents, saved in a table in the file. You can also save other assets, like PDF files or images, directly in the database to keep different documents together. All data can be easily exported to CSV or JSON if needed. Privacy and security were a big priority for me, so documents cannot do anything out of the box. They don’t have d

*Reproduced from the Hacker News Best feed. No model was used to write this entry — follow the link for the full article.*
