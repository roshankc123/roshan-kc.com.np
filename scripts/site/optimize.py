#!/usr/bin/env python3
"""Optimise dist/ after scripts/build.sh has copied the site into it.

- minifies every CSS file (comments and whitespace only; no rewriting of rules)
- fingerprints CSS and JS: css/site.css -> css/site.3f2a9c1b.css, and rewrites every
  reference in dist HTML, so the files can be cached for a year (see the _headers rule)
Source files in the repo are never touched.
"""
import hashlib
import re
from pathlib import Path

DIST = Path(__file__).resolve().parents[2] / "dist"


def minify_css(css):
    css = re.sub(r"/\*(?!!).*?\*/", "", css, flags=re.S)       # keep /*! licence */ comments
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)                              # "a: b" -> "a:b" (selectors keep their spaces before :)
    css = css.replace(";}", "}")
    return css.strip() + "\n"


def main():
    before = after = 0
    renames = {}
    for f in sorted(DIST.glob("css/*.css")):
        src = f.read_text(encoding="utf-8")
        before += len(src.encode())
        out = minify_css(src)
        after += len(out.encode())
        f.write_text(out, encoding="utf-8")
    for f in sorted(list(DIST.glob("css/*.css")) + list(DIST.glob("js/*.js"))):
        digest = hashlib.sha256(f.read_bytes()).hexdigest()[:10]
        new = f.with_name(f"{f.stem}.{digest}{f.suffix}")
        f.rename(new)
        renames["/" + str(f.relative_to(DIST))] = "/" + str(new.relative_to(DIST))
    pages = list(DIST.rglob("*.html"))
    for p in pages:
        s = p.read_text(encoding="utf-8")
        t = re.sub(r'(href|src)="(/(?:css|js)/[^"?#]+)"', lambda m: f'{m.group(1)}="{renames.get(m.group(2), m.group(2))}"', s)
        if t != s:
            p.write_text(t, encoding="utf-8")
    html_all = "".join(p.read_text(encoding="utf-8") for p in pages)
    for new in [v for v in renames.values() if v.endswith(".css")]:
        if new not in html_all:                      # build inputs (tailwind-input, utilities, home) never ship
            (DIST / new.lstrip("/")).unlink()
    missing = [p for p in pages if re.search(r'(?:href|src)="/(?:css|js)/[^".]+\.(?:css|js)"', p.read_text(encoding="utf-8"))]
    if missing:
        raise SystemExit(f"unhashed asset reference left in: {missing[:3]}")
    print(f"optimised dist: CSS {before // 1024} KB -> {after // 1024} KB, {len(renames)} assets fingerprinted, {len(pages)} pages rewritten")


if __name__ == "__main__":
    main()
