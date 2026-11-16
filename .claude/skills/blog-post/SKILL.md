---
name: blog-post
description: Research, write and publish a blog post on roshan-kc.com.np in Roshan Kc's voice, with fact-checking, SEO, AEO (answer engines) and GEO (generative/AI search) optimisation, human-sounding prose, FAQ schema, internal links and site registration. Use when asked to write, draft, add, update, re-date or rewrite a blog post or article on this site, or to plan blog topics.
---

# Writing a post for roshan-kc.com.np

Roshan Kc is Co-Founder and CTO of MarginTop Solutions (Kathmandu). Readers are engineers,
CTOs and founders. Posts must be accurate, first-hand where possible, and useful enough to rank
in Google and to be quoted by AI answer engines (ChatGPT, Perplexity, Google AI Overviews).

Quality beats volume. One post a reader bookmarks is worth five that restate the docs.

## 1. Plan

- Name the search query the post targets (check Search Console exports if provided) and 2–4
  related queries, including the questions people actually type ("is X production ready",
  "X vs Y", "what is X"). Put the main query in the title, h1, description and first paragraph.
- Decide the post's **one job**: explain, compare, decide or predict. A post that tries to do
  all four does none well. Clusters (a hub + spokes) beat one giant post.
- Check existing posts (`content/blog/*.json`) to avoid overlap and to pick 3–6 internal links.
  Link spokes to the hub and the hub to every spoke. If it belongs to the "Modern PHP in 2026"
  series, add its slug to `SERIES` in `scripts/blog/enhance.py`.
- When planning topics for the user, show the list (title, query, angle) and wait for approval.

## 2. Research and fact-check (non-negotiable)

- Verify every version number, date, CVE, vote result, statistic and quote against a primary
  source (php.net, wiki.php.net/rfc, GitHub repos and releases, vendor docs). Use web search for
  anything after the model's training cutoff.
- Trend summaries the user pastes are leads, not sources. Confirm each claim or drop it.
- Label vendor benchmarks as vendor benchmarks ("the project's own README reports…").
- When sources disagree, say so or leave it out. Never invent numbers, benchmarks or quotes.
- **Never invent first-hand claims** about Roshan or MarginTop (what "we" did, use, measured,
  felt). Use only what the user said or what's already on the site; otherwise ask, or write it
  as analysis. Flag any first-person line you weren't given.
- Credit and link sources, including people. Quote briefly and attribute; paraphrase the rest.
- No exploit details in security posts.

## 3. Write

Structure (match existing posts):
1. `<p><strong>Direct answer:</strong> …</p>`: answers the query in 2–3 sentences that make
   sense quoted on their own (featured snippets, AI Overviews and `speakable` schema use it).
2. A short paragraph of context: why Roshan is writing it and what the reader will leave with.
3. `<h2 id="…">` sections. Phrase many headings as the question a reader would ask
   ("Is elephc production ready?"). Open each section with a one-sentence answer, then the detail.
4. Tables for comparisons (plain `<table><thead><tr><th>` markup is styled automatically);
   `<pre><code>` for code with HTML-escaped `<`, `>`, `&`.
5. `<h2 id="takeaways">Key takeaways</h2>` with 4–5 bullets.
6. FAQ: put 3–5 real follow-up questions in the JSON `faq` field (see §4). The build inserts the
   FAQ section before Key takeaways and emits FAQPage schema. Don't repeat it in the body.
7. `<h2 id="sources">Sources</h2>` with outbound links.
8. Optional one-line call to action linking `/#contact`.

### AEO and GEO: write so machines can quote you accurately

- **Self-contained answers.** Every section's first sentence should survive being lifted out of
  context. Name the subject ("elephc compiles…"), not "it compiles…".
- **Entity clarity.** On first mention, say what a thing is, who makes it and the link:
  "elephc, an open-source PHP-to-native compiler from Illegal Studio (github.com/…)".
- **Facts with dates.** "As of November 2026, v0.27.8…". AI engines prefer dated, specific
  claims and drop vague ones.
