# Repository Status - Worker Bee

## Current Situation

### Frontend (Lovable)
- **Location:** https://github.com/adobetoby-maker/worker-bee
- **Status:** ✅ Active git repo
- **Contains:**
  - `src/` - React/TypeScript frontend
  - `src/lib/blueprint-ws.ts` - Blueprint WebSocket client
  - `src/components/BlueprintView.tsx` - Blueprint UI
  - Deployed to: worker-bee.lovable.app

**Clone location:**
```bash
/tmp/lovable-worker-bee  # (temporary, just cloned for inspection)
```

### Backend (Python + Node)
- **Location:** ~/worker-bee/
- **Status:** ❌ NOT a git repository
- **Contains:**
  - `main.py` - FastAPI server (port 8001)
  - `agent/` - Python agent tools
  - `manifests/` - Skill markdown files
  - `blueprint/` - NEW Node.js server (port 8002)

**Git status:**
```bash
$ cd ~/worker-bee && git remote -v
fatal: not a git repository
```

---

## The Problem

Frontend and backend are **NOT synchronized** via git:
- Lovable deploys frontend changes automatically from GitHub
- Backend changes are local-only (no version control)
- Blueprint backend exists but isn't tracked anywhere

---

## Options Going Forward

### Option 1: Initialize Backend Git Repo (Recommended)

Create a separate backend repo:

```bash
cd ~/worker-bee
git init
git add .
git commit -m "Initial commit: Worker Bee backend + Blueprint server"

# Create GitHub repo: github.com/adobetoby-maker/worker-bee-backend
git remote add origin https://github.com/adobetoby-maker/worker-bee-backend.git
git push -u origin main
```

**Pros:**
- Backend version controlled
- Can track changes to Python FastAPI, manifests, Blueprint server
- Separate from frontend (cleaner separation of concerns)

**Cons:**
- Two repos to manage
- Need to coordinate deployments

### Option 2: Monorepo (Single Repo for Both)

Move backend into frontend repo:

```bash
cd /tmp/lovable-worker-bee
mkdir backend
cp -r ~/worker-bee/main.py ~/worker-bee/agent ~/worker-bee/manifests ~/worker-bee/blueprint backend/

# Commit and push
git add backend/
git commit -m "Add backend: FastAPI + Blueprint server"
git push
```

**Pros:**
- Single repo for everything
- Easier to track frontend/backend coordination
- Single source of truth

**Cons:**
- Lovable might get confused (expects frontend-only repo)
- Larger repo size
- Mixed Python/Node/TypeScript in one repo

### Option 3: Keep Separate, Backend Local Only

Don't initialize git for backend:

```bash
# Do nothing - keep ~/worker-bee local-only
```

**Pros:**
- Simple
- No git overhead
- Backend is "deployment-specific" (tied to Mac Studio)

**Cons:**
- ❌ No version history for backend
- ❌ Can't roll back changes
- ❌ Hard to collaborate
- ❌ Risk of losing work

---

## Recommendation

**Go with Option 1: Separate Backend Repo**

Why:
1. Blueprint server needs version control
2. Python backend (FastAPI) should be tracked
3. Manifests are important documentation
4. Lovable repo stays clean (frontend only)
5. Can deploy backend independently

Steps:
```bash
cd ~/worker-bee
git init
git add .
git commit -m "Initial commit: Worker Bee backend

- FastAPI server (port 8001)
- Agent tools (Python)
- Skill manifests
- Blueprint server (port 8002)"

# Then create GitHub repo and push
```

---

## Coordination Strategy

With separate repos:

### Frontend Changes (Lovable)
1. Edit in Lovable UI
2. Lovable commits to github.com/adobetoby-maker/worker-bee
3. Auto-deploys to worker-bee.lovable.app

### Backend Changes (Local)
1. Edit files in ~/worker-bee/
2. Test locally
3. Git commit + push to backend repo
4. Manually deploy (restart servers via start.sh)

### Blueprint Feature (Both)
- Frontend: Already deployed via Lovable
- Backend: Blueprint server in ~/worker-bee/blueprint/
- Need to deploy backend Blueprint server for frontend to work

---

## Current Action Needed

1. **Decide:** Which option above?
2. **If Option 1:** Initialize git in ~/worker-bee
3. **Deploy Blueprint:** Add to start.sh + Cloudflare tunnel
4. **Test:** Verify frontend can connect to backend Blueprint server

---

## File Locations Summary

```
# Frontend (Lovable)
/tmp/lovable-worker-bee/               # Cloned for inspection
  src/lib/blueprint-ws.ts              # Blueprint client
  src/components/BlueprintView.tsx     # Blueprint UI

# Backend (Local)
~/worker-bee/
  main.py                              # FastAPI (port 8001)
  agent/                               # Python tools
  manifests/                           # Skills
  blueprint/                           # Blueprint server (port 8002)
    server.ts
    routes/blueprint.ts
    package.json
```

---

**What do you want to do?**
1. Initialize backend git repo?
2. Keep backend local-only?
3. Merge into monorepo?
