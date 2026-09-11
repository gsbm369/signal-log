---
title: "What Now? Handling Errors in Large Systems"
description: "What Now? Handling Errors in Large Systems More options means more choices."
pubDate: 2025-11-20T00:00:00+00:00
addedAt: 2026-09-11T10:20:27.668024+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/11/20/what-now.html"
tags: ["cloudflare", "rust"]
heat: 73
score: 0.35022
readMinutes: 1
---

What Now? Handling Errors in Large Systems More options means more choices. Cloudflare’s deep postmortem for their November 18 outage triggered a ton of online chatter about error handling, caused by a single line in the postmortem: .unwrap () If you’re not familiar with Rust, you need to know about Result , a kind of struct that can contain either a successful result, or an error. unwrap says basically “return the successful results if there is one, otherwise crash the program” 1 . You can think of it like an assert . There’s a ton of debate about whether assert s are good in production 2 , but most are missing the point. Quite simply, this isn’t a question about a single program. It’s not a local property. Whether assert s are appropriate for a given component is a global property of the system, and the way it handles data. Let’s play a little error handling game. Click the ✅ if you th

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
