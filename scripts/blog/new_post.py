#!/usr/bin/env python3
"""Create (or regenerate) a blog post from a JSON meta file + an HTML body file.

    python3 scripts/blog/new_post.py path/to/post.json     # body = path/to/post.html

post.json keys:
  slug, date (YYYY-MM-DD), read (minutes), tag ("PHP · Security"),
  title (<title>, ~50-60 chars, ends " | Roshan Kc"), h1, social (og/twitter title),
  short (short name for sitemap/llms), desc (meta description, 140-160 chars),
  keywords, prev/next ([href, title], optional), citations ([[name, url], ...], optional),
  about (schema.org objects, optional), modified (YYYY-MM-DD, optional)

The body is plain article HTML (no header/h1). Plain <table><thead><tr><th>…
markup is styled automatically. Re-running with the same slug rewrites the
page in place; site listings are only added once. Afterwards it runs
enhance.py so TOC, series, author and related blocks are rebuilt everywhere.
"""
import datetime
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from enhance import strip_blocks  # noqa: E402

TEMPLATE = ROOT / "blog/what-typephp-means-for-php-performance/index.html"
TEMPLATE_URL = "https://www.roshan-kc.com.np/blog/what-typephp-means-for-php-performance/"
SITE = "https://www.roshan-kc.com.np"
E = lambda x: html.escape(x, quote=True)


def style_tables(b):
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


def jsonld(o):
    return ('<script type="application/ld+json">\n'
            + json.dumps(o, indent=2, ensure_ascii=False).replace("</", "<\\/") + "\n  </script>\n  ")


def build_page(m, body):
    S, D, H1, DESC = m["slug"], m["date"], m["h1"], m["desc"]
    U = f"{SITE}/blog/{S}/"
    human = datetime.date.fromisoformat(D).strftime("%B %-d, %Y")
    tpl = strip_blocks(TEMPLATE.read_text(encoding="utf-8"))
    head = tpl[:tpl.index('<script type="application/ld+json">')]
    head = re.sub(r"<title>.*?</title>", lambda _: f"<title>{E(m['title'])}</title>", head, count=1)
    for attr, val in [('name="description"', DESC), ('property="og:description"', DESC),
                      ('name="twitter:description"', DESC), ('property="og:title"', m.get("social", H1)),
                      ('name="twitter:title"', m.get("social", H1))]:
        head = re.sub(r"(" + attr + r' content=")[^"]*', lambda x, v=val: x.group(1) + E(v), head, count=1)
    head = head.replace(TEMPLATE_URL, U)
    head = re.sub(r'(article:(published|modified)_time" content=")[^"]*', lambda x: x.group(1) + m.get("modified", D) if "modified" in x.group(2) else x.group(1) + D, head)
    person = {"@type": "Person", "name": "Roshan Kc", "url": f"{SITE}/", "@id": f"{SITE}/#person"}
    post = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": H1, "description": DESC,
            "image": f"{SITE}/images/profile.webp", "datePublished": D, "dateModified": m.get("modified", D),
            "author": dict(person, jobTitle="Cofounder & CTO"), "publisher": person,
            "mainEntityOfPage": {"@type": "WebPage", "@id": U}, "keywords": m["keywords"], "inLanguage": "en",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".prose p:first-of-type"]},
            "isPartOf": {"@type": "Blog", "name": "Notes by Roshan Kc", "url": f"{SITE}/blog/"}}
    if m.get("about"):
        post["about"] = m["about"]
    if m.get("citations"):
        post["citation"] = [{"@type": "CreativeWork", "name": n, "url": u} for n, u in m["citations"]]
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
        {"@type": "ListItem", "position": 3, "name": H1, "item": U}]}
    head += jsonld(post) + jsonld(crumbs).rstrip() + "\n</head>"

    rest = tpl[tpl.index("</head>") + 7:]
    a0, a1 = rest.index('<header style="margin-bottom:2rem">'), rest.index("</article>")
    rest = rest[:a0] + f'''<header style="margin-bottom:2rem">
            <div class="blog-meta">
              <span class="tag">{E(m["tag"])}</span>
              <time datetime="{D}">{human}</time>
              <span>{m["read"]} min read</span>
            </div>
            <h1 class="font-display" style="font-size:clamp(1.9rem,4.5vw,2.85rem);color:var(--ink);margin:0 0 1rem;line-height:1.15">{E(H1)}</h1>
          </header>

{style_tables(body)}
''' + rest[a1:]
    if m.get("prev") and m.get("next"):
        n0 = rest.index('<nav class="post-nav"')
        n1 = rest.index("</nav>", n0) + 6
        (ph, pt), (nh, nt) = m["prev"], m["next"]
        rest = rest[:n0] + f'''<nav class="post-nav" aria-label="Post navigation">
          <div class="post-nav__link post-nav__prev">
            <span class="font-mono-label" style="color:var(--sapphire)">Previous</span>
            <a class="post-nav__title" href="{ph}">{E(pt)}</a>
          </div>
          <div class="post-nav__link post-nav__next">
            <span class="font-mono-label" style="color:var(--sapphire)">Next</span>
            <a class="post-nav__title" href="{nh}">{E(nt)}</a>
          </div>
        </nav>''' + rest[n1:]
    return head + rest, human


