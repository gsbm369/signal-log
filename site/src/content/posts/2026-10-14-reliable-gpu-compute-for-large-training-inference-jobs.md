---
title: "Reliable GPU compute for large training & inference jobs"
description: "Authors: Nick Rutigliano , Argha C , Samartha Chandrashekar How we detect failing GPUs and network fabric, remediate machines automatically, and let long-running jobs survive hardware loss. Open Netflix, and the home scr"
pubDate: 2026-10-14T19:47:42+00:00
addedAt: 2026-10-14T21:18:05.708378+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/reliable-gpu-compute-for-large-training-inference-jobs-d62b03a96d7a?source=rss----2615bd06b42e---4"
tags: ["inference", "gpu"]
heat: 100
score: 1.929
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*d15z8m06XjWnYeauK7iXfQ.png"
---

Authors: Nick Rutigliano , Argha C , Samartha Chandrashekar How we detect failing GPUs and network fabric, remediate machines automatically, and let long-running jobs survive hardware loss. Open Netflix, and the home screen is assembled for you: which rows appear, the order they appear in, the titles within them, and the artwork for each title are chosen by machine learning models trained on how hundreds of millions of members watch. Personalization is one of the most widely used things we build, and members feel it every time they open the app. Like a growing share of Netflix, it runs on GPUs, which train those models and increasingly serve them live. Those GPUs have to stay healthy for that experience to hold up, and keeping them healthy is harder than it sounds. A single large training job can run for weeks across hundreds of GPUs spread over many machines. It runs as a gang: the rank

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
