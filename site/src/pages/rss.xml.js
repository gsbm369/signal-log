import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  // Sorted and dated by addedAt — when THIS FEED published the item — not by
  // when its author did.
  //
  // There is no item cap here; every post is emitted. The failure is in the
  // ordering, and it is the pruner bug one layer up: a feed reader sorts by
  // pubDate and marks read by GUID, so an evergreen piece we curate today but
  // whose author wrote it in January 2024 arrives at the very bottom of the
  // subscriber's list, stamped two years old, below everything they have
  // already scrolled past. Delivered, and invisible — sunk by the exact
  // property it was selected for.
  //
  // RSS pubDate means "when this item was published in this feed", which for a
  // curated feed is when it was curated. The author's date is not lost: it moves
  // to signal:originDate below, where it is data rather than an ordering key.
  const entered = (p) => (p.data.addedAt ?? p.data.pubDate).valueOf();
  const posts = (await getCollection('posts')).sort((a, b) => entered(b) - entered(a));

  return rss({
    title: 'signal.log',
    description: 'An engineering newsletter — system design, company engineering, deep dives, devops, fintech and gaming. Ranked by an open heuristic: per-category recency decay, source trust, topic relevance, deduplication. No model in the ranking.',
    site: context.site,
    trailingSlash: true,
    // Custom fields live in their own namespace so they cannot collide with
    // reserved RSS 2.0 elements (<source> in particular).
    xmlns: { signal: 'https://signal.log/ns#' },
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.addedAt ?? post.data.pubDate,
      link: `/posts/${post.id}/`,
      categories: post.data.tags,
      // Provenance for anything consuming this feed programmatically.
      customData: [
        `<signal:source>${escapeXml(post.data.source)}</signal:source>`,
        post.data.sourceUrl
          ? `<signal:originUrl>${escapeXml(post.data.sourceUrl)}</signal:originUrl>`
          : '',
        // When the AUTHOR published it, as distinct from when this feed did.
        // For the evergreen categories these are months or years apart, and the
        // difference is the whole point of the publication.
        `<signal:originDate>${post.data.pubDate.toUTCString()}</signal:originDate>`,
        `<signal:heat>${post.data.heat}</signal:heat>`,
        `<signal:readMinutes>${post.data.readMinutes}</signal:readMinutes>`,
      ]
        .filter(Boolean)
        .join(''),
    })),
    customData: [
      '<language>en-us</language>',
      '<generator>signal.log curator</generator>',
    ].join(''),
  });
}

function escapeXml(value) {
  return String(value ?? '').replace(/[<>&'"]/g, (c) =>
    ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' })[c]
  );
}
