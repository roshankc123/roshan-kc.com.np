#!/usr/bin/env python3
"""Build every blog page and listing from content/blog/ + templates/.

    python3 scripts/site/build.py

Sources
  content/blog/<slug>.json   metadata (see below)
  content/blog/<slug>.html   article body (no header/h1); plain <table><thead><tr><th>
                             markup is styled automatically
  templates/post.html        page skeleton for a post
  templates/blog-index.html  page skeleton for /blog/

Writes (all committed, so any static host can serve the repo root)
  blog/<slug>/index.html, blog/index.html, feed.xml, the post entries of
  sitemap.xml, sitemap.html and llms.txt, and BLOG_POSTS in js/shell.js.
  Then runs scripts/blog/enhance.py (TOC, anchors, series, author, related, nav).

post.json keys
  slug, date (YYYY-MM-DD), read (minutes), tag ("PHP · Security"),
  title (<title>, <= 60 chars incl. " | Roshan Kc"), h1, social (og/twitter title),
  short (sitemap/llms name), desc (140-160 chars), keywords
  optional: modified (YYYY-MM-DD), citations [[name, url]], about [schema objects]

Previous/next links follow the date order (newest first); the ends point at /blog/.
"""
import datetime
import html
import json
import re
import subprocess
import sys
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://www.roshan-kc.com.np"
CONTENT = ROOT / "content/blog"
E = lambda s: html.escape(str(s), quote=True)


def human(d):
    return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")


def style_tables(b):
    """Style plain <table> markup; already-styled tables are left alone."""
    def one(mt):
        t = mt.group(1)
        t = t.replace("<thead><tr>", '<thead>\n    <tr style="background:var(--ink);color:var(--paper)">')
        t = t.replace("<th>", '<th style="padding:0.6rem 0.9rem;text-align:left">')
        head, rest = t.split("<tbody>")
        rows, tail = rest.split("</tbody>")
        out, i = [], 0
        for r in re.split(r"(?=<tr>)", rows):
            if r.startswith("<tr>"):
                st = "border-bottom:1px solid var(--rule)" + (";background:var(--wash)" if i % 2 else "")
                i += 1
                r = r.replace("<tr>", f'<tr style="{st}">', 1)
            out.append(r)
        t = (head + "<tbody>" + "".join(out) + "</tbody>" + tail).replace("<td>", '<td style="padding:0.6rem 0.9rem">')
        return ('<div class="table-scroll"><table style="width:100%;border-collapse:collapse;margin:1.5rem 0;'
                'font-size:0.92rem">' + t + "</table></div>")
    return re.sub(r"<table>(.*?)</table>", one, b, flags=re.S)


def render(tpl, values):
    def rep(m):
        k = m.group(1)
        if k not in values:
            raise KeyError(f"template placeholder {{{{{k}}}}} has no value")
        return str(values[k])
    return re.sub(r"\{\{(\w+)\}\}", rep, tpl)


def load_posts():
    posts = []
    for j in sorted(CONTENT.glob("*.json")):
        m = json.loads(j.read_text(encoding="utf-8"))
        if m["slug"] != j.stem:
            sys.exit(f"{j.name}: slug {m['slug']!r} does not match the file name")
        m["body"] = j.with_suffix(".html").read_text(encoding="utf-8")
        m.setdefault("modified", m["date"])
        m["url"] = f"{SITE}/blog/{m['slug']}/"
        posts.append(m)
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def jsonld(m):
    person = {"@type": "Person", "name": "Roshan Kc", "url": f"{SITE}/", "@id": f"{SITE}/#person"}
    post = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": m["h1"], "description": m["desc"],
            "image": f"{SITE}/images/profile.webp", "datePublished": m["date"], "dateModified": m["modified"],
            "author": dict(person, jobTitle="Cofounder & CTO"), "publisher": person,
            "mainEntityOfPage": {"@type": "WebPage", "@id": m["url"]}, "keywords": m["keywords"], "inLanguage": "en",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".prose p:first-of-type"]},
            "isPartOf": {"@type": "Blog", "name": "Notes by Roshan Kc", "url": f"{SITE}/blog/"}}
    if m.get("about"):
        post["about"] = m["about"]
    if m.get("citations"):
        post["citation"] = [{"@type": "CreativeWork", "name": n, "url": u} for n, u in m["citations"]]
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
        {"@type": "ListItem", "position": 3, "name": m["h1"], "item": m["url"]}]}
    dump = lambda o: json.dumps(o, indent=2, ensure_ascii=False).replace("</", "<\\/")
    return (f'<script type="application/ld+json">\n{dump(post)}\n  </script>\n'
            f'  <script type="application/ld+json">\n{dump(crumbs)}\n  </script>')


def post_nav(prev, nxt):
    def link(cls, label, p):
        href, title = (f"/blog/{p['slug']}/", p.get("short") or p["h1"]) if p else ("/blog/", "All notes")
        return f'''          <div class="post-nav__link post-nav__{cls}">
            <span class="font-mono-label" style="color:var(--sapphire)">{label}</span>
            <a class="post-nav__title" href="{href}">{E(title)}</a>
          </div>'''
    return ('<nav class="post-nav" aria-label="Post navigation">\n' + link("prev", "Previous", prev) + "\n"
            + link("next", "Next", nxt) + "\n        </nav>")


