---
title: "CASTLE: training natural language search before the first real query"
description: "How we addressed the cold-start problem for Airbnb’s natural language search by jointly generating synthetic training data — queries and relevance labels — from de-identified booking and search signals. By : Wendy Ran We"
pubDate: 2026-10-13T17:01:02+00:00
addedAt: 2026-10-13T21:18:05.490000+00:00
source: "Airbnb Engineering"
category: company_eng
sourceUrl: "https://medium.com/airbnb-engineering/castle-training-natural-language-search-before-the-first-real-query-3818ef8b4828?source=rss----53c7c27702d5---4"
tags: ["tech"]
heat: 78
score: 0.94164
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*EsZaupfNPaIk04Xh5whb5A.jpeg"
imageAlt: "View across the lake in St. James’s Park, London, framed by golden autumn willow trees, with the ornate towers and domes of Horse Guards building visible in the background and swans and waterfowl swimming on the water with a fountain spraying in the center."
---

How we addressed the cold-start problem for Airbnb’s natural language search by jointly generating synthetic training data — queries and relevance labels — from de-identified booking and search signals. By : Wendy Ran Wei , Hao Li , Weiwei Guo , Xiaowei Liu , Xueyin Chen , Chun How Tan , Malay Haldar , Soumyadip Banerjee , Kedar Bellare , Huiji Gao , Sanjeev Katariya , and Stephanie Moyerman Introduction Natural language search lets guests express intent in their own words, such as “romantic cabin near skiing” or “pet-friendly beach house that sleeps eight,” rather than navigating filters and categories. We needed to introduce this kind of search for Airbnb, and to have it work well from the start. However, this required training the model before we had actual user queries to train the model on, and a reasonable set of relevance labels (inferred from the queries) to map queries to matchi

*Reproduced from the Airbnb Engineering feed. No model was used to write this entry — follow the link for the full article.*
