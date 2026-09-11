import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { ACCEPTED_CATEGORIES, DEFAULT_CATEGORY } from './categories';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    // When THIS SITE published the story, as opposed to when its author did.
    // Optional: posts written before the field existed do not have it. The
    // curator prunes on this, because pubDate for an evergreen story can be
    // years old and pruning on it deletes the best content first.
    addedAt: z.coerce.date().optional(),
    source: z.string().default('unknown'),
    sourceUrl: z.string().url().optional(),
    tags: z.array(z.string()).default([]),
    heat: z.number().min(0).max(100).default(50),
    // Raw ranker score. `heat` is normalised per run and is display-only; this
    // is the value that can be compared across runs (used by the weekly digest).
    score: z.number().default(0),
    readMinutes: z.number().default(2),
    // Which section a story belongs to. Derived from the FEED it came from,
    // never from keywords: a gaming site covering NVIDIA earnings is still
    // gaming, and a fintech site covering a game studio is still fintech.
    // Keyword guessing would get both wrong.
    //
    // The list is imported, not literal. It is a CLOSED enum, so an unknown
    // category is a hard build failure rather than a silently mis-shelved post
    // — which is the behaviour we want, but it means the curator's list and
    // this one must never drift. curator/test_categories.py enforces that.
    // ACCEPTED = the live categories plus the legacy ones still on disk. A
    // z.enum is closed in BOTH directions, so narrowing it to the live list
    // rejects every post the old taxonomy wrote — 55 of the 60 on disk.
    category: z.enum(ACCEPTED_CATEGORIES).default(DEFAULT_CATEGORY),
    // Lead image for the story, taken from the feed entry (media:content,
    // media:thumbnail or enclosure). Optional: TechCrunch ships no image, and
    // any feed can omit one, so every layout must survive its absence.
    image: z.string().url().optional(),
    imageAlt: z.string().optional(),
  }),
});

export const collections = { posts };
