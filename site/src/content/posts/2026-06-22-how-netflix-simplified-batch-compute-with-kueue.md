---
title: "How Netflix Simplified Batch Compute with Kueue"
description: "By Alvin Bao , Alex Petrov , Jennifer Lai , Aidan Sherr , and Samartha Chandrashekar As a part of the journey to transition Netflix’s compute infrastructure to be more Kubernetes-native, we have leaned into incorporating"
pubDate: 2026-06-22T21:35:01+00:00
addedAt: 2026-09-11T11:03:46.192187+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/how-netflix-simplified-batch-compute-with-kueue-87860682629c?source=rss----2615bd06b42e---4"
tags: ["kubernetes"]
heat: 9
score: 0.01917
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*MfDuB407Rq81AHZEbhARWA.png"
---

By Alvin Bao , Alex Petrov , Jennifer Lai , Aidan Sherr , and Samartha Chandrashekar As a part of the journey to transition Netflix’s compute infrastructure to be more Kubernetes-native, we have leaned into incorporating components from the Kubernetes ecosystem into our container platform Titus . One example of this is our use of Kueue , a cloud-native job queueing system for batch workloads, which has largely replaced the custom queuing and scheduling logic in our homegrown managed batch solution Compute Managed Batch (CMB). In this post, we’ll give an overview of what motivated the migration, how we migrated millions of batch jobs to use Kueue, and what Kueue allows us to offer as a Compute platform. Brief Overview of CMB and Titus CMB is a managed batch solution that allows users and applications to execute and manage workloads that run to completion. Using a tenant hierarchy, workloa

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
