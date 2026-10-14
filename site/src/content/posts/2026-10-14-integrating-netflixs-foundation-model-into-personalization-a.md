---
title: "Integrating Netflix’s Foundation Model into Personalization applications"
description: "Authors: Divya Gadde , Ko-Jen Hsiao , Dhaval Patel and Moumita Bhattacharya The motivation for building the Netflix Foundation Model for personalization was laid out in this previous blog post. The Netflix homepage is po"
pubDate: 2026-10-14T20:02:22+00:00
addedAt: 2026-10-14T21:18:05.708566+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb?source=rss----2615bd06b42e---4"
tags: ["inference", "transformer"]
heat: 69
score: 1.03231
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/960/1*9xBaz1zkvALNwB3iT3xK8g.png"
---

Authors: Divya Gadde , Ko-Jen Hsiao , Dhaval Patel and Moumita Bhattacharya The motivation for building the Netflix Foundation Model for personalization was laid out in this previous blog post. The Netflix homepage is powered by several specialized models and it requires significant time and resources to maintain and continue innovating on these individual models. Therefore, we decided to centralize member preference learning and have one powerful model learned from comprehensive user interaction histories and content data at a large scale and have this model distribute its learnings to other models. The previous two blog posts( 1 , 2 ) focus on the development of the Foundation Model and here we talk about how we integrate the Foundation Model into various applications. We found that there is extensive literature focused on the training and inference of large-scale transformer-based mod

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
