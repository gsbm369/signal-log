---
title: "How a shared merchant data service can degrade gracefully"
description: "Introduction When a cache becomes unreliable, a shared read service can struggle in ways that spread to the systems that depend on it. We saw this pattern in our merchant data service (MDS)."
pubDate: 2026-11-18T00:00:00+00:00
addedAt: 2026-11-24T09:48:05.484255+00:00
source: "Grab Engineering"
category: company_eng
sourceUrl: "https://engineering.grab.com/shared-merchant-data-service"
tags: ["tech"]
heat: 56
score: 0.61891
readMinutes: 1
image: "https://engineering.grab.com/img/degrade-merchant-data/figure-1.png"
imageAlt: "Diagram of the cache-aside read path for the merchant data service"
hnPoints: 0
hnComments: 0
buzz: 0
---

Introduction When a cache becomes unreliable, a shared read service can struggle in ways that spread to the systems that depend on it. We saw this pattern in our merchant data service (MDS). Cache reads began timing out, fallback requests increased database pressure, and service availability degraded. The trigger was localized; the broader impact came from how each layer responded, passing more work downstream instead of containing the failure. That amplification follows a predictable pattern, and a few design changes help MDS degrade instead of collapse. The central lesson is simple: a fallback is not a safety net unless its work is bounded. The merchant data service and its cache MDS is a shared read service for merchant information. Many client applications use it for questions such as “Is this outlet open?”, “Does this merchant accept orders manually?”, and “What are this merchant’s

*Reproduced from the Grab Engineering feed. No model was used to write this entry — follow the link for the full article.*
