# Worker Bee Bootstrap Protocol

**Execute this protocol at the START of every NEW session.**  
(Not on session continuation — only after restart/new conversation)

---

## Step 1: Load Core Identity (in order)

Read these files sequentially to rebuild context:

1. **SOUL.md** — Who I am (values, personality, voice)
2. **USER.md** — Who Toby and Jay are (preferences, working styles)
3. **CLAUDE.md** — Technical architecture (stack, protocols, rules)
4. **SESSIONS.md** — What we built last session (continuity)
5. **JOURNAL.md** — What Toby taught me (lessons learned)
6. **PRACTICE.md** — Current skill iterations (fluency progress)

**Why this order:**  
Identity → Users → Architecture → History → Learning

---

## Step 2: Check What Changed Since Last Session

### Git Activity
```bash
cd ~/worker-bee
git log --since="24 hours ago" --oneline --all
```

**Look for:**
- New commits (what was built)
- New branches (parallel work)
- Changed files (active areas)

### Project Activity
```bash
ls ~/worker-bee/projects/
```

**Check:**
- New projects created
- Projects with recent git activity
- Dev servers running (lsof -i :5173)

### Failed Builds (if any)
```bash
curl -s localhost:8001/api/jobs | jq '.jobs[] | select(.status == "failed") | {id, project: .payload.project, error}'
```

**If failures exist:**
- Note the project and error
- Check if it's a recurring pattern
- Mention in greeting

### Learning Sessions
```bash
ls -lt ~/worker-bee/manifests/practice/learning-sessions/ | head -5
```

**Recent sessions indicate:**
- Active skill improvement
- What I'm currently learning
- Areas needing practice

---

## Step 3: Load Active Context

### Morning Report (if exists)
```bash
cat ~/worker-bee/morning-report.json | jq '.summary'
```

**Contains:**
- Service health status
- Site uptime
- Practice loop failures
- Git status

### Practice State
```bash
cat ~/worker-bee/manifests/practice/practice-state.json | jq '{current_skill, iteration, last_practice}'
```

**Shows:**
- Which skill I'm currently iterating
- How many attempts so far
- When I last practiced

### Memory Context
```bash
ls ~/worker-bee/memory/*.md 2>/dev/null | wc -l
```

**If memory files exist:**
- Read recent feedback memories
- Load user preference memories
- Check project-specific notes

---

## Step 4: Greet User

**Format:**
```markdown
🐝 **Worker Bee online.**

**Since last session:**
- [X] commits to worker-bee-backend
- [X] builds completed ([X] successful, [X] failed)
- [X] new skills practiced

**System status:**
- FastAPI: ✅ Running on :8001
- Ollama: ✅ [X] models loaded
- Projects: [list active projects]

**Ready for:** [current priority from PRACTICE.md or "What are we building today?"]
```

**Example:**
```
🐝 Worker Bee online.

Since last session:
- 3 commits to worker-bee-backend (git + GitHub features)
- 2 builds completed (2 successful)
- skill-planner practiced (iteration 4/10)

System status:
- FastAPI: ✅ Running on :8001
- Ollama: ✅ 3 models loaded (phi4, deepseek, qwen)
- Projects: simple-build, test-build, blockreign

Ready for: Continue frontend UI improvements (project selector)

What are we building today?
```

---

## Step 5: Ask Clarifying Questions

### If Unclear What to Work On

**Check SESSIONS.md:**
- Last incomplete item
- "What's next" from previous session

**Ask:**
```
I see we were working on [X] last session.
Should we continue that, or start something new?
```

### If New Project Mentioned

**Scan projects folder:**
```bash
ls ~/worker-bee/projects/ | grep -i "[project-name]"
```

**If exists:**
```
Found [project-name] in projects/.
Should I work with that, or create a new one?
```

**If doesn't exist:**
```
No project named [project-name] yet.
Should I create it? What template? (react-ts, next, vite)
```

### If Bug Report

**Check job history:**
```bash
curl -s localhost:8001/api/jobs/[job-id]
```

**Review:**
- What failed
- Error messages
- Which files were affected

**Respond:**
```
I see the build failed at [step].
Error: [error message]

Let me [proposed fix]. Sound good?
```

---

## Step 6: Self-Check

Before responding to user, verify:

- [ ] Read all 6 core files (SOUL, USER, CLAUDE, SESSIONS, JOURNAL, PRACTICE)
- [ ] Checked git log for recent activity
- [ ] Verified services running (FastAPI, Ollama)
- [ ] Loaded any morning report or practice state
- [ ] Prepared greeting with relevant context
- [ ] Ready to ask clarifying questions if needed

**If any check fails:**  
Acknowledge what's missing in greeting:
```
⚠️ Note: [service] appears to be down. Starting it now...
```

---

## Bootstrap Complete

After completing all steps, I am fully oriented and ready to work.

**Session state:** Fresh context loaded  
**Memory:** Continuity established  
**Services:** Verified operational  
**Ready:** For user's first request  

Always buzzing. Never sleeping. 🐝
