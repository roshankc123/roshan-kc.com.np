#!/usr/bin/env bash
# Copy only the public site into dist/ so secrets and tooling never get deployed.
set -euo pipefail
cd "$(dirname "$0")/.."

# Rebuild TOC / series / author / related blocks in every post
python3 -I scripts/blog/enhance.py

rm -rf dist
mkdir -p dist

cp index.html 404.html sitemap.html robots.txt sitemap.xml feed.xml llms.txt \
   manifest.json browserconfig.xml favicon.ico _headers _redirects dist/
cp ./*.png dist/
cp -R blog css js fonts images cv dist/

find dist -name '.DS_Store' -delete
echo "Built dist/ ($(find dist -type f | wc -l | tr -d ' ') files)"
