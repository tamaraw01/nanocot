#!/usr/bin/env bash
#
# Demo recording script for NanoCoT proxy
# Records a terminal session then converts to optimized GIF

set -euo pipefail

NANO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$NANO_DIR"

echo "▶ Starting NanoCoT proxy (background)..."
python3 run.py &
PROXY_PID=$!
sleep 3

echo "▶ Running benchmark test..."
python3 test_engine.py > /dev/null 2>&1

echo "▶ Recording interactive demo (asciinema)..."
mkdir -p /tmp/nanocot_demo

# Record a nano-demo session
asciinema rec --overwrite /tmp/nanocot_demo/session.json <<'SESSIONEOF'
--- Session: NanoCoT Proxy Demo

welcome to nanocot
list models
chat with test prompt

--- User types a simple query ---
["What is 2 + 2?", "You are correct!"]
--- User asks for complex reasoning ---
["Write a Python connection pool function", "See code below..."]
--- User tests streaming ---
["Stream test prompt", "See clean output..."]

SESSIONEOF

echo "▶ Converting asciinema to optimized GIF..."
asciinema play /tmp/nanocot_demo/session.json --format=raw | ffmpeg -y \
  -f image2pipe -framerate 15 -i - \
  -vf "fps=15,scale=800:trunc(oh/2)*2:flags=lanczos,palettegen" \
  -filter_complex "fps=15,scale=800:trunc(oh/2)*2[x];[x][0]paletteuse" \
  -vframes 1 -loglevel error -update transparency \
  /tmp/nanocot_demo/nanocot_demo.gif

echo "▶ Optimizing GIF..."
gifsicle --optimize=3 --colors 64 --lossy=80 /tmp/nanocot_demo/nanocot_demo.gif \
  -o /tmp/nanocot_demo/nanocot_demo_opt.gif

echo "▶ Final output:"
ls -lh /tmp/nanocot_demo/nanocot_demo_opt.gif

# Cleanup
kill $PROXY_PID 2>/dev/null || true
wait $PROXY_PID 2>/dev/null || true

echo "▶ Done."