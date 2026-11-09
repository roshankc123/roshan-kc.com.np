#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver, Yep...) which URLs changed.

    python3 scripts/seo/indexnow.py              # URLs new or changed in sitemap.xml since the last run
    python3 scripts/seo/indexnow.py --all        # every URL in sitemap.xml
    python3 scripts/seo/indexnow.py URL [URL..]  # just these URLs
    add --dry-run to print without sending

Run it after a deploy: the key file must already be live at
https://www.roshan-kc.com.np/<KEY>.txt or the engines reject the submission.
What was sent is remembered in .indexnow-state.json (git-ignored) as url -> lastmod.
Google does not use IndexNow; use Search Console there.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOST = "www.roshan-kc.com.np"
KEY = "cecf42ed10c14e03a85b4f593fb8aa9b"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
STATE = ROOT / ".indexnow-state.json"


def sitemap():
    s = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    out = {}
    for block in re.findall(r"<url>(.*?)</url>", s, re.S):
        loc = re.search(r"<loc>([^<]+)</loc>", block).group(1).strip()
        mod = re.search(r"<lastmod>([^<]+)</lastmod>", block)
        out[loc] = mod.group(1).strip() if mod else ""
    return out


def key_is_live():
    try:
        with urllib.request.urlopen(urllib.request.Request(KEY_LOCATION, headers={"User-Agent": "indexnow-submit"}), timeout=15) as r:
            return r.status == 200 and r.read().decode().strip() == KEY
    except (urllib.error.URLError, TimeoutError):
        return False


def submit(urls):
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "indexnow-submit"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    current = sitemap()
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if args:
        urls = args
    elif "--all" in sys.argv:
        urls = list(current)
    else:
        urls = [u for u, mod in current.items() if state.get(u) != mod]
    bad = [u for u in urls if not u.startswith(f"https://{HOST}/")]
    if bad:
        sys.exit(f"not on {HOST}: {bad}")
    if not urls:
        print("IndexNow: nothing new or changed since the last submission")
        return
    print(f"IndexNow: {len(urls)} URL(s)")
    for u in urls:
        print("  ", u)
    if dry:
        return
    if not key_is_live():
        sys.exit(f"IndexNow: {KEY_LOCATION} is not live yet; deploy first, then run this again")
    status, text = submit(urls[:10000])
    # 200 = accepted, 202 = accepted (key check pending); anything else is an error
    print(f"IndexNow: HTTP {status} {text[:200]}")
    if status in (200, 202):
        for u in urls:
            if u in current:
                state[u] = current[u]
        STATE.write_text(json.dumps(state, indent=1, sort_keys=True))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
