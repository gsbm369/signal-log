---
title: "GitHub Actions leaking secrets when Miri output is cached"
description: "The Rust Security Response Team was notified that Miri stores all environment variables to target/ , allowing secrets to persist in caches. While not necessary a vulnerability in and of itself, when paired with GitHub Ac"
pubDate: 2026-09-21T00:00:00+00:00
addedAt: 2026-09-21T21:17:36.839379+00:00
source: "Rust Blog"
category: languages
sourceUrl: "https://blog.rust-lang.org/2026/09/21/github-actions-leaking-secrets-when-miri-output-is-cached/"
tags: ["rust", "vulnerab"]
heat: 97
score: 1.05329
readMinutes: 1
image: "https://www.rust-lang.org/static/images/rust-social.jpg"
---

The Rust Security Response Team was notified that Miri stores all environment variables to target/ , allowing secrets to persist in caches. While not necessary a vulnerability in and of itself, when paired with GitHub Actions caching behavior, it is possible for this to expose secrets to PRs. Overview GitHub Actions makes it possible to cache directories between runs. Typical setups allow CI runs on main (and other branches) to write to cache, and PRs can only read from cache (preventing cache poisoning). Rust projects tend to speed up CI by caching binaries built by cargo install and sometimes the contents of target/ . PR CI can be triggered by anyone who can open PRs on your repository. GitHub requires maintainer approval for the first PR, but future PRs will rerun CI on every push. Anyone who has previously landed a change can trigger a CI run extracting information from cached target

*Reproduced from the Rust Blog feed. No model was used to write this entry — follow the link for the full article.*
