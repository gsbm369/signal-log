---
title: "Pass@k is Mostly Bunk"
description: "Pass@k is Mostly Bunk Exponentially better results? I'll take three!"
pubDate: 2026-01-21T00:00:00+00:00
addedAt: 2026-09-11T10:17:29.289396+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/01/21/pass-k.html"
tags: ["tech"]
heat: 76
score: 0.38667
readMinutes: 1
image: "https://brooker.co.za/blog/images/d6_trimmed.jpg"
---

Pass@k is Mostly Bunk Exponentially better results? I'll take three! Measuring the success of AI agents isn’t easy. It’s very sensitive to what success means, it can require a lot of samples, its highly context sensitive. Generally hard. So it doesn’t help that one of the most common metrics used for agents is (mostly) bunk. I’m talking about pass@k . What is pass@k ? It’s the probability that at least one of k different attempts will succeed. A six-sided die, where pass means rolling a 6, has a pass@3 of 45% and a pass@10 of 83%. A D20 has a pass@25 of 72%, and a pass@100 of 99.4%. 99.4%! What a great evaluation result! Clearly the model is doing something meaningful and useful! No, it’s doing something meaningful and useful 5% of the time. The problem with pass@k is that’s exponentially forgiving. There’s a value of k , a fairly low one generally, that can make anything look good. Here

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
