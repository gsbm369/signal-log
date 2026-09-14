---
title: "Emacs arbitrary code execution flaw"
description: "Sean Whitton has announced that the original fix for an arbitrary code execution flaw in Emacs ( CVE-2024-53920 ) was incomplete. Bas Alberts discovered that viewing or editing untrusted files in modes other than Emacs's"
pubDate: 2026-09-14T15:20:00+00:00
addedAt: 2026-09-14T18:36:46.488893+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1094224/"
tags: ["cve", "vulnerab"]
heat: 78
score: 1.05857
readMinutes: 1
---

Sean Whitton has announced that the original fix for an arbitrary code execution flaw in Emacs ( CVE-2024-53920 ) was incomplete. Bas Alberts discovered that viewing or editing untrusted files in modes other than Emacs's Lisp mode can also result in arbitrary code execution. This problem affects all Emacs versions affected by CVE-2024-53920. This means Emacs 24 and newer, and possibly also older versions. A minimal fix, attached, is queued up for release with Emacs 31.2. We (the Emacs upstream maintainers) don't expect to backport the fix to older Emacs releases ourselves. LWN covered the original vulnerability in December 2024.

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
