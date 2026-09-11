---
title: "Learning a few things about running SQLite"
description: "Hello! I ve been working on a Django site recently, and I decided to use SQLite as the database."
pubDate: 2026-07-17T00:00:00+00:00
addedAt: 2026-09-11T04:05:08.563445+00:00
source: "jvns.ca"
category: deep_dives
sourceUrl: "https://jvns.ca/blog/2026/07/17/learning-about-running-sqlite/"
tags: ["sqlite"]
heat: 85
score: 1.32906
readMinutes: 1
---

Hello! I ve been working on a Django site recently, and I decided to use SQLite as the database. When I was getting started with using SQLite as database for a website I read a bunch of blog posts about how it is totally fine to use SQLite in production for a small site and I think it is totally fine, but what I did not fully appreciate is that SQLite is still a database, databases are complicated, and I do not know a lot about operating databases. So here are a couple of small things I ve been learning about running SQLite. This is the 4th website I ve used SQLite for, and I think this one is harder because with the power of the Django ORM I ve been making the database do more work than I was previously without Django. I started by turning on WAL mode like all the blog posts said to do and hoping for the best. ANALYZE is apparently important Today I was running a query (using SQLite s F

*Reproduced from the jvns.ca feed. No model was used to write this entry — follow the link for the full article.*
