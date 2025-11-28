#!/usr/bin/env bash
set -euo pipefail

# ----------------------------
# Configuration
# ----------------------------

# Render automatically provides $PORT
PORT="${PORT:-10000}"  # fallback if not set

# ----------------------------
# Start Flask app with Gunicorn
# ----------------------------

echo "Starting Flask app on port $PORT..."
exec gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:application
