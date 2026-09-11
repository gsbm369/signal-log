---
title: "Decomposing Aurora DSQL"
description: "Decomposing Aurora DSQL Riffing, I guess. Earlier today, Alex Miller wrote an excellent blog post titled Decomposing Transaction Systems ."
pubDate: 2025-04-17T00:00:00+00:00
addedAt: 2026-09-11T11:27:00.665984+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/04/17/decomposing.html"
tags: ["tech"]
heat: 36
score: 0.13203
readMinutes: 1
image: "https://brooker.co.za/blog/images/dsql_txn_order.png"
---

Decomposing Aurora DSQL Riffing, I guess. Earlier today, Alex Miller wrote an excellent blog post titled Decomposing Transaction Systems . It’s one of the best things I’ve read about transactions this year, maybe the best. You should read it now. In the post, Alex breaks transactions down like this: Every transactional system does four things: It executes transactions. It orders transactions. It validates transactions. It persists transactions. then describes how these steps map to traditional OCC and PCC systems, research designs like Calvin, and real-world systems like FoundationDB. How do these steps map to Aurora DSQL ? An overview of DSQL’s architecture may be useful if you haven’t been following along so far: Now, an hour of video and 20 minutes of reading another post later, we’re back. Let’s dive in. Executing a transaction means evaluating the body of the transaction to produce

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
