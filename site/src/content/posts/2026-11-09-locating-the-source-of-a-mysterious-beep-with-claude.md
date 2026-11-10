---
title: "Locating the source of a mysterious beep with Claude"
description: "Our house has a box room, full of boxes that we still haven't unpacked from our last move. A couple of weeks ago something in that room started intermittently beeping ."
pubDate: 2026-11-09T23:57:21+00:00
addedAt: 2026-11-10T03:48:36.235869+00:00
source: "Simon Willison"
category: ai
sourceUrl: "https://simonwillison.net/2026/Nov/9/mysterious-beeps/"
tags: ["claude", "python"]
heat: 100
score: 1.4827
readMinutes: 1
image: "https://static.simonwillison.net/static/2026/beep-locator-ui.webp"
imageAlt: "Screenshot of a web app that uses several phones, tablets and laptops as microphones to locate a mystery beeping sound in a room. The left column has an &quot;Add a listener&quot; panel with a QR code and join link, a &quot;Controls&quot; panel with buttons including &quot;Calibrate&quot;, &quot;Test beep&quot; and &quot;It just beeped!&quot; plus a &quot;Listen for beeps&quot; checkbox, and a &quot;Mystery beep&quot; note reading &quot;3345 Hz · 3 confirmed · remembered across sessions&quot;. Below that, a &quot;Devices&quot; list shows five color-coded listeners (Simon iPhone, New iPad, Old iPad, MacBook Pro, Surface Ultra), each marked &quot;✓ mic working · ✓ speaker working&quot;. The main area is a gridded map with a 1 m scale bar that shows the five devices as colored dots and earlier sounds as small timestamped markers. A pink shaded circle near the MacBook Pro is labeled &quot;mystery beep · 2 hearings · within ~41 cm&quot;, and beside it a dashed plus marker suggests &quot;add a listener here? could tighten the mystery beep"
hnPoints: 40
hnComments: 21
buzz: 60
---

Our house has a box room, full of boxes that we still haven't unpacked from our last move. A couple of weeks ago something in that room started intermittently beeping . The beeps were far enough apart that standing in the room and trying to determine the source of the noise was frustrating, and I really didn't want to dig through every one of those boxes. So I had Claude Code build Beep Locator , a software system for triangulating the source of a mysterious beep using multiple devices scattered around the room. Here's what Beep Locator looks like after it has been running for a while: You run Python web server to show the primary UI, and then use the QR code or URL to connect as many devices as you can spare to act as listeners - I was using two iPads, a phone, a MacBook Pro and a Surface Ultra. The devices then play noises to each other to help estimate their locations. This didn't wor

*Reproduced from the Simon Willison feed. No model was used to write this entry — follow the link for the full article.*
