#!/usr/bin/env python3
"""On-page SEO audit for the static site. Exit code 1 if any FAIL.

    python3 scripts/seo/audit.py            # full report
    python3 scripts/seo/audit.py --quiet    # only problems

Checks every public HTML page (home, blog index, posts, sitemap.html, 404):
title/description length, canonical, Open Graph + Twitter tags, one <h1>,
JSON-LD validity, image alt/size attributes, internal links, duplicate
titles/descriptions. Then checks that every post is listed in sitemap.xml,
feed.xml, llms.txt, sitemap.html, the blog index and js/shell.js.
"""
import json
import re
import sys
import xml.dom.minidom
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://www.roshan-kc.com.np"
QUIET = "--quiet" in sys.argv
problems = {"FAIL": 0, "WARN": 0}


def report(level, page, msg):
    problems[level] += 1
    print(f"  {level:4} {page}: {msg}")


def meta(s, attr, name):
    m = re.search(rf'<meta {attr}="{re.escape(name)}"\s+content="([^"]*)"', s)
    return m.group(1) if m else None


def pages():
    yield ROOT / "index.html", "/"
    yield ROOT / "blog/index.html", "/blog/"
    yield ROOT / "sitemap.html", "/sitemap"
    yield ROOT / "404.html", None
    for f in sorted((ROOT / "blog").glob("*/index.html")):
        yield f, f"/blog/{f.parent.name}/"


def exists(href):
    path = href.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return True
    p = ROOT / path.lstrip("/")
    return p.exists() or (p / "index.html").exists() or p.with_suffix(".html").exists()


def audit_page(f, path, seen_titles, seen_desc):
    s = f.read_text(encoding="utf-8")
    name = str(f.relative_to(ROOT))
    title = re.search(r"<title>(.*?)</title>", s, re.S)
    desc = meta(s, "name", "description")
    if not title:
        report("FAIL", name, "missing <title>")
    else:
        t = title.group(1).strip()
        seen_titles[t].append(name)
        if path not in (None, "/sitemap") and not 30 <= len(t) <= 68:
            report("WARN", name, f"title is {len(t)} chars (aim 50-65): {t}")
    if path is None:  # 404 page: should not be indexed, nothing else matters
        if "noindex" not in s:
            report("WARN", name, "404 page should have <meta name=\"robots\" content=\"noindex\">")
        return
    if not desc:
        report("FAIL", name, "missing meta description")
    else:
        seen_desc[desc].append(name)
        if not 70 <= len(desc) <= 170:
            report("WARN", name, f"description is {len(desc)} chars (aim 140-160)")
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not canon:
        report("FAIL", name, "missing canonical")
    elif canon.group(1) != SITE + path:
        report("WARN", name, f"canonical {canon.group(1)} != {SITE + path}")
    social = [] if path == "/sitemap" else [("property", "og:title"), ("property", "og:description"), ("property", "og:image"),
                      ("property", "og:url"), ("name", "twitter:card")]
    for attr, key in social:
        if not meta(s, attr, key):
            report("WARN", name, f"missing {key}")
    if 'name="robots" content="noindex' in s:
        report("FAIL", name, "page is noindex")
    h1 = len(re.findall(r"<h1[\s>]", s))
    if h1 != 1:
        report("FAIL" if h1 == 0 else "WARN", name, f"{h1} <h1> elements")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            report("FAIL", name, f"invalid JSON-LD: {e}")
    for img in re.findall(r"<img\b[^>]*>", s):
        if "alt=" not in img:
            report("WARN", name, f"image without alt: {img[:80]}")
        if "width=" not in img or "height=" not in img:
            report("WARN", name, f"image without width/height (layout shift): {img[:80]}")
    for href in set(re.findall(r'href="(/[^"]*)"', s)):
        if not exists(href):
            report("FAIL", name, f"broken internal link {href}")


def audit_listings():
    posts = sorted(f.parent.name for f in (ROOT / "blog").glob("*/index.html"))
    sources = {
        "sitemap.xml": (ROOT / "sitemap.xml").read_text(encoding="utf-8"),
        "feed.xml": (ROOT / "feed.xml").read_text(encoding="utf-8"),
        "llms.txt": (ROOT / "llms.txt").read_text(encoding="utf-8"),
        "sitemap.html": (ROOT / "sitemap.html").read_text(encoding="utf-8"),
        "blog/index.html": (ROOT / "blog/index.html").read_text(encoding="utf-8"),
        "js/shell.js": (ROOT / "js/shell.js").read_text(encoding="utf-8"),
    }
    for fname in ("sitemap.xml", "feed.xml"):
        try:
            xml.dom.minidom.parseString(sources[fname])
        except Exception as e:  # noqa: BLE001
            report("FAIL", fname, f"invalid XML: {e}")
    for slug in posts:
        for fname, text in sources.items():
            if f"/blog/{slug}/" not in text:
                report("FAIL", fname, f"post not listed: {slug}")
    for lastmod in re.findall(r"<lastmod>([^<]+)</lastmod>", sources["sitemap.xml"]):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod):
            report("WARN", "sitemap.xml", f"lastmod not YYYY-MM-DD: {lastmod}")
    return len(posts)


def main():
    seen_titles, seen_desc = defaultdict(list), defaultdict(list)
    print("Pages")
    n = 0
    for f, path in pages():
        audit_page(f, path, seen_titles, seen_desc)
        n += 1
    for t, where in seen_titles.items():
        if len(where) > 1:
            report("WARN", ", ".join(where), f"duplicate title: {t}")
    for d, where in seen_desc.items():
        if len(where) > 1:
            report("WARN", ", ".join(where), "duplicate meta description")
    print("Listings")
    count = audit_listings()
    print(f"\n{n} pages, {count} posts: {problems['FAIL']} FAIL, {problems['WARN']} WARN")
    sys.exit(1 if problems["FAIL"] else 0)


if __name__ == "__main__":
    main()
