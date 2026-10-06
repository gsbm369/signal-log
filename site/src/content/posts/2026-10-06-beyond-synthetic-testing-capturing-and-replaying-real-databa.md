---
title: "Beyond synthetic testing: Capturing and replaying real database workloads at Airbnb"
description: "How we capture real production database traffic at Airbnb and replay it offline to load-test, plan capacity, and de-risk upgrades. By: Zuofei Wang , Erluo Li Introduction At Airbnb, MySQL-compatible databases are a criti"
pubDate: 2026-10-06T17:01:04+00:00
addedAt: 2026-10-06T18:24:02.115253+00:00
source: "Airbnb Engineering"
category: company_eng
sourceUrl: "https://medium.com/airbnb-engineering/beyond-synthetic-testing-capturing-and-replaying-real-database-workloads-at-airbnb-cea7ee9b1ab2?source=rss----53c7c27702d5---4"
tags: ["tech"]
heat: 68
score: 0.9473
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*iYpaqy9OLoB92atnd-0cEA.png"
imageAlt: "Three hikers wearing backpacks walk away from the camera along a coastal trail through low green shrubs, heading toward large smooth granite boulders on a rocky beach, with the ocean and distant mountains visible under a cloudy sky."
---

How we capture real production database traffic at Airbnb and replay it offline to load-test, plan capacity, and de-risk upgrades. By: Zuofei Wang , Erluo Li Introduction At Airbnb, MySQL-compatible databases are a critical backbone of our online database infrastructure: a fleet of hundreds of clusters supporting thousands of use cases at millions of queries per second (QPS). Operating databases at scale brings hard problems, including sizing clusters for future growth, keeping behavior consistent across version upgrades and migrations, and reproducing production incidents well enough to debug them. This post describes the database traffic capture and replay system we built to help us tackle them. Challenges and motivation A complex database operation such as Airbnb’s requires a number of supporting systems, and one of them is a way to capture database queries and replay them. This is ne

*Reproduced from the Airbnb Engineering feed. No model was used to write this entry — follow the link for the full article.*
