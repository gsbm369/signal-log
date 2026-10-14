---
title: "Linus Torvalds's first LLM-assisted patch series"
description: "At the recently concluded Maintainers Summit , Linus Torvalds said that he had been using a large language model to work on a patch series addressing a longstanding problem; he has now posted that series for review . The"
pubDate: 2026-10-14T13:50:29+00:00
addedAt: 2026-10-14T15:18:06.808615+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1100449/"
tags: ["llm", "benchmark"]
heat: 100
score: 1.54565
readMinutes: 1
---

At the recently concluded Maintainers Summit , Linus Torvalds said that he had been using a large language model to work on a patch series addressing a longstanding problem; he has now posted that series for review . The fairly short series of ten patches basically enhances folio lookup by noticing when folios are hot, and setting a "delay releasing this folio until after a RCU period", and then using that RCU delay it does not just the folio lookup itself under RCU (which we've done forever), but also the actual folio data accesses themselves under RCU. No refcount taking needed for the fastpath where we can just read the data from the folio entirely in an RCU-protected region when the user copy doesn't cause page faults. The end result is an order-of-magnitude speedup for a read() -heavy benchmark. Review has already identified a race condition in the code, though, so further work will

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
