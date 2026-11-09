---
name: site-design-system
description: Design system and UI rules for roshan-kc.com.np (Roshan Kc's personal site and blog). Use before changing any page layout, CSS, component or visual element on this site, adding a new section or page, or reviewing how the site looks on desktop and mobile. Pairs with the frontend-design skill for taste; this skill holds the site's actual tokens, components and checks.
---

# roshan-kc.com.np design system

A calm, editorial personal site for a CTO. Content-first, fast, legible. The design's job is
to make long technical writing easy to read and make Roshan credible. It is not a landing page:
no hero animations, stock photos, gradients, shader effects or scroll-triggered reveals.

Load the `frontend-design` skill for general taste. Where it and this file disagree about this
site, this file wins: it describes decisions already made.

## Tokens (css/site.css `:root`)

| Token | Value | Use |
|---|---|---|
| `--ink` | #0b1220 | headings, strong text, dark surfaces (series feature, active chip, table heads) |
| `--ink-soft` | #243044 | body copy |
| `--mist` | #5c6b7e | meta, captions, secondary text |
| `--paper` | #fafbfc | page background |
| `--paper-deep` | #f0f2f5 | code backgrounds, subtle fills |
| `--line` | #e2e6ec | borders, dividers |
| `--sapphire` / `--sapphire-deep` | #1546e8 / #0f35b5 | links, focus, the only accent colour |
| `--radius` | 10px | cards and boxes; chips are pill-shaped |

Never add a second accent colour. White (`#fff`) is used for boxes sitting on `--paper`.

## Type

- **Atkinson Hyperlegible** (400/700, italics) for everything; self-hosted in `/fonts`.
- **JetBrains Mono** only for code and the small `.tag` labels. Ligatures are disabled in code
  (`|>` and `=>` must render as typed).
- Body copy in posts: 1.125rem / 1.75, max width 42rem (`.prose`). Do not widen it.
- Don't introduce new font families or load Google Fonts.

## Layout shell

- Desktop (≥1024px): fixed left sidebar (`.left-nav`, 20rem, 24rem at ≥1280px) + `.main-pane`.
  The sidebar can collapse to "full width reading" (`html[data-sidebar="collapsed"]`).
- Mobile: `.mobile-bar` at top, drawer menu, floating `.deck-dock` prev/next pill at the bottom.
- Posts: `.post-shell` grid = article + sticky `.post-toc` rail, only at ≥1400px.
- Every layout must work at 390, 768, 1024, 1280 and 1440px with no horizontal page scroll.
  Wide tables go inside `.table-scroll`.

## Components (reuse before inventing)

| Component | Where | Notes |
|---|---|---|
| `.blog-card` | blog index | list rows, top border, whole card clickable via `h2 a::after` |
| `.tag` | cards, post header | mono, small; written as "Topic · Subtopic" |
| `.prose` | post body | h2/h3 get ids + `.h-anchor` from `scripts/blog/enhance.py` |
| `.post-toc` | post right rail | built from h2s; active link via IntersectionObserver in `js/shell.js` |
| `.post-end` boxes | end of post | `.post-series`, `.post-author`, `.post-related` |
| `.series-feature` | blog index top | the one dark block on the page |
| `.topic-chip` | blog index | `aria-pressed`, filter state in `?topic=` |
| `.post-nav` | after article | previous/next |

The blog sidebar and mobile drawer links are synced from `NAV` in `scripts/blog/enhance.py` so
they always match the homepage. When a homepage section is added or renamed, update `NAV` too.

Blog pages are generated: `templates/post.html` and `templates/blog-index.html` hold the page
skeleton, `content/blog/` the posts, and `scripts/site/build.py` renders them. The TOC, series,
author, related and index-chip blocks come from `scripts/blog/enhance.py` (between
`<!--enh:...-->` markers). Change templates or scripts, never the generated HTML; `scripts/build.sh`
re-runs everything.

## Rules

1. One accent, one family, one radius. Spend boldness in at most one place per page.
2. Motion only answers an action (hover, focus, open). Respect `prefers-reduced-motion`.
3. Visible keyboard focus everywhere (`--focus` outline). Tap targets ≥ 40px.
4. Images: always `width`, `height`, `alt`, `loading="lazy"` below the fold; use the
   `profile-144/288/432/560.webp` sizes instead of the 75 KB `profile.webp` where possible.
5. No new JS frameworks or CDNs. Vanilla JS in `js/shell.js` (all pages) or `js/home.js`.
6. CSS lives in `css/site.css` (blog pages) and `css/home.css`; after editing run
   `cat css/utilities.css css/site.css css/home.css > css/app.css` (the homepage loads app.css),
   or `npm run build:css` when Tailwind classes changed.

## Headings and copy

- Section titles are plain and user-facing: "About me", "Values I hold", "Experience", "Top domains I’ve worked in",
  "Tech stack I’ve worked with", "Posts", "Get in touch". No clever or self-referential titles
  ("The CV, without the PDF", "Notes from the founder seat").
- No label above a title and no tagline under it. The title is followed directly by content.
- Card titles say what the thing is ("EV charging and sensor integrations"), not a mood
  ("Talking to chargers and sensors"). No numbered or category labels above them.
- Nav labels match the section titles.

## Check your work

1. `bash scripts/build.sh` then serve: `cd dist && python3 -m http.server 8765`.
2. Screenshot desktop with headless Chrome:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1440,1000 --virtual-time-budget=5000 --screenshot=out.png http://localhost:8765/blog/`
3. Mobile: headless Chrome won't go below ~500px wide, so wrap the page in a 390px iframe
   (`<iframe src="/blog/..." style="width:390px;height:3000px;border:0">` in a temp file in
   `dist/`), screenshot that, then delete the temp file.
4. Look at the screenshots before claiming a visual change works.
5. Run `python3 scripts/seo/audit.py --quiet`. It must report 0 FAIL.
