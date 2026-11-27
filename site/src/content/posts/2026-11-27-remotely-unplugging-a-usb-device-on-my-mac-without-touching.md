---
title: "Remotely unplugging a USB device on my Mac, without touching it"
description: "Tonight I was remote debugging a USB-C device with custom firmware, which was plugged into my Mac Studio at work. I was accessing it over a WireGuard VPN tunnel."
pubDate: 2026-11-27T05:18:00+00:00
addedAt: 2026-11-27T09:38:11.491025+00:00
source: "Jeff Geerling"
category: deep_dives
sourceUrl: "https://www.jeffgeerling.com/blog/2026/remote-control-usb-hub/"
tags: ["tech"]
heat: 63
score: 0.83493
readMinutes: 1
image: "https://www.jeffgeerling.com/blog/2026/remote-control-usb-hub/m4-max-mac-studio-front.jpeg"
imageAlt: "Front of M4 Max Mac Studio"
hnPoints: 4
hnComments: 0
buzz: 26
---

Tonight I was remote debugging a USB-C device with custom firmware, which was plugged into my Mac Studio at work. I was accessing it over a WireGuard VPN tunnel. Part of the debugging process involves flashing firmware to the device using MIDI SysEx messages , and while handy, this technique can also be flaky, leaving the device in a partially-flashed state that needs a physical re-plug to recover from.

*Reproduced from the Jeff Geerling feed. No model was used to write this entry — follow the link for the full article.*
