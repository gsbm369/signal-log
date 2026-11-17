---
title: "De-identifying text at scale: How Airbnb protects personal data in AI training"
description: "Here’s how Airbnb detects and replaces personal data in messages, reviews, and support chats before it reaches a model. By: Emelin Flores , Alex Klimov , Lee Formyduval , Bahador Nooraei Introduction Airbnb is built on t"
pubDate: 2026-11-17T18:01:03+00:00
addedAt: 2026-11-17T21:48:37.768051+00:00
source: "Airbnb Engineering"
category: company_eng
sourceUrl: "https://medium.com/airbnb-engineering/de-identifying-text-at-scale-how-airbnb-protects-personal-data-in-ai-training-32f3ff8ff7d0?source=rss----53c7c27702d5---4"
tags: ["tech"]
heat: 69
score: 0.9426
readMinutes: 1
image: "https://cdn-images-1.medium.com/max/1024/1*nyiV0meGhVO9cZszJPeHCQ.jpeg"
imageAlt: "A bright, open-air dining area featuring a rustic, light-washed wooden table and matching benches set for a meal. A large woven white pendant light hangs from a high, exposed wooden ceiling. The left side of the room is completely open to a lush tropical garden with a tall, vine-covered wall and large elephant ear plants, bringing natural light into the white-tiled space."
hnPoints: 0
hnComments: 0
buzz: 0
---

Here’s how Airbnb detects and replaces personal data in messages, reviews, and support chats before it reaches a model. By: Emelin Flores , Alex Klimov , Lee Formyduval , Bahador Nooraei Introduction Airbnb is built on trust. Every night that a guest books a stay, or a host welcomes someone into their home, that trust is backed by information they’ve shared with us, which includes personally identifiable information (PII) such as names, home location, current location, and payment details. We now use transaction information to train machine learning models. Before we do so, we remove PII to minimize the number of copies of this information and prevent leakage into and through our models. As we’ve written before , Airbnb maintains a shared taxonomy as to what constitutes PII, from commonly used fields such as names and card numbers to less frequently used fields such as precise location c

*Reproduced from the Airbnb Engineering feed. No model was used to write this entry — follow the link for the full article.*
