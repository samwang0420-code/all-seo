#!/bin/bash
# getuscompliance.com Auto Update Script
# Runs: Every Sunday at 2 AM

set -e

PROJECT_DIR="/root/.openclaw/workspace-geo-all/all-seo"
TOKEN="X-3jRM7vU05v4XKinPscNTaq66haXS_kXVm6dsaD"

echo "$(date): Starting getuscompliance.com update..."

cd "$PROJECT_DIR"

# Build
echo "$(date): Building..."
npm run build

# Deploy
echo "$(date): Deploying..."
CLOUDFLARE_API_TOKEN="$TOKEN" npx wrangler pages deploy dist

echo "$(date): Update complete!"
