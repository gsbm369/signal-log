/* FRESHNESS POLICY (owner, 2026-09-18) — the site half.
 *
 *   age        = cycle start (UTC) minus the AUTHOR's publication date
 *   today      age <= 24h
 *   this week  age <= 7d
 *   stale      > 7d — never rendered
 *
 * The clock is CYCLE_START_UTC, exported by run-cycle.sh before it curates and
 * builds, so the curator's ingest gate and pruner, this build, and the publish
 * gate that parses this build's output all measure against the same instant.
 * A build without it (local dev) falls back to now.
 */
export const FRESH_DAYS = 7;

export const cycleStart: Date = (() => {
  const raw = process.env.CYCLE_START_UTC;
  const d = raw ? new Date(raw) : new Date();
  return Number.isNaN(d.valueOf()) ? new Date() : d;
})();

export type Freshness = 'today' | 'week' | 'stale';

export const ageHours = (d: Date): number => (cycleStart.valueOf() - d.valueOf()) / 3_600_000;

export const freshnessOf = (d: Date): Freshness => {
  const h = ageHours(d);
  if (h <= 24) return 'today';
  if (h <= FRESH_DAYS * 24) return 'week';
  return 'stale';
};

/* The one ordering every page uses: today before this week; within a tier the
   curator's score, best first; then id in CODEPOINT order — not localeCompare,
   which can ignore punctuation and would disagree with check_selection.py. */
type Ranked = { id: string; data: { pubDate: Date; score?: number } };
const TIER_RANK: Record<Freshness, number> = { today: 0, week: 1, stale: 2 };
export const byOrder = (a: Ranked, b: Ranked): number =>
  TIER_RANK[freshnessOf(a.data.pubDate)] - TIER_RANK[freshnessOf(b.data.pubDate)] ||
  (b.data.score ?? 0) - (a.data.score ?? 0) ||
  (a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
