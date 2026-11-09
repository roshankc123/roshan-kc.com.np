#!/usr/bin/env bash
# Copy only the public site into dist/ so secrets and tooling never get deployed.
set -euo pipefail
cd "$(dirname "$0")/.."

# Generate every blog page and listing from content/ + templates/ (also runs enhance.py)
python3 -I scripts/site/build.py

rm -rf dist
mkdir -p dist

cp index.html 404.html sitemap.html robots.txt sitemap.xml feed.xml llms.txt \
   cecf42ed10c14e03a85b4f593fb8aa9b.txt \
   manifest.json favicon.ico _headers _redirects dist/
cp ./*.png dist/
cp -R blog css js fonts images cv dist/

find dist -name '.DS_Store' -delete
# Minify CSS and fingerprint CSS/JS in dist/ (long-cache safe)
python3 -I scripts/site/optimize.py

echo "Built dist/ ($(find dist -type f | wc -l | tr -d ' ') files)"
