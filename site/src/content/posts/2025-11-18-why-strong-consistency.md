---
title: "Why Strong Consistency?"
description: "Why Strong Consistency? Eventual consistency makes your life harder."
pubDate: 2025-11-18T00:00:00+00:00
addedAt: 2026-09-11T10:52:16.178795+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/11/18/consistency.html"
tags: ["aws"]
heat: 55
score: 0.34751
readMinutes: 1
image: "https://brooker.co.za/blog/images/1205_write_arch.jpg"
imageAlt: "Architecture diagram showing Aurora DSQL components: three AZ Endpoints, four Query Processors, three Adjudicators, three Journals, and six Storage nodes arranged left to right, with the top AZ Endpoint connecting to the second Query Processor via orange &quot;Reads and Writes&quot; line, the second Query Processor connecting to the first two Adjudicators via red &quot;Commits&quot; lines, a red &quot;Commits&quot; line between the first two Adjudicators, the second Adjudicator connecting to the second Journal via red &quot;Commits&quot; line, and the second Journal connecting to the second and fourth Storage nodes via red &quot;Commits&quot; lines, with legend showing orange for &quot;Reads and Writes&quot;, green dashed for &quot;Reads&quot;, and red for &quot;Commits&quot;"
---

Why Strong Consistency? Eventual consistency makes your life harder. When I started at AWS in 2008, we ran the EC2 control plane on a tree of MySQL databases: a primary to handle writes, a secondary to take over from the primary, a handful of read replicas to scale reads, and some extra replicas for doing latency-insensitive reporting stuff. All of thing was linked together with MySQL’s statement-based replication. It worked pretty well day to day, but two major areas of pain have stuck with me ever since: operations were costly, and eventual consistency made things weird. Since then, managed databases like Aurora MySQL have made relational database operations orders of magnitude easier. Which is great. But eventual consistency is still a feature of most database architectures that try scale reads. Today, I want to talk about why eventual consistency is a pain, and why we invested heavil

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
