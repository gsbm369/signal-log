---
title: "Agent Safety is a Box"
description: "Agent Safety is a Box Keep a lid on it. Before we start, let’s cover some terms so we’re thinking about the same thing."
pubDate: 2026-01-12T00:00:00+00:00
addedAt: 2026-09-11T10:20:27.667975+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2026/01/12/agent-box.html"
tags: ["tech"]
heat: 76
score: 0.3735
readMinutes: 1
image: "https://brooker.co.za/blog/images/agent_loop.png"
---

Agent Safety is a Box Keep a lid on it. Before we start, let’s cover some terms so we’re thinking about the same thing. This is a post about AI agents, which I’ll define (riffing off Simon Willison 1 ) as: An AI agent runs models and tools in a loop to achieve a goal. Here, goals can include coding, customer service, proving theorems, cloud operations , or many other things. These agents can be interactive or one-shot; called by humans, other agents, or traditional computer systems; local or cloud; and short-lived or long-running. What they don’t tend to be is pure . They typically achieve their goals by side effects. Side effects including modifying the local filesystem, calling another agent, calling a cloud service, making a payment, or starting a 3D print. The topic of today’s post is those side-effects. Simply, what agents can do . We should also be concerned with what agents can sa

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
