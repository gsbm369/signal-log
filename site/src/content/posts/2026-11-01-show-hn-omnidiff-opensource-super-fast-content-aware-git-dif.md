---
title: "Show HN: OmniDiff – Opensource, super fast, content aware Git difftool, in Rust"
description: "I have been researching what the ultimate diff tool would look like, based on actual diffs in open source repositories. OmniDiff can diff: code (25 languages), config, images, PDFs, archives, cursors, fonts..."
pubDate: 2026-11-01T13:02:30+00:00
addedAt: 2026-11-02T10:18:32.631725+00:00
source: "Hacker News Best"
category: aggregators
sourceUrl: "https://github.com/ivankovic/omnidiff"
tags: ["rust"]
heat: 68
score: 0.50924
readMinutes: 1
image: "https://repository-images.githubusercontent.com/1078209382/05657b56-1763-4014-bae7-bb30db0db322"
imageAlt: "Fast, robust, accurate diffing . Contribute to ivankovic/omnidiff development by creating an account on GitHub."
hnPoints: 244
hnComments: 70
buzz: 88
---

I have been researching what the ultimate diff tool would look like, based on actual diffs in open source repositories. OmniDiff can diff: code (25 languages), config, images, PDFs, archives, cursors, fonts... It's fast. It can diff C++ files of tens of thousands of lines in under 100ms, on a 2023 ThinkPad T14s. It's open source. AGPLv3. It's based on real diffs. I looked at the 7400 repositories that are listed in Gentoo packages, sampled 2000 diffs and solved them manually to get a good understanding of what is needed, before putting together the diff pipelines for each content type. Incidentally, this also forms the basis of the CI pipeline, so the robustness of the codebase is quite high. I'm still developing it. It's v0.3.0 at this time. But I have been using it daily as my git difftool for months now, and it works well. AI Disclosure: Yes, I do use AI. No, I do not vibecode. Commen

*Reproduced from the Hacker News Best feed. No model was used to write this entry — follow the link for the full article.*
