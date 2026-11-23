---
title: "Ladybird's first alpha release"
description: "Ladybird is an astonishingly ambitious project: a new browser, in 2026, with its own implementation of most of the key components - HTML parsing, CSS engine, layout, JavaScript, even WebAssembly. It still uses a few exte"
pubDate: 2026-11-23T21:46:35+00:00
addedAt: 2026-11-23T21:48:09.750148+00:00
source: "Simon Willison"
category: ai
sourceUrl: "https://simonwillison.net/2026/Nov/23/ladybird/"
tags: ["linux", "sqlite", "webassembly"]
heat: 72
score: 1.09213
readMinutes: 1
image: "https://static.simonwillison.net/static/2026/ladybird-ffmpeg.webp"
imageAlt: "macOS running Ladybird - it has four tabs open, the visible one is showing tools.simonwillison.net/video-compressor which is an app for running ffmpeg using WebAssembly and is shown working."
hnPoints: 0
hnComments: 0
buzz: 0
---

Ladybird is an astonishingly ambitious project: a new browser, in 2026, with its own implementation of most of the key components - HTML parsing, CSS engine, layout, JavaScript, even WebAssembly. It still uses a few external components - things like HarfBuzz for text shaping, Skia for 2D graphics, ffmpeg for video, and SQLite for the things you do with SQLite. Everything else is part of Ladybird, or code brought in from Ladybird's even more ambitious predecessor project SerenityOS . This morning the Ladybird project released their first alpha , which means you can now install the browser (on macOS or Linux) without having to compile it yourself! I've been trying it out today, and it's very impressive. It feels fast, the UI is lightweight and intuitive, and most of the websites I've tried to load in it have worked as they should. It looks like this (showing my video-compressor tool): Here

*Reproduced from the Simon Willison feed. No model was used to write this entry — follow the link for the full article.*