def insert_once(path, slug, after, text):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    if f"/blog/{slug}/" in s:
        return
    i = s.index(after) + len(after) if isinstance(after, str) else after(s)
    p.write_text(s[:i] + text + s[i:], encoding="utf-8")


def register(m, human):
    S, U = m["slug"], f"{SITE}/blog/{m['slug']}/"
    insert_once("js/shell.js", S, "const BLOG_POSTS = [\n", f'    "/blog/{S}/",\n')
    insert_once("blog/index.html", S, lambda s: s.index('<article class="blog-card"'), f'''<article class="blog-card">
            <div class="blog-meta">
              <span class="tag">{E(m["tag"])}</span>
              <time datetime="{m["date"]}">{human}</time>
              <span>{m["read"]} min read</span>
            </div>
            <h2 class="font-display" style="margin:0 0 0.5rem;font-size:clamp(1.35rem,3vw,1.85rem);color:var(--ink);line-height:1.2"><a href="/blog/{S}/">{E(m["h1"])}</a></h2>
            <p style="margin:0;color:var(--mist);font-size:1.05rem;max-width:40rem">{E(m["desc"])}</p>
          </article>

          ''')
    insert_once("feed.xml", S, lambda s: s.index("    <item>"), f'''    <item>
      <title>{E(m["h1"])}</title>
      <link>{U}</link>
      <guid isPermaLink="true">{U}</guid>
      <pubDate>{m["date"]}</pubDate>
      <description>{E(m["desc"])}</description>
      <author>kcroshan566@gmail.com (Roshan Kc)</author>
    </item>

''')
    insert_once("sitemap.xml", S, lambda s: s.rindex("    <url>", 0, s.index(f"<loc>{SITE}/blog/", s.index(f"<loc>{SITE}/blog/</loc>") + 1)),
                f"    <url>\n        <loc>{U}</loc>\n        <lastmod>{m['date']}</lastmod>\n"
                "        <changefreq>monthly</changefreq>\n        <priority>0.8</priority>\n    </url>\n")
    insert_once("sitemap.html", S, "<h2>Blog posts</h2>\n    <ul>\n",
                f'      <li><a href="/blog/{S}/">{E(m.get("short", m["h1"]))}</a></li>\n')
    insert_once("llms.txt", S, f"Founder and CTO notes: {SITE}/blog/\n\n", f"- {m.get('short', m['h1'])}: {U}\n")


def main():
    meta = Path(sys.argv[1]).resolve()
    m = json.loads(meta.read_text(encoding="utf-8"))
    body = meta.with_suffix(".html").read_text(encoding="utf-8")
    page, human = build_page(m, body)
    out = ROOT / "blog" / m["slug"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    register(m, human)
    subprocess.run([sys.executable, "-I", str(Path(__file__).parent / "enhance.py")], check=True)
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    print(f"{m['slug']}: {words} words | title {len(m['title'])} chars | description {len(m['desc'])} chars")


if __name__ == "__main__":
    main()
