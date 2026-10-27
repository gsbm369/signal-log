---
title: "TLA-Verus: LLM agents prove temporal properties of TLA+ specs"
description: "This NeurIPS'26 workshop paper takes TLA+ specs from GitHub, translates them into Verus, and has LLM agents prove the safety and liveness properties in the specs. The motivation The paper aims to address two problems it "
pubDate: 2026-10-27T19:13:12+00:00
addedAt: 2026-10-27T22:18:32.045254+00:00
source: "Murat Demirbas"
category: system_design
sourceUrl: "https://muratbuffalo.blogspot.com/2026/10/tla-verus-llm-agents-prove-temporal.html"
tags: ["llm", "rust"]
heat: 100
score: 1.54766
readMinutes: 1
image: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg6rAvVf2m_S8K8-Ovw8bfaOg7S_MN3LGG6ZuZqeR2joMYNPmRK4wLmHuatPvLzZyudPLDjV8EExJz-6LQnTkYmaYg_PNYQc-CZLSBvflhGk2WKP0SRq6xNP74MiL3aBqB0Gdx71CA-ESqfUx7j0ELELKu7Ua3GXdEJSP5pdAihyNdNvfjQpT0UGIdaw1w/s72-w640-h170-c/Screenshot%202026-10-27%20at%2012.09.46%E2%80%AFPM.png"
---

This NeurIPS'26 workshop paper takes TLA+ specs from GitHub, translates them into Verus, and has LLM agents prove the safety and liveness properties in the specs. The motivation The paper aims to address two problems it raises with TLA+. First, nothing ties the spec to the code, so they drift apart. And second, it claims that proof support is thin: TLC only checks small configurations, and TLAPS is weak on liveness. They abandon pursuing the first weakness they raise at the onset of the paper. Closing it needs a proof that the generated Rust code (which it turns out TLA-Verus doesn't produce anyway) refines the spec, so they list this as future work. It gets worse though. There is no refinement proof between the TLA+ spec and the Verus spec either. Nothing establishes that the translated Verus spec means what the original meant. (Trace validation, meanwhile, is a viable way of tying TLA+

*Reproduced from the Murat Demirbas feed. No model was used to write this entry — follow the link for the full article.*
