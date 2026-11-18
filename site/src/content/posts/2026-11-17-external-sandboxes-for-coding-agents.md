---
title: "External sandboxes for coding agents"
description: "External sandboxes for coding agents I've been exploring new ways to sandbox code that is executed by agents, with a focus on making it safer to try out local models without worrying that a mistake or prompt injection at"
pubDate: 2026-11-17T22:52:29+00:00
addedAt: 2026-11-18T03:48:31.035356+00:00
source: "Simon Willison"
category: ai
sourceUrl: "https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/"
tags: ["linux", "python", "webassembly"]
heat: 81
score: 1.01741
readMinutes: 1
image: "https://static.simonwillison.net/static/2026/sandbox-proxy.png"
imageAlt: "The network policy page with allowed destinations, the policy JSON editor and recent proxy activity"
hnPoints: 0
hnComments: 0
buzz: 0
---

External sandboxes for coding agents I've been exploring new ways to sandbox code that is executed by agents, with a focus on making it safer to try out local models without worrying that a mistake or prompt injection attack might cause them to take damaging actions on a machine. I worked on this project with Prime Radiant , the AI research lab behind Superpowers and other projects . My post on the Prime Radiant blog introduces the external sandbox pattern, where code executed by the agent runs inside a dedicated sandbox while the agent itself lives outside of that sandbox. To demonstrate this pattern we've released three sandbox server implementations: external-sandbox-v86 runs a Node.js server which then uses v86 to run Alpine Linux inside WebAssembly. external-sandbox-container is a Python web server which runs the sandbox in Alpine Linux inside an Apple Containers instance. external-

*Reproduced from the Simon Willison feed. No model was used to write this entry — follow the link for the full article.*
