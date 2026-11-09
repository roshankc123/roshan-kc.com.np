#!/usr/bin/env python3
"""Add reading aids to every blog post and topic filters to the blog index.

Idempotent: every block it writes is wrapped in <!--enh:...--> markers and is
stripped and rebuilt on each run. Run from anywhere:

    python3 scripts/blog/enhance.py

Per post: heading ids + anchor links, a sticky table of contents (wide screens),
a series box (for posts in SERIES), an author box and three related posts.
Blog index: data-topics on every card, topic filter chips and a series feature.
"""
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOG = ROOT / "blog"
E = lambda s: html.escape(s, quote=True)

SERIES_NAME = "Modern PHP in 2026"
SERIES_HUB = "php-in-2026-why-you-should-revisit-php"
# Reading order for the series box.
SERIES = [
    "php-in-2026-why-you-should-revisit-php",
    "php-8-6-new-features",
    "php-8-5-features-production",
    "php-8-4-property-hooks-asymmetric-visibility",
    "php-type-system-evolution",
    "php-runtimes-fpm-octane-frankenphp-swoole-roadrunner",
    "php-async-fibers-coroutines",
    "what-typephp-means-for-php-performance",
    "php2shell-how-php-contained-critical-rce",
    "php-runtime-vulnerabilities-history",
    "upgrade-php-7-to-php-8-5-playbook",
    "choose-tech-stack-ai-era-patch-velocity",
]

# Tag word -> filter topic on the blog index.
TOPIC_OF = {
    "php": "php", "modern php": "php", "releases": "php", "language": "php", "async": "php", "upgrades": "php",
    "laravel": "laravel",
    "security": "security",
    "performance": "performance", "docker": "performance",
    "engineering": "engineering", "principles": "engineering", "architecture": "engineering", "ai": "engineering",
    "stack": "engineering", "strategy": "engineering", "product": "engineering", "cloud": "engineering",
    "cto": "leadership", "hiring": "leadership", "team": "leadership", "founder": "leadership",
    "leadership": "leadership", "delivery": "leadership", "hustle": "leadership", "startups": "leadership",
    "kathmandu": "leadership", "nepal": "leadership",
}
TOPICS = [("php", "PHP"), ("laravel", "Laravel"), ("security", "Security"), ("performance", "Performance"),
          ("engineering", "Engineering"), ("leadership", "Leadership & founding")]

# Topics that are close enough to recommend across.
NEAR = {
    "php": ("laravel", "performance"), "laravel": ("php", "performance"), "performance": ("php", "laravel"),
    "security": ("engineering", "php"), "engineering": ("leadership", "security"), "leadership": ("engineering",),
}

STOP = set("a an the and or of for to in on with how why what we our your is are it its not vs from at by you i my "
           "that this php".split())


# Sidebar + drawer navigation, kept identical to the homepage (index.html).
NAV = [("/#home", "Presence"), ("/#about", "The Story"), ("/#focus", "Focus"), ("/#experience", "Experience"),
       ("/#work", "Work"), ("/#stack", "Stack"), ("/blog/", "Blog"), ("/#contact", "Connect")]


def sync_nav(s):
    desk = "\n".join(
        f'                    <li><a href="{h}"{" aria-current=\"page\"" if h == "/blog/" else ""}>'
        f'<span class="nav-rule" aria-hidden="true"></span>{t}</a></li>' for h, t in NAV)
    mob = "\n".join(
        f'                    <li><a href="{h}"><span class="visually-hidden">Mobile nav: </span>{t}</a></li>' for h, t in NAV)
    s = re.sub(r'(<ul class="nav-list" id="desktop-nav-links">).*?(\s*</ul>)', lambda m: m.group(1) + "\n" + desk + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<ul id="mobile-nav-links" class="mobile-nav-list">).*?(\s*</ul>)', lambda m: m.group(1) + "\n" + mob + m.group(2), s, count=1, flags=re.S)
    return s.replace("Cofounder &amp; CTO, MarginTop Solutions", "Co-Founder and CTO, MarginTop Solutions")


def strip_blocks(s):
    # eat the whitespace each block was inserted with, so repeated runs are byte-identical
    s = re.sub(r"\n*<!--enh:(\w+):start-->.*?<!--enh:\1:end-->\n?", "", s, flags=re.S)
    s = s.replace('<!--enh:shell-open--><div class="post-shell">', "")
    s = s.replace("</div><!--enh:shell-close-->", "")
    s = re.sub(r'<a class="h-anchor"[^>]*>#</a>', "", s)
    return s


