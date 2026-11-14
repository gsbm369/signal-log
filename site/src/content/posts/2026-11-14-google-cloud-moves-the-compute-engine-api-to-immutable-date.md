---
title: "Google Cloud Moves the Compute Engine API to Immutable Date-Based Versions"
description: "Google Cloud has made date-based versioning of the Compute Engine API generally available, replacing the single mutable /v1 surface with immutable quarterly snapshots such as 2026-09-01, selected per request with a heade"
pubDate: 2026-11-14T07:27:00+00:00
addedAt: 2026-11-14T13:16:15.748402+00:00
source: "InfoQ"
category: system_design
sourceUrl: "https://www.infoq.com/news/2026/11/compute-engine-api-versioning/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global"
tags: ["azure"]
heat: 81
score: 0.95432
readMinutes: 1
image: "https://res.infoq.com/news/2026/11/compute-engine-api-versioning/en/headerimage/generatedHeaderImage-1794296072866.jpg"
hnPoints: 0
hnComments: 0
buzz: 0
---

Google Cloud has made date-based versioning of the Compute Engine API generally available, replacing the single mutable /v1 surface with immutable quarterly snapshots such as 2026-09-01, selected per request with a header or query parameter. New versions can change defaults, error formats, and IAM checks without touching /v1 callers, a model Azure Resource Manager and Stripe have used for years. By Steef-Jan Wiggers

*Reproduced from the InfoQ feed. No model was used to write this entry — follow the link for the full article.*
