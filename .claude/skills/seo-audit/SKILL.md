---
name: seo-audit
description: Audit and improve SEO for roshan-kc.com.np, covering on-page tags, structured data, sitemaps, internal linking, redirects and Google Search Console analysis. Use when asked about SEO, rankings, clicks, CTR, impressions, Search Console exports, indexing, titles or descriptions, schema, sitemap, or "why isn't my page showing up" for this site.
---

# SEO for roshan-kc.com.np

Static HTML site on Cloudflare (Workers static assets / Pages), canonical host
`https://www.roshan-kc.com.np`, trailing-slash URLs (`/blog/<slug>/`).

## 1. Automated on-page audit

```bash
python3 scripts/seo/audit.py --quiet
```

It checks every page for title/description length, canonical, OG/Twitter tags, a single h1,
valid JSON-LD, image alt and dimensions, broken internal links and duplicate titles. It also
checks that every post appears in sitemap.xml, feed.xml, llms.txt, sitemap.html, the blog
index and `js/shell.js`. Fix every FAIL; fix WARNs unless there's a reason not to.

## 2. Search Console export analysis

When the user shares a Performance export folder (Queries.csv, Pages.csv, Countries.csv,
Devices.csv, Chart.csv):

1. **High impressions, ~0 clicks, position ≤ 10:** a CTR problem. Rewrite the title and
   description to match the exact query wording, and lead the description with the answer.
2. **Position 8–20 with impressions:** a ranking problem. Strengthen content for that query,
   add internal links from related posts, and earn external links (cross-posts with canonical
   links back, citations).
3. **Brand query ("roshan kc") below #1:** strengthen entity signals: Person schema `sameAs`,
   consistent name and links on LinkedIn, GitHub, Medium and X pointing back to the site.
4. **Duplicate URL variants in Pages.csv** (apex vs www, slash vs no slash, `#fragments`,
   old `/pdf/...`): fix with 301s in `_redirects` or Cloudflare Redirect Rules (host-level
   redirects such as apex → www can't be done in `_redirects`).

Report findings as numbers from the export, not impressions alone.

## 3. Rules for titles and descriptions

- Title ≤ 60 characters, including ` | Roshan Kc`. Main query first. No clickbait.
- Description 140–160 characters. It must contain the query and say what the reader gets.
- Every description lives in four places per post: meta description, og:description,
  twitter:description and JSON-LD `description`. Plus the card on `blog/index.html`, the
  `feed.xml` item and `content/blog/<slug>.json`. Change them together.
- Don't bump `dateModified` for metadata-only changes. Do bump it for real content updates.

## 4. Structured data in use

- Home: `WebSite`, `ProfilePage`, `Person` (with `sameAs`, `alternateName`,
  `disambiguatingDescription`), `Organization`, `FAQPage`.
- Posts: `BlogPosting` (author/publisher → `#person`, `citation`, `about` where useful) +
  `BreadcrumbList`.
- Validate after edits: the audit parses JSON-LD; for rich results use Google's Rich Results Test.

## 5. Technical checklist

- `_redirects`: legacy `.html` → slash URLs, old `/pdf/*` → `/cv/Roshan-Kc-CV.pdf`, slash-less
  posts → 301.
- `robots.txt` allows search and AI crawlers and points to the sitemap. `llms.txt` lists posts.
- Internal links: every post links to 3+ related posts. The enhancer also adds a series box and
  related posts automatically.
- After a deploy, request indexing for changed URLs in Search Console. Re-check CTR after 3–4 weeks.

## 6. IndexNow (Bing, Yandex, Seznam, Naver, Yep)

- Key file: `/cecf42ed10c14e03a85b4f593fb8aa9b.txt` at the site root (copied into dist by
  `scripts/build.sh`). The key is public by design.
- `npm run deploy` submits automatically after `wrangler deploy`; manually: `npm run indexnow`
  (new or changed URLs from sitemap.xml since the last run, tracked in the git-ignored
  `.indexnow-state.json`), `--all` for everything, `--dry-run` to preview, or pass URLs.
- It refuses to submit until the key file is live, so deploy first. Google ignores IndexNow:
  request indexing in Search Console for important pages.
