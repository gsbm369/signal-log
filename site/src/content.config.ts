import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    source: z.string().default('unknown'),
    sourceUrl: z.string().url().optional(),
    tags: z.array(z.string()).default([]),
    heat: z.number().min(0).max(100).default(50),
    // Raw ranker score. `heat` is normalised per run and is display-only; this
    // is the value that can be compared across runs (used by the weekly digest).
    score: z.number().default(0),
    readMinutes: z.number().default(2),
    // Which shelf a story belongs to. Derived from the FEED it came from, never
    // from keywords: a gaming site covering NVIDIA earnings is still gaming, and
    // a markets site covering a game studio is still markets. Keyword guessing
    // would get both wrong. Defaults to tech so posts written before categories
    // existed stay valid.
    category: z.enum(['tech', 'markets', 'gaming', 'world']).default('tech'),
    // Lead image for the story, taken from the feed entry (media:content,
    // media:thumbnail or enclosure). Optional: TechCrunch ships no image, and
    // any feed can omit one, so every layout must survive its absence.
    image: z.string().url().optional(),
    imageAlt: z.string().optional(),
  }),
});

export const collections = { posts };
