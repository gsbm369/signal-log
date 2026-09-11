---
title: "Seven Years of Firecracker"
description: "Seven Years of Firecracker Time flies like an arrow. Fruit flies like a banana."
pubDate: 2025-09-18T00:00:00+00:00
addedAt: 2026-09-11T11:03:46.193107+00:00
source: "Marc Brooker"
category: system_design
sourceUrl: "http://brooker.co.za/blog/2025/09/18/firecracker.html"
tags: ["kernel", "aws"]
heat: 47
score: 0.27475
readMinutes: 1
image: "https://brooker.co.za/blog/images/agentore_runtime_isol.png"
---

Seven Years of Firecracker Time flies like an arrow. Fruit flies like a banana. Back at re:Invent 2018, we shared Firecracker with the world. Firecracker is open source software that makes it easy to create and manage small virtual machines. At the time, we talked about Firecracker as one of the key technologies behind AWS Lambda, including how it’d allowed us to make Lambda faster, more efficient, and more secure. A couple years later, we published Firecracker: Lightweight Virtualization for Serverless Applications (at NSDI’20). Here’s me talking through the paper back then: The paper went into more detail into how we’re using Firecracker in Lambda, how we think about the economics of multitenancy ( more about that here ), and how we chose virtualization over kernel-level isolation (containers) or language-level isolation for Lambda. Despite these challenges, virtualization provides man

*Reproduced from the Marc Brooker feed. No model was used to write this entry — follow the link for the full article.*
