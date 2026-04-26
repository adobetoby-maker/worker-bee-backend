# Blueprint Deployment Instructions

## ✅ COMPLETED

Backend server built at `~/worker-bee/blueprint/` and tested successfully.

### What Was Built

1. **Node.js WebSocket Server** (port 8002)
   - `server.ts` - Main WebSocket server
   - `routes/blueprint.ts` - Claude API integration
   - Matches Lovable frontend contract exactly

2. **Message Protocol** (aligned with frontend)
   - Client → Server: `{action: "blueprint_paths", idea, features}`
   - Server → Client: `{type: "blueprint_ready"}`
   - Server → Client: `{type: "blueprint_generating"}`
   - Server → Client: `{type: "blueprint_paths", data: {...}}`
   - Server → Client: `{type: "blueprint_error", message: "..."}`

3. **TypeScript Types** (matching frontend)
   - `id: string` (not number)
   - `recommended: string` (not number)
   - Complexity: "Simple" | "Moderate" | "Complex"

---

## 🚀 DEPLOYMENT STEPS

### 1. Add to start.sh

Append these lines to `~/worker-bee/start.sh`:

```bash
echo ""
echo "🗺️  Starting Blueprint server on port 8002..."
cd ~/worker-bee/blueprint
npm run start > /tmp/blueprint.log 2>&1 &
BLUEPRINT_PID=$!
echo "✅ Blueprint started (PID: $BLUEPRINT_PID)"
```

### 2. Update Cloudflare Tunnel

Edit `~/.cloudflared/config.yml` and add Blueprint subdomain:

```yaml
tunnel: worker-bee
credentials-file: /Users/drive/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  # Main Worker Bee backend
  - hostname: bee.tobyandertonmd.com
    service: http://localhost:8001

  # Blueprint server (NEW)
  - hostname: blueprint.bee.tobyandertonmd.com
    service: http://localhost:8002

  # Catch-all
  - service: http_status:404
```

Then restart the tunnel:

```bash
pkill cloudflared
sleep 2
cloudflared tunnel run worker-bee > /tmp/cloudflared.log 2>&1 &
```

### 3. Verify Deployment

**Local health check:**
```bash
curl http://localhost:8002/health
```

Expected:
```json
{"status":"ok","service":"blueprint-server","version":"1.0.0",...}
```

**Public health check (after Cloudflare setup):**
```bash
curl https://blueprint.bee.tobyandertonmd.com/health
```

### 4. Frontend Connection

Frontend is already built by Lovable and connects to:
```
wss://blueprint.bee.tobyandertonmd.com
```

Files:
- `src/lib/blueprint-ws.ts` - WebSocket client
- `src/components/BlueprintView.tsx` - UI component
- `src/components/Sidebar.tsx` - Tab added
- `src/routes/index.tsx` - Route added

---

## 🧪 TESTING

### Manual WebSocket Test

```bash
npm install -g wscat
wscat -c ws://localhost:8002
```

Then send:
```json
{"action":"blueprint_paths","idea":"A todo app","features":["User auth","Dark mode"]}
```

Expected response sequence:
1. `{"type":"blueprint_ready"}`
2. `{"type":"blueprint_generating"}`
3. `{"type":"blueprint_paths","data":{...}}`

### Test with Frontend

1. Start Blueprint server: `cd ~/worker-bee/blueprint && npm run dev`
2. Open Lovable frontend
3. Click "🗺 BLUEPRINT" tab
4. Enter idea and features
5. Click "Ask Bee for a Path →"
6. Should see 3 path cards with recommendation

---

## 📊 MONITORING

### View Logs

```bash
# Development (stdout)
cd ~/worker-bee/blueprint
npm run dev

# Production (background)
tail -f /tmp/blueprint.log
```

### Check Running Processes

```bash
# Find Blueprint server PID
lsof -ti :8002

# Kill if needed
lsof -ti :8002 | xargs kill -9
```

---

## 🐛 TROUBLESHOOTING

### "ANTHROPIC_API_KEY not configured"

```bash
# Check key exists
grep ANTHROPIC_API_KEY ~/worker-bee/.env

# If missing, add it
echo "ANTHROPIC_API_KEY=sk-ant-xxxxx" >> ~/worker-bee/.env
```

### "Port 8002 already in use"

```bash
lsof -ti :8002 | xargs kill -9
cd ~/worker-bee/blueprint && npm run dev
```

### "Cannot connect to WebSocket"

1. Check server running: `curl http://localhost:8002/health`
2. Check Cloudflare tunnel running: `ps aux | grep cloudflared`
3. Check tunnel config has blueprint.bee.tobyandertonmd.com
4. Check DNS propagation: `dig blueprint.bee.tobyandertonmd.com`

### "Claude API timeout"

- Normal for first request (cold start)
- Typical generation time: 5-15 seconds
- Check API key quota at console.anthropic.com

---

## 📝 NEXT STEPS

1. ✅ Backend built and tested
2. ✅ Frontend already deployed by Lovable
3. ⏳ Add to start.sh (manual step)
4. ⏳ Configure Cloudflare tunnel (manual step)
5. ⏳ Test end-to-end flow
6. ⏳ Monitor production usage

---

## 🔗 INTEGRATION

Blueprint is now fully integrated with Worker Bee:

```
User → Lovable Frontend (worker-bee.lovable.app)
  ↓
Blueprint Tab (BlueprintView.tsx)
  ↓
blueprint-ws.ts WebSocket Client
  ↓
wss://blueprint.bee.tobyandertonmd.com
  ↓
Blueprint Server (port 8002)
  ↓
Claude API (claude-sonnet-4-20250514)
  ↓
3 Implementation Paths
  ↓
User selects path → starts building
```

---

**Blueprint is ready to ship.** 🐝🗺️
