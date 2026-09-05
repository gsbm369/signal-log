// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// Canonical origin, used for RSS <link> elements and any absolute URLs.
// Set SITE_URL in .env so the feed is correct behind the reverse proxy.
const site = process.env.SITE_URL || 'http://localhost:8080';

// https://astro.build/config
export default defineConfig({
  site,
  vite: {
    plugins: [tailwindcss()],
  },
});
