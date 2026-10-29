#!/usr/bin/env bash
# ==============================================================================
# NecroGit - Zero-Dependency One-Shot Launcher
# ==============================================================================
set -e

PORT="${PORT:-7777}"
HOST="${HOST:-0.0.0.0}"
MODEL="${MODEL:-gemma2:2b}"

echo "🕯️ Launching NecroGit..."
python3 app/server.py --port "$PORT" --host "$HOST" --model "$MODEL"
