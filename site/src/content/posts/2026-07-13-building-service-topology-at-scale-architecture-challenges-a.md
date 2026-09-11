---
title: "Building Service Topology at Scale: Architecture, Challenges, and Lessons Learned"
description: "By Parth Jain , Rakesh Sukumar , Yingwu Zhao , Renzo Sanchez-Silva Nathan Fisher A deep dive into the engineering challenges of building a real-time service dependency map at Netflix scale: from streaming architectures a"
pubDate: 2026-07-13T22:44:11+00:00
addedAt: 2026-09-11T10:52:16.177865+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/building-service-topology-at-scale-architecture-challenges-and-lessons-learned-f4b792f3f0d8?source=rss----2615bd06b42e---4"
tags: ["ebpf"]
heat: 18
score: 0.05438
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/947/1*dgCgcPQv-EvBNb_AXqtnhA.png"
imageAlt: "Diagram showing backpressure propagating backward through a pipeline — from Stage 3 to Stage 2 to Stage 1 to the message stream — each stage signaling the previous one to slow dow"
---

By Parth Jain , Rakesh Sukumar , Yingwu Zhao , Renzo Sanchez-Silva Nathan Fisher A deep dive into the engineering challenges of building a real-time service dependency map at Netflix scale: from streaming architectures and distributed aggregation pipelines to time-travel queries and the methodology that made it work. Introduction In our first post , we introduced the problem: engineers at Netflix needed a unified, real-time view of service dependencies to troubleshoot faster, understand blast radius, and navigate our distributed architecture. We described our multi-source approach, combining eBPF network flows, IPC metrics, and distributed tracing into physically separate graph layers that can be queried independently or merged into a comprehensive view. That post explained what we built and why . This post is about how , the engineering reality of building this system at Netflix scale.

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
