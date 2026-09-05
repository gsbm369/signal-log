import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (await getCollection('posts')).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  return rss({
    title: 'signal.log',
    description: 'AI-curated technology briefing. Tech news, minus the noise.',
    site: context.site,
    trailingSlash: true,
    // Custom fields live in their own namespace so they cannot collide with
    // reserved RSS 2.0 elements (<source> in particular).
    xmlns: { signal: 'https://signal.log/ns#' },
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/posts/${post.id}/`,
      categories: post.data.tags,
      // Provenance for anything consuming this feed programmatically.
      customData: [
        `<signal:source>${escapeXml(post.data.source)}</signal:source>`,
        post.data.sourceUrl
          ? `<signal:originUrl>${escapeXml(post.data.sourceUrl)}</signal:originUrl>`
          : '',
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
