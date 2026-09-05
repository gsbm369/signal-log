// @ts-check
import { readFileSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

/**
 * The canonical origin has exactly one definition: public/CNAME.
 *
 * That file already IS the domain binding — GitHub Pages reads it to attach the
 * custom domain, and Astro copies it into every build. Deriving `site` from it
 * means the hostname is never duplicated into the workflow, the playbook, or a
 * second environment variable that can drift out of sync.
 *
 * Order of precedence:
 *   1. SITE_URL          explicit override (local preview, staging)
 *   2. public/CNAME      the domain binding — what production uses
 *   3. localhost:8080    local dev with no custom domain
 */
function resolveSite() {
  if (process.env.SITE_URL) return process.env.SITE_URL.replace(/\/+$/, '');
  try {
    const cname = readFileSync(new URL('./public/CNAME', import.meta.url), 'utf8').trim();
    if (cname) return `https://${cname}`;
  } catch {
    // No CNAME: local development without a custom domain.
  }
  return 'http://localhost:8080';
}

const site = resolveSite();

// A production build that silently publishes localhost links must not be able to
// succeed. CI has no .env, so if public/CNAME were deleted or emptied the build
// would fall through to localhost and poison every canonical URL and every RSS
// <link> — the failure would only show up in the published feed. Fail loudly here.
const inCI = process.env.CI === 'true' || process.env.GITHUB_ACTIONS === 'true';
if (inCI && /^https?:\/\/(localhost|127\.0\.0\.1|\[::1\])(:|\/|$)/.test(site)) {
  throw new Error(
    `Refusing to build in CI with site="${site}".\n` +
    `Every canonical URL and every RSS <link> would point at localhost.\n` +
    `Expected site/public/CNAME to hold the public hostname, or SITE_URL to be set.`
  );
}

// `base` stays '/' because there is a custom domain. Without one it would have to
// be '/signal-log', and every internal link would break in a way that only
// appears in production.
export default defineConfig({
  site,
  base: '/',
  trailingSlash: 'always',
  vite: {
    plugins: [tailwindcss()],
  },
});
