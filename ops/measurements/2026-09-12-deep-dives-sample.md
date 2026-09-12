# deep_dives editorial sample — 2026-09-12

30 candidates drawn at random (seed 20260912) from the 85 the four deep_dives
sources offered, classified by hand before proposing any rule.

**Technical** = engineering substance: a system, a tool, a measurement, a
technique. **Non-technical** = career, hiring, industry news, commentary, meta,
or an announcement — regardless of how good it is.

| # | source | title | class |
|---|---|---|---|
| 1 | jvns.ca | Some notes on starting to use Django | technical |
| 2 | Dan Luu | In defense of simple architectures | technical |
| 3 | The Changelog | Exploring with agents | technical |
| 4 | jvns.ca | What's involved in getting a "modern" terminal setup? | technical |
| 5 | jvns.ca | Links to CSS colour palettes | non-technical |
| 6 | Brendan Gregg | Third Stage Engineering | non-technical |
| 7 | Dan Luu | Finding the Story | non-technical |
| 8 | Brendan Gregg | Leaving Intel | non-technical |
| 9 | Dan Luu | The container throttling problem | technical |
| 10 | jvns.ca | New zine: The Secret Rules of the Terminal | non-technical |
| 11 | The Changelog | Automation at the speed of Swamp | non-technical |
| 12 | Brendan Gregg | Why I joined OpenAI | non-technical |
| 13 | Dan Luu | Some latency measurement pitfalls | technical |
| 14 | Dan Luu | Misidentifying talent | non-technical |
| 15 | Brendan Gregg | No More Blue Fridays | technical |
| 16 | jvns.ca | A data model for Git (and other docs updates) | technical |
| 17 | Dan Luu | Steve Ballmer was an underrated CEO | non-technical |
| 18 | Dan Luu | Major errors on this blog (and their corrections) | non-technical |
| 19 | jvns.ca | Examples for the tcpdump and dig man pages | technical |
| 20 | Dan Luu | Against essential and accidental complexity | technical |
| 21 | jvns.ca | How to add a directory to your PATH | technical |
| 22 | Brendan Gregg | On "AI Brendans" or "Virtual Brendans" | non-technical |
| 23 | The Changelog | Astral has been acquired by OpenAI | non-technical |
| 24 | jvns.ca | Testing Vue components in the browser | technical |
| 25 | jvns.ca | Notes on switching to Helix from vim | technical |
| 26 | jvns.ca | Some terminal frustrations | technical |
| 27 | Dan Luu | The value of in-house expertise | non-technical |
| 28 | Dan Luu | Bug blindness | technical |
| 29 | jvns.ca | Notes on clarifying man pages | technical |
| 30 | Dan Luu | Cocktail party ideas | non-technical |

## Ratio

**16 technical / 14 non-technical — 53%.** Nearly half of what the deep_dives
section offers is not an engineering deep dive.

## The ratio is a property of the SOURCE, not of the title

| source | sampled | technical | rate |
|---|---|---|---|
| jvns.ca | 11 | 9 | **82%** |
| Dan Luu | 11 | 5 | 45% |
| The Changelog | 3 | 1 | 33% |
| Brendan Gregg | 5 | 1 | **20%** |

This is why the instruction to measure before proposing keywords was right, and
a keyword rule is the wrong instrument. There is no lexical signal separating
"The container throttling problem" from "Misidentifying talent" that would not
also catch half of what we want — both are plain English, neither carries
jargon. The separating variable is who wrote it and in what mode.

Brendan Gregg at 20% is the striking one. He was added as the archetypal
evergreen engineering source; his recent output is largely career and industry
commentary (*Leaving Intel*, *Why I joined OpenAI*, *Third Stage Engineering*,
*On "AI Brendans"*). The one technical piece in his sample, *No More Blue
Fridays*, is genuinely excellent — which is the problem: dropping the source
loses it, keeping the source brings four career posts with it.

## What NOT to do

- **Keyword allow/deny lists.** Measured above: no lexical boundary exists.
- **Dropping Brendan Gregg.** 20% of a very good source is still worth having.
- **Tuning today.** Five sources landed hours ago and devops_linux is at 43% on
  an onboarding spike; any rule fitted now is fitted to a transient.

## Options worth considering, in order of confidence

1. **Per-source trust weight already expresses this and is not being used for
   it.** Gregg sits at 1.00 — joint highest in the config — on a 20% hit rate.
   Dropping him to ~0.80 and jvns to 1.00 costs nothing structurally and lets
   the existing ranker do the work. This is the cheapest change and the one the
   config was designed for.
2. **A `deep_dives` sub-cap per source**, so no single author supplies more than
   two of the section's six. Addresses concentration, not quality.
3. **Nothing.** At 53% and a six-item cap, roughly three of the six are genuine
   deep dives each issue. That may simply be acceptable.

No rule proposed for adoption yet — the sample is 30 items from four sources on
one day, and option 1 should be measured over a week before it is trusted.
