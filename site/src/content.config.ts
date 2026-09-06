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
  }),
});

export const collections = { posts };
