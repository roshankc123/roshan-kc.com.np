---
name: blog-post
description: Research, write and publish a blog post on roshan-kc.com.np in Roshan Kc's voice, with fact-checking, SEO metadata, schema, internal links and site registration. Use when asked to write, draft, add, update, re-date or rewrite a blog post or article on this site, or to plan blog topics.
---

# Writing a post for roshan-kc.com.np

Roshan Kc is Co-Founder and CTO of MarginTop Solutions (Kathmandu). Readers are engineers,
CTOs and founders. Posts must be accurate, first-hand where possible, and useful enough to rank.

## 1. Plan

- Name the search query the post targets (check Search Console exports if provided) and 2–4
  related queries. Put the main query in the title, h1, description and first paragraph.
- Check existing posts (`blog/*/index.html`, `content/blog/*.json`) to avoid overlap and to
  pick 3–6 internal links. If it belongs to the "Modern PHP in 2026" series, add its slug to
  `SERIES` in `scripts/blog/enhance.py`.

## 2. Research and fact-check (non-negotiable)

- Verify every version number, date, CVE, vote result, statistic and quote against a primary
  source (php.net, wiki.php.net/rfc, GitHub advisories, vendor docs). Use web search for
  anything after the model's training cutoff.
- When sources disagree, say so or leave it out. Never invent numbers, benchmarks or quotes.
- **Never invent first-hand claims** about Roshan or MarginTop (what "we" did, use, measured,
  felt). Use only what the user said or what's already on the site; otherwise ask, or write it
  as analysis. Flag any first-person line you weren't given.
- Credit and link sources, including people. Quote briefly and attribute; paraphrase the rest.
- No exploit details in security posts.

## 3. Write

Structure (match existing posts):
1. `<p><strong>Direct answer:</strong> …</p>`: answers the query in 2–3 sentences (featured
   snippets and AI answers quote this).
2. A short paragraph of context and why Roshan is writing it.
3. `<h2 id="…">` sections; tables for comparisons (plain `<table><thead><tr><th>` markup is
   styled automatically); `<pre><code>` for code with HTML-escaped `<`, `>`, `&`.
4. `<h2 id="takeaways">Key takeaways</h2>` with 4–5 bullets.
5. `<h2 id="sources">Sources</h2>` with outbound links.
6. Optional one-line call to action linking `/#contact`.

Voice: plain, direct, specific, first person where real. Sentence case headings. No hype, no
filler, no "in today's fast-paced world". Short paragraphs. Explain jargon once.

## 4. Metadata (content/blog/<slug>.json)

```json
{"slug": "kebab-case-with-main-keyword", "date": "YYYY-MM-DD", "read": 9,
 "tag": "PHP · Security", "title": "≤ 60 chars incl. ' | Roshan Kc'",
 "h1": "Full headline", "social": "og/twitter title", "short": "Short name",
 "desc": "140–160 chars, contains the main query, says what the reader gets",
 "keywords": "comma, separated", "prev": ["/blog/…/", "Title"], "next": ["/blog/…/", "Title"],
 "citations": [["Source name", "https://…"]]}
```

Dates: don't date a post before the events it describes. Keep `date` honest; use `modified`
when updating content later.

## 5. Publish

```bash
python3 scripts/blog/new_post.py content/blog/<slug>.json   # body: content/blog/<slug>.html
python3 scripts/seo/audit.py --quiet                         # must be 0 FAIL
bash scripts/build.sh
```

`new_post.py` builds the page from the site template (head, schema, breadcrumbs, nav), adds it
to the blog index, feed.xml, sitemap.xml, sitemap.html, llms.txt and the `BLOG_POSTS` list in
`js/shell.js` (newest first), then runs `enhance.py` (TOC, anchors, series, author, related).
Re-running with the same JSON regenerates the page in place.

If a post's date changes, the listings must be re-ordered by date (blog index cards, feed
items, sitemap entries, `BLOG_POSTS`) and prev/next links updated.

Then preview it (see the site-design-system skill for screenshots) and tell the user which
first-person lines and facts to double-check.
