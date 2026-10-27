---
title: "How Anchorage Digital and Turnkey verify code with AWS Nitro Enclaves"
description: "Anchorage Digital and Turnkey built verifiable infrastructure on AWS Nitro Enclaves so crypto wallets can cryptographically verify which code parsed a transaction. This post covers the architecture, the attestation-gated"
pubDate: 2026-10-27T17:10:35+00:00
addedAt: 2026-10-27T22:18:32.044082+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-anchorage-digital-and-turnkey-verify-code-with-aws-nitro-enclaves/"
tags: ["aws"]
heat: 94
score: 1.38773
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/10/09/ARCHBLOG-1598-1-1.png"
imageAlt: "Flow diagram: a wallet client sends a raw transaction to a Nitro Enclave, which returns parsed JSON and a signed attestation."
---

Anchorage Digital and Turnkey built verifiable infrastructure on AWS Nitro Enclaves so crypto wallets can cryptographically verify which code parsed a transaction. This post covers the architecture, the attestation-gated access pattern, and how it extends to any high-trust workflow beyond blockchain.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
