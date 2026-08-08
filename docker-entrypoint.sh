#!/bin/sh

set -e

echo "Starting AutoOps..."

mkdir -p /app/data

# Gmail OAuth credentials
if [ -n "$GMAIL_CREDENTIALS_JSON_B64" ]; then
    echo "$GMAIL_CREDENTIALS_JSON_B64" | base64 -d > /app/data/credentials.json
    echo "Gmail credentials restored."
fi

# Gmail OAuth token
if [ -n "$GMAIL_TOKEN_JSON_B64" ]; then
    echo "$GMAIL_TOKEN_JSON_B64" | base64 -d > /app/data/token.json
    echo "Gmail token restored."
fi

exec "$@"