---
title: "TimeSeries Tiered Storage Journey: Kafka/Flink Streams to Native Cassandra Cold Reads"
description: "By Oleksii Tkachuk , Rajiv Shringi , Chris Lohfink , Abe Ratnofsky , Kartik Sathyanarayanan Introduction In an earlier post , we introduced the TimeSeries Abstraction, our high-throughput, low-latency platform designed t"
pubDate: 2026-10-14T19:56:08+00:00
addedAt: 2026-10-15T09:18:01.001290+00:00
source: "Netflix Tech"
category: company_eng
sourceUrl: "https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60?source=rss----2615bd06b42e---4"
tags: ["tech"]
heat: 100
score: 0.87553
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*ZL0rDP0Un-DxepYPmFo4aQ.png"
---

By Oleksii Tkachuk , Rajiv Shringi , Chris Lohfink , Abe Ratnofsky , Kartik Sathyanarayanan Introduction In an earlier post , we introduced the TimeSeries Abstraction, our high-throughput, low-latency platform designed to store and query temporal event data at scale. It has since become the operational backbone for Netflix’s largest datasets, which now span multiple petabytes. However, managing such large datasets in hot storage, tuned for low-millisecond latency access , is not cheap. At Netflix, cost-efficiency is a continuous discipline rather than a temporary initiative. This post shares two solutions that significantly reduce storage costs by continuously moving older, less frequently accessed data into cheaper object storage: Solution 1 : Uses Apache Kafka and Flink to stream data directly to S3 Solution 2 : Leverages Cassandra backups in S3 and pluggable Memtables to read data dir

*Reproduced from the Netflix Tech feed. No model was used to write this entry — follow the link for the full article.*
