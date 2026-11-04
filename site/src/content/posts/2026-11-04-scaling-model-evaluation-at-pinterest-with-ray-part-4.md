---
title: "Scaling Model Evaluation at Pinterest with Ray (Part 4)"
description: "Vishnu Arun | Tech Lead, Feature Importance Platform; Anderson Lam | Sr Software Engineer; Andrew Qiu | Machine Learning Engineer I; Helena Xu | Data Scientist I; Tianyou Wang | Data Scientist II Introduction In our mult"
pubDate: 2026-11-04T16:01:04+00:00
addedAt: 2026-11-04T16:18:34.981437+00:00
source: "Pinterest Engineering"
category: company_eng
sourceUrl: "https://medium.com/pinterest-engineering/scaling-model-evaluation-at-pinterest-with-ray-part-4-4a96cd12cc11?source=rss----4c5a5f6279b6---4"
tags: ["inference"]
heat: 84
score: 1.03438
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*IjS1hNUJHyV0NzVGLIiAOA.png"
hnPoints: 0
hnComments: 0
buzz: 0
---

Vishnu Arun | Tech Lead, Feature Importance Platform; Anderson Lam | Sr Software Engineer; Andrew Qiu | Machine Learning Engineer I; Helena Xu | Data Scientist I; Tianyou Wang | Data Scientist II Introduction In our multi-part blog series, we have discussed why we chose Ray as a last mile data processing framework, how we integrated Ray into our existing ML Training Infrastructure, and how we enabled efficient Batch Inference at scale. In this blog post, we will discuss how we were able to apply Ray to another critical part of our ML Infrastructure stack: Model Evaluation . In the Ray Batch Inference Blog Post , we ended on a section on accumulators (counters that would allow us to calculate metrics like ROC-AUC and cross entropy). This post is where those accumulators pay off: a model evaluation platform that combines the strengths of Ray and Apache Spark to compute metrics efficiently

*Reproduced from the Pinterest Engineering feed. No model was used to write this entry — follow the link for the full article.*
