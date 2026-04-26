# Blueprint Server

Standalone Node.js WebSocket server for Worker Bee's Blueprint feature.

Blueprint is a prompt engineering tool that generates 3 implementation paths for any project idea using Claude Sonnet 4.

## Architecture

```
Port 8001: FastAPI Backend (existing Worker Bee)
Port 8002: Blueprint Server (this server)
Port 5173: Lovable Frontend (connects to both)

Frontend → ws://localhost:8002 → Blueprint Server → Claude API
```

## Quick Start

### 1. Install Dependencies

```bash
cd ~/worker-bee/blueprint
npm install
```

### 2. Configure API Key

The Blueprint server reads `ANTHROPIC_API_KEY` from `~/worker-bee/.env`.

Verify it exists:
```bash
grep ANTHROPIC_API_KEY ~/worker-bee/.env
```

If not found, add it:
```bash
echo "ANTHROPIC_API_KEY=sk-ant-xxxxx" >> ~/worker-bee/.env
```

### 3. Run Development Server

```bash
npm run dev
```

Server starts on port 8002. You should see:
```
🗺️  BLUEPRINT SERVER STARTED
Port: 8002
Health: http://localhost:8002/health
WebSocket: ws://localhost:8002
✅ ANTHROPIC_API_KEY configured
```

### 4. Test Health Endpoint

```bash
curl http://localhost:8002/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "blueprint-server",
  "version": "1.0.0",
  "port": 8002,
  "timestamp": "2026-04-26T..."
}
```

## WebSocket Protocol

### Client → Server

```json
{
  "action": "generate_paths",
  "idea": "A tool to manage customer feedback",
  "features": [
    "User authentication",
    "Email notifications",
    "Analytics dashboard"
  ]
}
```

### Server → Client (Status Update)

```json
{
  "type": "status",
  "message": "Analyzing your idea..."
}
```

### Server → Client (Success)

```json
{
  "type": "paths",
  "data": {
    "recommended": 0,
    "paths": [
      {
        "id": 0,
        "name": "Quick & Minimal",
        "tagline": "Get it working fast",
        "why_recommended": "...",
        "pros": ["...", "..."],
        "cons": ["...", "..."],
        "tech_approach": "...",
        "time_estimate": "2-3 hours",
        "complexity": "Simple"
      }
      // ... 2 more paths
    ],
    "bee_note": "Focus on getting the feedback form working first"
  }
}
```

### Server → Client (Error)

```json
{
  "type": "error",
  "error": "Claude API error: Rate limit exceeded"
}
```

## Production Deployment

### Add to start.sh

Append to `~/worker-bee/start.sh`:

```bash
echo ""
echo "🗺️  Starting Blueprint server on port 8002..."
cd ~/worker-bee/blueprint
npm run start > /tmp/blueprint.log 2>&1 &
echo "✅ Blueprint started (background)"
```

### Add to Cloudflare Tunnel

Edit `~/.cloudflared/config.yml`:

```yaml
ingress:
  # Existing rule for port 8001
  - hostname: bee.tobyandertonmd.com
    service: http://localhost:8001

  # NEW: Blueprint on subdomain
  - hostname: blueprint.bee.tobyandertonmd.com
    service: http://localhost:8002

  # Catch-all (keep at bottom)
  - service: http_status:404
```

Then restart tunnel:
```bash
pkill cloudflared
cloudflared tunnel run worker-bee > /tmp/cloudflared.log 2>&1 &
```

### Verify Production

```bash
curl https://blueprint.bee.tobyandertonmd.com/health
```

## Frontend Integration

### TypeScript Types

```typescript
interface BlueprintPath {
  id: number;
  name: string;
  tagline: string;
  why_recommended: string;
  pros: string[];
  cons: string[];
  tech_approach: string;
  time_estimate: string;
  complexity: "Simple" | "Moderate" | "Complex";
}

interface BlueprintData {
  recommended: number;
  paths: BlueprintPath[];
  bee_note: string;
}
```

### WebSocket Client

```typescript
const ws = new WebSocket('wss://blueprint.bee.tobyandertonmd.com');

ws.onopen = () => {
  ws.send(JSON.stringify({
    action: 'generate_paths',
    idea: userIdea,
    features: userFeatures
  }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.type === 'status') {
    console.log(msg.message); // "Analyzing your idea..."
  } else if (msg.type === 'paths') {
    console.log(msg.data); // BlueprintData object
  } else if (msg.type === 'error') {
    console.error(msg.error);
  }
};
```

## Development

### File Structure

```
blueprint/
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── server.ts             # Main WebSocket server
├── routes/
│   └── blueprint.ts      # Claude API integration
├── .env.template         # Environment template
└── README.md            # This file
```

### Logs

Development: Logs to console
Production: Logs to `/tmp/blueprint.log`

View logs:
```bash
tail -f /tmp/blueprint.log
```

### Debugging

Test WebSocket connection:
```bash
npx wscat -c ws://localhost:8002
```

Then send:
```json
{"action":"generate_paths","idea":"test","features":[]}
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Check `~/worker-bee/.env` exists
- Verify key starts with `sk-ant-`
- Restart server after adding key

### "Port 8002 already in use"
```bash
lsof -ti :8002 | xargs kill -9
npm run dev
```

### "Cannot connect to WebSocket"
- Check server is running: `curl http://localhost:8002/health`
- Check Cloudflare tunnel config
- Verify frontend using correct URL

### "Claude API timeout"
- Claude API can take 10-15 seconds
- Client should show "Analyzing..." status
- If timeout persists, check API key quota

## License

Part of Worker Bee system. See parent directory.