- **Distinctive information.** Add something the docs don't: a decision rule, a comparison
  table, a failure mode, a "who should not use this". Original framing is what gets cited.
- **Definitions and lists.** A one-line definition and a short numbered decision list per post
  give answer engines clean extraction targets.
- **Consistent naming.** Use the product's own spelling (NativePHP, TypePHP, elephc) everywhere.
- `citations` in the JSON and the Sources section must match the links used in the body.

### Sound like a person, not a model

Roshan writes like an engineer talking to another engineer over tea: opinions, trade-offs, a
little dry humour, no performance.

- **Vary rhythm.** Mix short sentences with longer ones. A two-word sentence is fine. So is a
  one-sentence paragraph.
- **Have a view.** Say what you'd pick and why, and when you'd be wrong. Hedge once, honestly,
  not in every sentence.
- **Concrete over abstract.** A specific scenario ("a Laravel agency with one Flutter dev who
  just quit") beats "teams of all sizes".
- **Admit limits.** "I haven't shipped this in production" reads as more trustworthy than
  pretending.
- **Banned tells:** delve, landscape, tapestry, realm, game-changer, revolutionise, unlock,
  seamless, robust (as filler), leverage (as a verb), "it's worth noting", "in today's
  fast-paced world", "let's dive in", "in conclusion", "whether you're a… or a…", rhetorical
  question openers, triple-adjective lists, every paragraph ending in a neat moral.
- **Punctuation:** at most one em dash per few paragraphs; prefer commas, colons or full stops.
  No emoji. Sentence case headings.
- **Read it aloud test:** if a sentence would sound odd said to a colleague, rewrite it.

## 4. Metadata (content/blog/<slug>.json, body in content/blog/<slug>.html)

```json
{"slug": "kebab-case-with-main-keyword", "date": "YYYY-MM-DD", "read": 9,
 "tag": "PHP · Security", "title": "≤ 60 chars incl. ' | Roshan Kc'",
 "h1": "Full headline", "social": "og/twitter title", "short": "Short name",
 "desc": "140–160 chars, contains the main query, says what the reader gets",
 "keywords": "comma, separated",
 "citations": [["Source name", "https://…"]],
 "faq": [["Question in the reader's words?", "Plain-text answer, 1–3 sentences."]],
 "about": [{"@type": "SoftwareApplication", "name": "…", "url": "…"}]}
```

`faq` answers are plain text (no HTML) and must agree with the body. `about` names the main
entities for schema; use `SoftwareApplication` for tools.

Dates: don't date a post before the events it describes. Keep `date` honest; use `modified`
when updating content later.

## 5. Quality gate (check before publishing)

- [ ] Direct answer answers the query in ≤ 3 sentences and stands alone.
- [ ] Every number, version and date has a source in Sources.
- [ ] No unflagged first-person claims; no banned phrases.
- [ ] At least one table, decision list or original framing a competitor post lacks.
- [ ] 3–6 internal links, hub ↔ spokes connected, series updated.
- [ ] Title ≤ 60 chars, desc 140–160 chars, FAQ present.
- [ ] `audit.py` reports 0 FAIL.

## 6. Publish

```bash
python3 scripts/site/build.py          # builds every post + listing from content/ and templates/
python3 scripts/seo/audit.py --quiet   # must be 0 FAIL
bash scripts/build.sh                  # copies the public site into dist/
```

`build.py` renders each post from `templates/post.html`, sets previous/next by date, and
regenerates the blog index, feed.xml, the post entries of sitemap.xml, sitemap.html, llms.txt and
`BLOG_POSTS` in `js/shell.js` (newest first). It then runs `enhance.py` for the TOC, anchors,
series, author and related blocks. Never hand-edit `blog/*/index.html`: edit the content file or
the template and rebuild. Changing a post's `date` re-orders everything automatically.

After deploying, submit changed URLs to search engines with IndexNow (see the seo-audit skill).

Then preview it (see the site-design-system skill for screenshots) and tell the user which
first-person lines and facts to double-check.
