---
title: "Infrastructure Team 2026 Q3 Recap and Q4 Plan"
description: "Here's what the Infrastructure Team delivered in Q3 2026 and what we're focusing on in Q4. You can find the previous blog post of this series here ."
pubDate: 2026-10-12T00:00:00+00:00
addedAt: 2026-10-13T16:25:24.324168+00:00
source: "Inside Rust"
category: languages
sourceUrl: "https://blog.rust-lang.org/inside-rust/2026/10/12/infrastructure-team-q3-recap-and-q4-plan/"
tags: ["aws", "rust"]
heat: 71
score: 0.87602
readMinutes: 1
image: "https://www.rust-lang.org/static/images/rust-social.jpg"
---

Here's what the Infrastructure Team delivered in Q3 2026 and what we're focusing on in Q4. You can find the previous blog post of this series here . Q3 2026 Accomplishments Audit logs in Datadog Cloud SIEM We enabled audit logs for the following services and sent them to Datadog, so that the Rust Foundation security team can analyze them using Cloud SIEM : The Rust GitHub Enterprise and the Rust Foundation GitHub Enterprise, via audit log streaming . AWS, via CloudTrail . Heroku, Wiz, Fastly, and Datadog itself. See the GitHub issue for more details. Web Application Firewall and DDoS protection for crates.io and docs.rs Together with the crates.io and docs.rs teams, we set up the Fastly Next-Gen WAF (Web Application Firewall) for docs.rs and crates.io (see the GitHub issue ). The WAF blocks potential security threats and enforces rate limits. We also enabled Fastly DDoS protection for bo

*Reproduced from the Inside Rust feed. No model was used to write this entry — follow the link for the full article.*
