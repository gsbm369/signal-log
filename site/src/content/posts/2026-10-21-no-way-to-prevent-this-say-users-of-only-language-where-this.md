---
title: "\"No way to prevent this\" say users of only language where this regularly happens"
description: "In the hours following the release of CVE-2026-111813 for Apache Traffic Server , site reliability workers and systems administrators scrambled to patch systems running its experimental magick plugin. In its default unsi"
pubDate: 2026-10-21T00:00:00+00:00
addedAt: 2026-10-22T09:18:32.490994+00:00
source: "Xe Iaso"
category: deep_dives
sourceUrl: "https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-111813/"
tags: ["cve"]
heat: 74
score: 0.85199
readMinutes: 1
image: "https://files.xeiaso.net/hero/sad-business-man.jpg"
---

In the hours following the release of CVE-2026-111813 for Apache Traffic Server , site reliability workers and systems administrators scrambled to patch systems running its experimental magick plugin. In its default unsigned configuration, the plugin lets unauthenticated clients control arguments passed to ImageMagick convert, allowing anyone to execute whatever command they want on the server. The affected plugin is written in C++, whose users were relieved that this time the attacker did not even have to corrupt memory to tell the server what to do. This was a terrible tragedy, but sometimes these things just happen and there's nothing anyone can do to stop them, said programmer Mr. Friedrich Frami, whose image processing plugin accepted instructions from anyone who could construct a URL. It's a shame, but what can we do? There really isn't any way to know whether a stranger on the int

*Reproduced from the Xe Iaso feed. No model was used to write this entry — follow the link for the full article.*
