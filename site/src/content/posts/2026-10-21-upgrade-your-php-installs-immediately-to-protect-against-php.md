---
title: "Upgrade your PHP installs immediately to protect against php2shell"
description: "This morning, two critical PHP Security Advisories were published: RCE via OOM corruption (9.2/10) RCE via stale global state (9.2/10) If you're running PHP for any service, you need to upgrade immediately to 8.2.35, 8.3"
pubDate: 2026-10-21T14:10:00+00:00
addedAt: 2026-10-21T15:18:36.723458+00:00
source: "Jeff Geerling"
category: deep_dives
sourceUrl: "https://www.jeffgeerling.com/blog/2026/php-vulnerability-php2shell/"
tags: ["linux", "exploit", "rce"]
heat: 57
score: 0.97291
readMinutes: 1
---

This morning, two critical PHP Security Advisories were published: RCE via OOM corruption (9.2/10) RCE via stale global state (9.2/10) If you're running PHP for any service, you need to upgrade immediately to 8.2.35, 8.3.36, 8.4.27, or 8.5.12. And if you use Remi's repos on RedHat-derivative Linux distros, you need to switch to official repos temporarily as Remi's on vacation and can't update his community repo. (Reminds me of xkcd 2347 ). I'm glad I finished migrating this website from a PHP-based CMS to Hugo earlier this year—having a static website and a minimal commenting system saves on hosting costs and dramatically reduces attack surfaces. Especially in this era of AI tooling making exploit discovery easier.

*Reproduced from the Jeff Geerling feed. No model was used to write this entry — follow the link for the full article.*
