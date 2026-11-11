---
title: "Tests as data: ensuring AI-generated code does what we want"
description: "Automated testing in the age of AI coding assistants is problematic: when AI agents write both production and test code, developers risk losing the assurance that automated tests protect against functional errors. Matteo"
pubDate: 2026-11-11T15:17:00+00:00
addedAt: 2026-11-11T15:49:21.853377+00:00
source: "Martin Fowler"
category: system_design
sourceUrl: "https://martinfowler.com/articles/tests-as-data.html"
tags: ["tech"]
heat: 69
score: 0.99779
readMinutes: 1
image: "https://martinfowler.com/articles/tests-as-data/card.png"
hnPoints: 2
hnComments: 0
buzz: 18
---

Automated testing in the age of AI coding assistants is problematic: when AI agents write both production and test code, developers risk losing the assurance that automated tests protect against functional errors. Matteo Vaccari makes three claims: (1) when AI writes the code, developers become its customers; (2) therefore customer tests, not developer tests, become the primary contract between humans and AI; (3) moving that contract into test data rather than test code makes it easier to protect it from unexpected modifications by coding agents. All of this optimizes for human-readable tests that establish a contract between humans and AI. While in the past DSL parsers and custom test runners were expensive to write and maintain, now AI makes them cheap. more…

*Reproduced from the Martin Fowler feed. No model was used to write this entry — follow the link for the full article.*
