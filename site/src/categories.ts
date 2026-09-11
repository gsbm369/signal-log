/* The site's category list.
 *
 * SINGLE SOURCE OF TRUTH FOR THE SITE HALF of the contract. The curator half
 * lives in `scoring.categories` in curator/feeds.yml, which is itself generated
 * from `scoring_categories` in ansible/deploy.yml.
 *
 * These two lists MUST agree, and curator/test_categories.py fails the build if
 * they drift. That test exists because widening the enum without it just moves
 * the trap: the schema is a hard failure at build time, so a category added to
 * the curator and forgotten here does not degrade — it stops the site building,
 * hours later, from a file nobody was editing.
 *
 * Adding a category: add it to ansible/deploy.yml, run the playbook, add it
 * here, run curator/test_categories.py.
 */
export const CATEGORIES = [
  'system_design',
  'company_eng',
  'devops_linux',
  'deep_dives',
  'aggregators',
  'fintech',
  'gaming',
] as const;

export type Category = (typeof CATEGORIES)[number];

/* Categories the curator no longer emits, still present on posts already on
 * disk. The schema must accept them or the site cannot build at all: widening
 * the enum to the seven above and nothing else rejected all 55 surviving posts
 * from the news taxonomy, because a z.enum is closed in both directions.
 *
 * These are NOT part of the curator contract and the drift test deliberately
 * ignores them. They age out on their own — max_posts prunes the oldest, so the
 * list empties as the newsletter publishes. When `grep -c "^category: tech"` over
 * site/src/content/posts returns 0 for all three, delete this array.
 *
 * `gaming` is absent because it exists in BOTH taxonomies and is live above.
 */
export const LEGACY_CATEGORIES = ['tech', 'markets', 'world'] as const;

/* What the schema will accept: the live contract plus whatever has not aged out. */
export const ACCEPTED_CATEGORIES = [...CATEGORIES, ...LEGACY_CATEGORIES] as const;

/* Fallback for a post written before categories existed, and for any post whose
 * category the schema default had to supply. */
export const DEFAULT_CATEGORY: Category = 'aggregators';