def slugify(text):
    t = re.sub(r"<[^>]+>", "", text)
    t = html.unescape(t).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60] or "section"


def topics_for(tag):
    out = []
    for part in [p.strip().lower() for p in html.unescape(tag).split("·")]:
        t = TOPIC_OF.get(part)
        if t and t not in out:
            out.append(t)
    return out


def read_posts():
    posts = {}
    for d in sorted(BLOG.iterdir()):
        f = d / "index.html"
        if not d.is_dir() or not f.exists():
            continue
        s = f.read_text(encoding="utf-8")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        date = re.search(r'<time datetime="([^"]+)">([^<]+)</time>', s)
        tag = re.search(r'<span class="tag">([^<]*)</span>', s)
        if not (h1 and date and tag):
            continue
        title = html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip()
        posts[d.name] = {
            "slug": d.name, "file": f, "title": title, "date": date.group(1), "date_h": date.group(2),
            "tag": html.unescape(tag.group(1)), "topics": topics_for(tag.group(1)),
            "words": {w for w in re.findall(r"[a-z0-9.+#]+", title.lower()) if w not in STOP and len(w) > 2},
        }
    return posts


def related(cur, posts, exclude):
    scored = []
    for p in posts.values():
        if p["slug"] == cur["slug"] or p["slug"] in exclude:
            continue
        near = {t for c in cur["topics"] for t in NEAR.get(c, ())}
        score = (3 * len(set(cur["topics"]) & set(p["topics"])) + len(near & set(p["topics"]))
                 + len(cur["words"] & p["words"]))
        scored.append((score, p["date"], p))  # score 0 still works as a recency fallback
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [p for _, _, p in scored[:3]]


def toc_block(items):
    lis = "\n".join(f'          <li><a href="#{i}">{E(t)}</a></li>' for i, t in items)
    return f'''<!--enh:aside:start--><aside class="post-toc" aria-label="On this page">
        <p class="post-toc__title">On this page</p>
        <ol>
{lis}
        </ol>
        <a class="post-toc__top" href="#main-content">Back to top</a>
      </aside><!--enh:aside:end-->'''


def series_block(cur, posts):
    rows = []
    for n, slug in enumerate([s for s in SERIES if s in posts], 1):
        p = posts[slug]
        if slug == cur["slug"]:
            rows.append(f'            <li aria-current="page"><span>{E(p["title"])}</span></li>')
        else:
            rows.append(f'            <li><a href="/blog/{slug}/">{E(p["title"])}</a></li>')
    return f'''          <section class="post-series" aria-labelledby="series-title">
            <p class="post-series__label" id="series-title">Part of the series <a href="/blog/{SERIES_HUB}/">{E(SERIES_NAME)}</a></p>
            <ol>
{chr(10).join(rows)}
            </ol>
          </section>'''


AUTHOR = '''          <section class="post-author" aria-label="About the author">
            <img src="/images/profile-144.webp" width="72" height="72" alt="Portrait of Roshan Kc" loading="lazy" decoding="async">
            <div>
              <p class="post-author__name">Written by <a href="/#about">Roshan Kc</a></p>
              <p class="post-author__bio">Co-Founder and CTO of <a href="https://www.margintopsolutions.com/" target="_blank" rel="noopener noreferrer">MarginTop Solutions</a> in Kathmandu. Computer engineer building device-connected and enterprise software: IoT, robotics, multi-tenant SaaS and the PHP and Laravel systems behind them.</p>
              <p class="post-author__links"><a href="https://www.linkedin.com/in/roshan-kc-12892b25a" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://github.com/roshankc123" target="_blank" rel="noopener noreferrer">GitHub</a><a href="/#contact">Get in touch</a></p>
            </div>
          </section>'''


def related_block(items):
    if not items:
        return ""
    lis = "\n".join(
        f'            <li><a href="/blog/{p["slug"]}/">{E(p["title"])}</a><time datetime="{p["date"]}">{E(p["date_h"])}</time></li>'
        for p in items)
    return f'''          <section class="post-related" aria-labelledby="related-title">
            <p class="post-related__label" id="related-title">Keep reading</p>
            <ul>
{lis}
            </ul>
          </section>'''


