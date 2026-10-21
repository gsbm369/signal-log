---
title: "PHP patches released for two critical RCEs"
description: "The PHP project has published PHP versions 8.5.12 , 8.4.27 , 8.3.36 and 8.2.35 to address two critical vulnerabilities that could allow unauthenticated remote code execution. Who is at risk: all PHP installations serving"
pubDate: 2026-10-21T13:53:18+00:00
addedAt: 2026-10-21T15:18:36.723689+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1102014/"
tags: ["cve", "vulnerab", "exploit", "rce"]
heat: 60
score: 1.07768
readMinutes: 1
---

The PHP project has published PHP versions 8.5.12 , 8.4.27 , 8.3.36 and 8.2.35 to address two critical vulnerabilities that could allow unauthenticated remote code execution. Who is at risk: all PHP installations serving web requests, including PHP-FPM, Apache with mod_php, php-cgi, FrankenPHP and LiteSpeed. We consider the risk highest for mod_php, with a demonstrated exploit where an unauthenticated request can trigger the attack before any application code runs. The vulnerabilities: RCE via OOM corruption , CVE-2026-109618 ( GHSA-w8hw-w9fx-j79w ): out-of-memory handling can interrupt PHP while internal request data is only partially initialized. Request cleanup may then treat the invalid data as valid. RCE via stale global state , CVE-2026-109619 ( GHSA-6wmf-4rv5-p3rp ): request-owned internal state can survive after its backing memory has been freed. A later request handled by the sa

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
