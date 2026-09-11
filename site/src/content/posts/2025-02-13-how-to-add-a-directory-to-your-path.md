---
title: "How to add a directory to your PATH"
description: "I was talking to a friend about how to add a directory to your PATH today. It s something that feels obvious to me since I ve been using the terminal for a long time, but when I searched for instructions for how to do it"
pubDate: 2025-02-13T12:27:56+00:00
addedAt: 2026-09-11T10:52:16.178064+00:00
source: "jvns.ca"
category: deep_dives
sourceUrl: "https://jvns.ca/blog/2025/02/13/how-to-add-a-directory-to-your-path/"
tags: ["tech"]
heat: 27
score: 0.10927
readMinutes: 1
---

I was talking to a friend about how to add a directory to your PATH today. It s something that feels obvious to me since I ve been using the terminal for a long time, but when I searched for instructions for how to do it, I actually couldn t find something that explained all of the steps a lot of them just said add this to ~/.bashrc , but what if you re not using bash? What if your bash config is actually in a different file? And how are you supposed to figure out which directory to add anyway? So I wanted to try to write down some more complete directions and mention some of the gotchas I ve run into over the years. Here s a table of contents: step 1: what shell are you using? step 2: find your shell s config file a note on bash s config file step 3: figure out which directory to add step 3.1: double check it s the right directory step 4: edit your shell config step 5: restart your shel

*Reproduced from the jvns.ca feed. No model was used to write this entry — follow the link for the full article.*