def enhance_post(cur, posts):
    s = strip_blocks(cur["file"].read_text(encoding="utf-8"))
    a0 = s.index('<article class="prose">')
    a1 = s.index("</article>", a0)
    art = s[a0:a1]

    # Heading ids + anchors (h2 and h3 inside the article body).
    seen, toc = set(), []

    def fix(m):
        lvl, attrs, inner = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'\bid="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slugify(inner)
        base, k = hid, 2
        while hid in seen:
            hid, k = f"{base}-{k}", k + 1
        seen.add(hid)
        if not idm:
            attrs = f' id="{hid}"' + attrs
        if lvl == "2":
            toc.append((hid, html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()))
        return f'<h{lvl}{attrs}>{inner}<a class="h-anchor" href="#{hid}" aria-label="Link to this section">#</a></h{lvl}>'

    art = re.sub(r"<h([23])((?:\s[^>]*)?)>(.*?)</h\1>", fix, art, flags=re.S)

    in_series = cur["slug"] in SERIES
    end = [series_block(cur, posts)] if in_series else []
    end.append(AUTHOR)
    end.append(related_block(related(cur, posts, set(SERIES) if in_series else set())))
    end_html = "\n<!--enh:end:start--><footer class=\"post-end\">\n" + "\n".join(x for x in end if x) + "\n        </footer><!--enh:end:end-->\n"

    aside = toc_block(toc) if len(toc) >= 3 else ""
    s = (s[:a0] + '<!--enh:shell-open--><div class="post-shell">' + art + end_html + "</article>"
         + aside + "</div><!--enh:shell-close-->" + s[a1 + len("</article>"):])
    cur["file"].write_text(sync_nav(s), encoding="utf-8")


def enhance_index(posts):
    f = BLOG / "index.html"
    s = strip_blocks(f.read_text(encoding="utf-8"))
    s = re.sub(r'<article class="blog-card"(?: data-topics="[^"]*")?>', '<article class="blog-card">', s)

    def card(m):
        block = m.group(0)
        slug = re.search(r'href="/blog/([^/"]+)/"', block)
        p = posts.get(slug.group(1)) if slug else None
        topics = " ".join(p["topics"]) if p else ""
        return block.replace('<article class="blog-card">', f'<article class="blog-card" data-topics="{topics}">', 1)

    s = re.sub(r'<article class="blog-card">.*?</article>', card, s, flags=re.S)

    counts = {k: sum(k in p["topics"] for p in posts.values()) for k, _ in TOPICS}
    chips = "\n".join(
        f'            <button type="button" class="topic-chip" data-topic="{k}" aria-pressed="false">{E(label)} <span>{counts[k]}</span></button>'
        for k, label in TOPICS if counts[k])
    hub = posts.get(SERIES_HUB)
    n_series = sum(s_ in posts for s_ in SERIES)
    feature = f'''<!--enh:index:start-->
        <section class="series-feature" aria-labelledby="series-feature-title">
          <p class="series-feature__kicker">A {n_series}-part series</p>
          <h2 id="series-feature-title"><a href="/blog/{SERIES_HUB}/">{E(SERIES_NAME)}</a></h2>
          <p>{E("Where PHP actually stands today: the new releases, the type system, runtimes and async, how the PHP team handled PHP2Shell, and how to upgrade safely.")}</p>
          <a class="series-feature__cta" href="/blog/{SERIES_HUB}/">Start with {E(hub["title"]) if hub else "the overview"}</a>
        </section>
        <nav class="topic-filter" aria-label="Filter posts by topic" hidden>
          <div class="topic-filter__chips">
            <button type="button" class="topic-chip" data-topic="all" aria-pressed="true">All <span>{len(posts)}</span></button>
{chips}
          </div>
          <p class="topic-filter__status" aria-live="polite"></p>
        </nav>
<!--enh:index:end-->'''
    anchor = '        <div>\n          <article class="blog-card"'
    assert anchor in s, "blog index anchor not found"
    s = s.replace(anchor, feature + "\n" + anchor, 1)
    f.write_text(sync_nav(s), encoding="utf-8")


def main():
    posts = read_posts()
    for p in posts.values():
        enhance_post(p, posts)
    enhance_index(posts)
    print(f"enhanced {len(posts)} posts + blog index")


if __name__ == "__main__":
    main()
