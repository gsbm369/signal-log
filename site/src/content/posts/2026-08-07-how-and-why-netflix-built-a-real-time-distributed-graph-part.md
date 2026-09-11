---
title: "How and Why Netflix Built a Real-Time Distributed Graph: Part 3 — Querying the graph with gRPC…"
description: "How and Why Netflix Built a Real-Time Distributed Graph: Part 3 — Querying the graph with gRPC execution API Authors: Nilesh Mishra and Ajit Koti This is the third entry of a multi-part blog series describing how we buil"
pubDate: 2026-08-07T16:01:02+00:00
addedAt: 2026-09-11T10:20:27.665658+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/how-and-why-netflix-built-a-real-time-distributed-graph-part-3-querying-the-graph-with-grpc-0f3468349607?source=rss----2615bd06b42e---4"
tags: ["tech"]
heat: 46
score: 0.16097
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*X_O1wdMIVfm9upb2tLXD9A.png"
---

How and Why Netflix Built a Real-Time Distributed Graph: Part 3 — Querying the graph with gRPC execution API Authors: Nilesh Mishra and Ajit Koti This is the third entry of a multi-part blog series describing how we built a Real-Time Distributed Graph (RDG). In Part 1 , we discussed the motivation for creating the RDG and the architecture of the data processing pipeline that populates it. In Part 2 , we discussed how we designed the storage layer to handle billions of nodes and edges while maintaining single-digit-millisecond latency. In Part 3, we will explore how we designed a fast, flexible serving layer to efficiently query the graph. Introduction In Part 1 of this series, we described why Netflix needed a Real-Time Distributed Graph (RDG) and how we used Apache Flink to build an ingestion and processing pipeline that turns streaming events into graph primitives. In Part 2 , we explo

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
