#!/usr/bin/env bash
set -euo pipefail

# ----------------------------
# Configuration
# ----------------------------

# Render provides $PORT automatically
PORT="${PORT:-10000}"  # fallback if not set

# Use a writable directory for the Oracle wallet
WALLET_DIR="/tmp/wallet"

# ----------------------------
# Prepare wallet
# ----------------------------

# Create wallet directory
mkdir -p "$WALLET_DIR"

# Decode the base64 wallet environment variable and unzip
if [ -n "${ORACLE_WALLET_BASE64:-}" ]; then
  echo "Decoding Oracle wallet..."
  printf "%s" "$ORACLE_WALLET_BASE64" | base64 --decode > /tmp/wallet.zip
  unzip -o /tmp/wallet.zip -d "$WALLET_DIR"
  rm /tmp/wallet.zip
else
  echo "WARNING: ORACLE_WALLET_BASE64 is not set. Make sure to provide it in Render environment variables."
fi

# Set TNS_ADMIN so Oracle client knows where tnsnames.ora and sqlnet.ora are
export TNS_ADMIN="$WALLET_DIR"

# Optional: show wallet files for debugging (remove after first successful deploy)
echo "Wallet contents:"
ls -l "$WALLET_DIR" || true

# ----------------------------
# Start Flask app with Gunicorn
# ----------------------------

echo "Starting Flask app..."
exec gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:application
