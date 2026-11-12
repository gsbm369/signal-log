---
title: "Bliki: Generated Glossary"
description: "When we use LLMs in a specialized domain, such as the operations of any reasonably-large organization, there is a lot of specialized vocabulary. Such words and specialized meanings will be foreign to an LLM because they "
pubDate: 2026-11-12T14:15:00+00:00
addedAt: 2026-11-12T15:48:06.366525+00:00
source: "Martin Fowler"
category: system_design
sourceUrl: "https://martinfowler.com/bliki/GeneratedGlossary.html"
tags: ["llm"]
heat: 81
score: 1.14268
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

When we use LLMs in a specialized domain, such as the operations of any reasonably-large organization, there is a lot of specialized vocabulary. Such words and specialized meanings will be foreign to an LLM because they aren't in its training set, making it harder for the LLM to be effective when doing tasks in that domain. One technique to aid this is to use an LLM to generate a glossary of the terminology in that domain, and make this glossary available for any LLMs doing work in those circumstances. The sources for the LLM can be any material within the organization concerned such as documents, emails, and chat logs. In some cases getting transcripts of audio or video may be helpful, although most organizations generate enough text to do the job. The glossary-generating LLM should look for single words, and phrases of several words that regularly hang out together to form a meaningful

*Reproduced from the Martin Fowler feed. No model was used to write this entry — follow the link for the full article.*
