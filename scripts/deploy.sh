#!/usr/bin/env bash
# Build dist/ and deploy it to Cloudflare Pages. Only dist/ is uploaded —
# never node_modules, .env or other tooling.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  echo "Missing .env — copy .env.example to .env and fill in your Cloudflare keys." >&2
  exit 1
fi

set -a
. ./.env
set +a

for var in CLOUDFLARE_ACCOUNT_ID CLOUDFLARE_API_TOKEN CF_PAGES_PROJECT; do
  if [[ -z "${!var:-}" ]]; then
    echo "$var is empty in .env — fill it in before deploying." >&2
    exit 1
  fi
done

npm run build

# Create the Pages project on first deploy only; any failure here is shown and stops the deploy
if ! npx --yes wrangler pages project list 2>/dev/null | grep -qw -- "$CF_PAGES_PROJECT"; then
  echo "Creating Cloudflare Pages project \"$CF_PAGES_PROJECT\"..."
  npx --yes wrangler pages project create "$CF_PAGES_PROJECT" \
    --production-branch "${CF_PAGES_BRANCH:-main}"
fi

npx --yes wrangler pages deploy dist \
  --project-name "$CF_PAGES_PROJECT" \
  --branch "${CF_PAGES_BRANCH:-main}" \
  --commit-dirty=true

# Tell IndexNow engines (Bing and others) which URLs changed
python3 -I scripts/seo/indexnow.py || echo "IndexNow submission failed; run: npm run indexnow"
