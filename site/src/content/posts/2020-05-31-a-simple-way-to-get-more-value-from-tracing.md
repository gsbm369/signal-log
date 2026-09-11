---
title: "A simple way to get more value from tracing"
description: "A lot of people seem to think that distributed tracing isn't useful, or at least not without extreme effort that isn't worth it for companies smaller than FB. For example, here are a couple of public conversations that s"
pubDate: 2020-05-31T07:06:34+00:00
addedAt: 2026-09-11T21:25:45.639977+00:00
source: "Dan Luu"
category: deep_dives
sourceUrl: "https://danluu.com/tracing-analytics/"
tags: ["tech"]
heat: 5
score: 0.00014
readMinutes: 1
image: "https://danluu.com/images/tracing-analytics/rpc-tree.webp"
imageAlt: "Diagram of RPC call graph; this will implicitly described in the relevant sections, although the entire SDE section in showing off a visual tool and will probably be unsatisfying if you"
---

A lot of people seem to think that distributed tracing isn't useful, or at least not without extreme effort that isn't worth it for companies smaller than FB. For example, here are a couple of public conversations that sound like a number of private conversations I've had. Sure, there's value somewhere, but it costs too much to unlock . I think this overestimates how much work it is to get a lot of value from tracing. At Twitter, Rebecca Isaacs was able to lay out a vision for how to get value from tracing and executed on it (with help from a number other folks, including Jonathan Simms, Yuri Vishnevsky, Ruben Oanta, Dave Rusek, Hamdi Allam, and many others 1 ) such that the work easily paid for itself. This post is going to describe the tracing infrastructure we've built and describe some use cases where we've found it to be valuable. Before we get to that, let's start with some backgro

*Reproduced from the Dan Luu feed. No model was used to write this entry — follow the link for the full article.*
