---
title: "Decoding base64 email attachments: a speed ranking of programming languages"
description: "Email attachments are base64. So are cryptographic PEM certificates."
pubDate: 2026-11-20T12:37:52+00:00
addedAt: 2026-11-20T15:48:35.103977+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/11/20/decoding-base64-email-attachments/"
tags: ["tech"]
heat: 74
score: 0.98699
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/11/mimespeed-cover-150x150.jpg"
imageAlt: "Decoding base64 email attachments: a speed ranking of programming languages"
hnPoints: 1
hnComments: 0
buzz: 11
---

Email attachments are base64. So are cryptographic PEM certificates. In both cases the text is broken into lines, 76 characters for email and 64 for PEM. Skipping line endings sounds trivial. Yet many fast decoders only work on uninterrupted base64. As soon as they meet a line break, they fall back to a slow path. Continue reading Decoding base64 email attachments: a speed ranking of programming languages

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
