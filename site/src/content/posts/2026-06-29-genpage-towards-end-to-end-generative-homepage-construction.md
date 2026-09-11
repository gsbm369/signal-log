---
title: "GenPage: Towards End-to-End Generative Homepage Construction at Netflix"
description: "Authors: Lequn Wang , J iangwei Pan , and Linas Baltrunas Figure 1. Autoregressive homepage generation."
pubDate: 2026-06-29T13:01:02+00:00
addedAt: 2026-09-11T11:03:46.192075+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/genpage-towards-end-to-end-generative-homepage-construction-at-netflix-77146fba8a08?source=rss----2615bd06b42e---4"
tags: ["tech"]
heat: 11
score: 0.02317
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*NurrizMgC7_QbsGuuW42Dg.gif"
---

Authors: Lequn Wang , J iangwei Pan , and Linas Baltrunas Figure 1. Autoregressive homepage generation. GenPage builds a Netflix homepage one row or entity at a time, each one conditioned on what’s already on the page and the user’s context. Introduction The Netflix homepage is the first thing users see when they open the app and the primary way they discover content to enjoy. Almost every part of it is personalized, including which rows appear, which entities show up within those rows, and how everything is arranged on the page. Constructing that homepage is a genuinely hard problem. It is not simply producing one ranked list. The homepage is a structured, two-dimensional layout, made up of recommendation rows and the entities within them. Here, an entity can be a movie, show, game, live event, or other recommendable item. Each choice can affect the value of the others. Traditionally, i

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
