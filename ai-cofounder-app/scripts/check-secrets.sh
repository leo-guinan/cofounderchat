#!/bin/bash
# Check that all required secrets are set

set -e

REQUIRED_SECRETS=(
  "OPENAI_API_KEY"
  "DATABASE_URL"
  "SESSION_SECRET"
)

OPTIONAL_SECRETS=(
  "ANTHROPIC_API_KEY"
  "GITHUB_CLIENT_SECRET"
  "S3_ACCESS_KEY"
  "SENTRY_DSN"
)

echo "Checking required secrets..."
MISSING=0

for secret in "${REQUIRED_SECRETS[@]}"; do
  if [ -z "${!secret}" ]; then
    echo "❌ Missing required secret: $secret"
    MISSING=1
  else
    echo "✓ $secret is set"
  fi
done

echo ""
echo "Checking optional secrets..."

for secret in "${OPTIONAL_SECRETS[@]}"; do
  if [ -z "${!secret}" ]; then
    echo "⚠️  Optional secret not set: $secret"
  else
    echo "✓ $secret is set"
  fi
done

if [ $MISSING -eq 1 ]; then
  echo ""
  echo "❌ Some required secrets are missing!"
  echo "See docs/SECRETS.md for setup instructions"
  exit 1
fi

echo ""
echo "✅ All required secrets are set!"
