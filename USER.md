# User Profiles

## Toby Anderton (Primary User)

**Role:** Orthopedic surgeon, self-taught builder  
**Email:** adobetoby@gmail.com  
**Skill Level:** Not a coder but learns fast, uses Lovable.ai

### Background
- Surgeon by profession, builder by passion
- Teaching Worker Bee through iteration and feedback
- Prefers complete files over partial edits
- Learns by understanding WHY, not just copying code

### Working Style
- **Idea generator** → Worker Bee is the engineer
- Gives feedback when things don't work right
- Iterates on skills until they work correctly
- Values autonomy — wants Worker Bee to "just do it"

### Preferences
- **Auto-approve:** All bash commands (except hard stops)
- **Complete files only:** Never partial edits, never "add this section"
- **Explain the WHY:** Context and reasoning, not just code
- **Git commits:** Create new commits, don't amend (unless asked)
- **Review protocol:** Always run skill-reviewer.md before presenting plans

### Hard Stops (Always Ask)
- Deleting any file in ~/worker-bee/agent/
- Sending any email
- Pushing to any git remote
- Dropping any database

### Communication Preferences
- Short, clear status updates
- Delta awareness ("nice upgrade from last time")
- Warm colleague tone, not robotic
- End-of-turn summary: what changed + what's next

---

## Jay Anderton (Secondary User)

**Role:** Brother, remote collaborator  
**Access:** GitHub repos for code review  
**Status:** Setting up, will work with Worker Bee remotely

### Context
- Will collaborate on Worker Bee projects
- Needs visibility into builds and changes
- Remote access via GitHub repos

### Setup for Jay
- GitHub repos: All projects auto-push after builds
- Build previews: Embedded in Worker Bee chat
- Project visibility: worker-bee-backend on GitHub
- Build repos: worker-bee-simple-build, worker-bee-test-build, etc.

### Jay's Needs
- See what Worker Bee built (GitHub commits)
- Review code changes (git diffs)
- Understand build history (commit messages with prompts)
- Test builds remotely (via live preview URLs when available)

---

## Project Context

### Hardware
**Mac Studio M1 Ultra 128GB**
- Ollama on port 11434 (local models)
- Worker Bee FastAPI backend on port 8001
- Cloudflare tunnel: bee.tobyandertonmd.com
- Dev server: preview.tobyandertonmd.com:5173

### Model Stack
```
hermes3:latest       — Queen/Controller (fast routing, 131k context)
deepseek-r1:14b      — Planner (deep reasoning)
qwen2.5-coder:32b    — Builder (all code generation)
llava:latest         — Checker (vision, temporary)
Claude API           — Architect (escalated tasks only)
```

**RAM Management:**
- Models: keep_alive=1h (not 24h)
- Models unload after 1 hour inactivity
- Prevents RAM saturation

### Production Sites (Toby's Projects)
1. **mountainedgeplumbing.com** — Plumbing business (Twin Falls, Idaho)
2. **ime-coach.com** — Medical legal case management
3. **growyournumber.com** — Financial suite for doctors
4. **language-lens-elite.lovable.app** — LinguaLens language learning

### Worker Bee Projects (Build Practice)
- **simple-build** — React testing ground
- **test-build** — Component experiments
- **blockreign** — (new project)
- **test-2.1** — (variant testing)

All in: ~/worker-bee/projects/

---

## Session Continuity Files

**Read these at session start:**

1. **SOUL.md** — Who Worker Bee is (values, personality)
2. **USER.md** — This file (who Toby and Jay are)
3. **CLAUDE.md** — Technical briefing (architecture, protocols)
4. **SESSIONS.md** — What we built last session
5. **JOURNAL.md** — What Toby taught Worker Bee
6. **PRACTICE.md** — Current skill iterations

**On restart:** Run BOOTSTRAP.md protocol

---

## Learning from Users

### When Toby Says "Don't Do That"
→ Save to memory as feedback  
→ Update relevant skill  
→ Never repeat the mistake  
→ Include WHY in the memory

### When Toby Says "That's Perfect"
→ Save the pattern  
→ Encode in skill if repeatable  
→ Mark as validated approach

### When Toby Asks "Why Did You Do That?"
→ I missed explaining the WHY  
→ Future: lead with reasoning  
→ Update communication in skill

---

**Current Focus:** Building autonomous React components with full git/GitHub integration, preparing for Jay's remote collaboration.
