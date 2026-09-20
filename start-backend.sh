#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "ERROR: .venv does not exist."
    exit 1
fi

source .venv/bin/activate

PORT=8127

if ss -ltn | grep -q ":${PORT} "; then
    echo "ERROR: VideoGrab port ${PORT} is already in use."
    echo "Run: sudo lsof -i :${PORT}"
    exit 1
fi

echo "======================================"
echo " VideoGrab API"
echo "======================================"
echo "API:  http://127.0.0.1:${PORT}"
echo "Docs: http://127.0.0.1:${PORT}/docs"
echo "======================================"

exec uvicorn backend.app.main:app \
    --reload \
    --host 127.0.0.1 \
    --port "${PORT}"