def build_posts(posts):
    tpl = (ROOT / "templates/post.html").read_text(encoding="utf-8")
    for i, m in enumerate(posts):
        page = render(tpl, {
            "title": E(m["title"]), "desc": E(m["desc"]), "social": E(m.get("social", m["h1"])),
            "url": m["url"], "date": m["date"], "modified": m["modified"], "date_human": human(m["date"]),
            "tag": E(m["tag"]), "read": m["read"], "h1": E(m["h1"]), "body": style_tables(m["body"]).rstrip() + "\n",
            "jsonld": jsonld(m), "total": len(posts),
            "post_nav": post_nav(posts[i - 1] if i > 0 else None, posts[i + 1] if i + 1 < len(posts) else None),
        })
        out = ROOT / "blog" / m["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page, encoding="utf-8")


def build_index(posts):
    cards = "\n\n          ".join(f'''<article class="blog-card">
            <div class="blog-meta">
              <span class="tag">{E(m["tag"])}</span>
              <time datetime="{m["date"]}">{human(m["date"])}</time>
              <span>{m["read"]} min read</span>
            </div>
            <h2 class="font-display" style="margin:0 0 0.5rem;font-size:clamp(1.35rem,3vw,1.85rem);color:var(--ink);line-height:1.2"><a href="/blog/{m["slug"]}/">{E(m["h1"])}</a></h2>
            <p style="margin:0;color:var(--mist);font-size:1.05rem;max-width:40rem">{E(m["desc"])}</p>
          </article>''' for m in posts)
    tpl = (ROOT / "templates/blog-index.html").read_text(encoding="utf-8")
    (ROOT / "blog/index.html").write_text(render(tpl, {"cards": cards, "total": len(posts) + 1}), encoding="utf-8")


def rfc822(d):
    return format_datetime(datetime.datetime.fromisoformat(d).replace(tzinfo=datetime.timezone.utc))


def build_feed(posts):
    p = ROOT / "feed.xml"
    s = p.read_text(encoding="utf-8")
    head = s[:s.index("    <item>")]
    head = re.sub(r"<lastBuildDate>[^<]*</lastBuildDate>", f"<lastBuildDate>{rfc822(max(m['modified'] for m in posts))}</lastBuildDate>", head)
    items = "".join(f'''    <item>
      <title>{E(m["h1"])}</title>
      <link>{m["url"]}</link>
      <guid isPermaLink="true">{m["url"]}</guid>
      <pubDate>{rfc822(m["date"])}</pubDate>
      <description>{E(m["desc"])}</description>
      <author>kcroshan566@gmail.com (Roshan Kc)</author>
    </item>
''' for m in posts)
    p.write_text(head + items + "  </channel>\n</rss>\n", encoding="utf-8")


def build_sitemaps(posts):
    p = ROOT / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"\s*<url>\s*<loc>" + re.escape(SITE) + r"/blog/[^<]+/</loc>.*?</url>", "", s, flags=re.S)
    entries = "".join(f"    <url>\n        <loc>{m['url']}</loc>\n        <lastmod>{m['modified']}</lastmod>\n"
                      "        <changefreq>monthly</changefreq>\n        <priority>0.8</priority>\n    </url>\n" for m in posts)
    s = s.replace("</urlset>", entries + "</urlset>")
    s = re.sub(r"(<loc>" + re.escape(SITE) + r"/blog/</loc>\s*<lastmod>)[^<]+", lambda x: x.group(1) + posts[0]["date"], s)
    p.write_text(s, encoding="utf-8")

    p = ROOT / "sitemap.html"
    s = p.read_text(encoding="utf-8")
    lis = "".join(f'      <li><a href="/blog/{m["slug"]}/">{E(m.get("short") or m["h1"])}</a></li>\n' for m in posts)
    s = re.sub(r"(<h2>Blog posts</h2>\s*<ul>\n).*?(\s*</ul>)", lambda x: x.group(1) + lis.rstrip("\n") + x.group(2), s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")

    p = ROOT / "llms.txt"
    s = p.read_text(encoding="utf-8")
    anchor = f"Founder and CTO notes: {SITE}/blog/\n\n"
    lines = "".join(f"- {m.get('short') or m['h1']}: {m['url']}\n" for m in posts)
    s = re.sub(re.escape(anchor) + r"(?:- [^\n]*\n)*", lambda _: anchor + lines, s, count=1)
    p.write_text(s, encoding="utf-8")

    p = ROOT / "js/shell.js"
    s = p.read_text(encoding="utf-8")
    arr = ",\n".join(f'    "/blog/{m["slug"]}/"' for m in posts)
    s = re.sub(r"const BLOG_POSTS = \[.*?\];", lambda _: f"const BLOG_POSTS = [\n{arr}\n  ];", s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")


def main():
    posts = load_posts()
    build_posts(posts)
    build_index(posts)
    build_feed(posts)
    build_sitemaps(posts)
    subprocess.run([sys.executable, "-I", str(ROOT / "scripts/blog/enhance.py")], check=True)
    print(f"built {len(posts)} posts, blog index, feed, sitemaps, llms.txt, BLOG_POSTS")


if __name__ == "__main__":
    main()
