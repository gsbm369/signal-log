---
title: "If in doubt, delete the uv.lock file"
description: "I've been getting the occasional confusing Python dependency error since switching over to Python 3.15 and the rule I'm having to remember is: If in doubt, delete the uv.lock file Most of my projects are libraries which "
pubDate: 2026-11-01T23:24:22+00:00
addedAt: 2026-11-08T21:48:42.094076+00:00
source: "Simon Willison"
category: ai
sourceUrl: "https://simonwillison.net/2026/Nov/1/delete-uv-lock-first/"
tags: ["python"]
heat: 18
score: 0.09882
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

I've been getting the occasional confusing Python dependency error since switching over to Python 3.15 and the rule I'm having to remember is: If in doubt, delete the uv.lock file Most of my projects are libraries which don't include a uv.lock file, since it's rude for a library dependency to lock versions for anything else that uses it. Running uv run pytest etc tends to leave uv.lock files lying around, which are listed in .gitignore and so do not get committed to my repositories. But... sometimes that uv.lock pins a version of a dependency that doesn't yet have a Python 3.15 wheel. An example from earlier today: error: Failed to build `watchfiles==1.1.1` cause: Call to `maturin.build_wheel` failed error: the configured Python interpreter version (3.15) is newer than PyO3's maximum supported version (3.14) Deleting that file and running uv run pytest again usually fixes the problem. Ta

*Reproduced from the Simon Willison feed. No model was used to write this entry — follow the link for the full article.*
