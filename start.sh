#!/usr/bin/env bash
set -euo pipefail

WALLET_DIR="/opt/wallet"
mkdir -p "$WALLET_DIR"

# Decode wallet
printf "%s" "$ORACLE_WALLET_BASE64" | base64 --decode > /tmp/wallet.zip
unzip -o /tmp/wallet.zip -d "$WALLET_DIR"
rm /tmp/wallet.zip

# Tell Oracle client where the wallet is
export TNS_ADMIN="$WALLET_DIR"

# Start app
exec gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:application
