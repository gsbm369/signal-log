---
title: "Java4Shell: when base64 decoding leads to remote code execution?"
description: "Let us start with an example that triggers the issue. byte[] src = (\"A\".repeat(128) + \"=\").getBytes(StandardCharsets.US_ASCII); Base64.getDecoder().decode(src); One hundred and twenty-eight letters A and one =."
pubDate: 2026-11-18T19:43:03+00:00
addedAt: 2026-11-19T22:43:39.042536+00:00
source: "Daniel Lemire"
category: deep_dives
sourceUrl: "https://lemire.me/blog/2026/11/18/java4shell-when-base64-decoding-leads-to-remote-code-execution/"
tags: ["cve"]
heat: 68
score: 1.02875
readMinutes: 1
image: "https://lemire.me/blog/wp-content/uploads/2026/11/java4shell-cover-150x150.jpg"
imageAlt: "Java4Shell: when base64 decoding leads to remote code execution"
hnPoints: 2
hnComments: 0
buzz: 18
---

Let us start with an example that triggers the issue. byte[] src = ("A".repeat(128) + "=").getBytes(StandardCharsets.US_ASCII); Base64.getDecoder().decode(src); One hundred and twenty-eight letters A and one =. The string is not valid base64, and a correct decoder rejects it. OpenJDK writes past the end of the array anyway. The bug is CVE-2026-114938. It has been in Continue reading Java4Shell: when base64 decoding leads to remote code execution?

*Reproduced from the Daniel Lemire feed. No model was used to write this entry — follow the link for the full article.*
