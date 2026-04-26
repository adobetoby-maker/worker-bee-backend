#!/bin/zsh
# 🐝 Worker Bee — Daily Startup Script v4
cd ~/worker-bee
source .venv/bin/activate

echo ""
echo "🐝 Worker Bee Starting..."
echo "================================"

caffeinate -i &
echo "☕ Mac will stay awake"

echo ""
echo "🔫 Clearing ports..."
lsof -ti :8001 | xargs kill -9 2>/dev/null
lsof -ti :5173 | xargs kill -9 2>/dev/null
sleep 2
echo "✅ Ports clear"

echo ""
if ! pgrep -x ollama > /dev/null; then
    echo "🦙 Starting Ollama..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 4
    echo "✅ Ollama started"
else
    echo "✅ Ollama already running"
fi

echo ""
echo "🔥 Warming models..."
curl -s http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:32b","prompt":"hi","keep_alive":"1h","options":{"num_ctx":20480}}' > /dev/null &
curl -s http://localhost:11434/api/generate \
  -d '{"model":"deepseek-r1:14b","prompt":"hi","keep_alive":"1h","options":{"num_ctx":8192}}' > /dev/null &
curl -s http://localhost:11434/api/generate \
  -d '{"model":"llava:latest","prompt":"hi","keep_alive":"1h","options":{"num_ctx":8192}}' > /dev/null &
curl -s http://localhost:11434/api/generate \
  -d '{"model":"phi4:latest","prompt":"hi","keep_alive":"1h","options":{"num_ctx":8192}}' > /dev/null &
wait
echo "✅ All models warm"

echo ""
MANIFEST_COUNT=$(find ~/worker-bee/manifests -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "📋 $MANIFEST_COUNT skill manifests loaded"

echo ""
echo "🔄 Starting dev servers..."
for dir in ~/worker-bee/projects/*/; do
    if [ -f "$dir/package.json" ]; then
        project=$(basename "$dir")
        echo "   → $project"
        cd "$dir" && npm run dev > /tmp/devserver-$project.log 2>&1 &
        cd ~/worker-bee
    fi
done
echo "✅ Dev servers started"

echo ""
echo "🌐 Starting Cloudflare tunnel..."
pkill cloudflared 2>/dev/null
sleep 1
cloudflared tunnel run worker-bee > /tmp/cloudflared.log 2>&1 &
sleep 3
echo "✅ Tunnel started"

(while true; do
    sleep 240
    curl -s http://localhost:11434/api/ps > /dev/null 2>&1
done) &

echo ""
echo "🎓 Starting continuous practice loop..."
pkill -f continuous_practice_loop 2>/dev/null
python continuous_practice_loop.py > /tmp/practice-loop.log 2>&1 &
echo "✅ Practice loop started (background)"

echo ""
echo "🗺️  Starting Blueprint server on port 8002..."
pkill -f "ts-node server.ts" 2>/dev/null
lsof -ti :8002 | xargs kill -9 2>/dev/null
cd ~/worker-bee/blueprint
npm run start > /tmp/blueprint.log 2>&1 &
BLUEPRINT_PID=$!
echo "✅ Blueprint started (PID: $BLUEPRINT_PID)"
cd ~/worker-bee

echo ""
echo "⚡ Starting Worker Bee on port 8001..."
echo "================================"
echo "🌐 https://worker-bee.lovable.app"
echo "⚙️  CONFIG → https://bee.tobyandertonmd.com"
echo "🗺️  BLUEPRINT → https://blueprint.worker-bee.app"
echo "📋 Manifests → ~/worker-bee/manifests/"
echo "🎓 Practice → ~/worker-bee/manifests/practice/"
echo "================================"
echo ""

lsof -ti :8001 | xargs kill -9 2>/dev/null
sleep 2

uvicorn main:app --host 0.0.0.0 --port 8001
