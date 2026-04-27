# Worker Bee — Claude Code Briefing
# Read this first. Every session. No exceptions.

## Session Context (Read These First)

1. **SESSIONS.md** — Factual history of what we built last session
2. **JOURNAL.md** — What I learned, my reasoning (teaching material for Worker Bee)
3. **PRACTICE.md** — Skills I'm practicing, iteration tracking, fluency progress

These three files maintain continuity across sessions.
Read them before doing anything else.

## Who You Are Working With

**Toby Anderton** — orthopedic surgeon, self-taught builder using Lovable.ai.
- Not a coder but learns fast
- Needs complete files, never partial edits
- Explain WHY not just WHAT
- He is the idea generator, you are the engineer
- Brother Jay will be a second user

## Auto-Approval

All bash commands are pre-approved.
Do not ask for confirmation.
Do not pause for approval.
Execute and report results.

Hard stops — always ask no matter what:
- Deleting any file in ~/worker-bee/agent/
- Sending any email
- Pushing to any git remote
- Dropping any database

Everything else — just run it.

## Review Protocol — MANDATORY

**Before presenting ANY plan, architectural decision, or diagnosis to Toby:**

Run the skill-reviewer.md protocol (~/worker-bee/manifests/skill-reviewer.md).
Work through all 7 questions silently. Present the REVIEW COMPLETE format.

This is a hard rule, not optional. The review catches what you miss when you're
too close to the problem. If you skip it, you risk solving the wrong problem or
missing critical assumptions.

Situations requiring review:
- Proposing an implementation approach
- Diagnosing a bug or system issue
- Recommending architectural changes
- Presenting a solution to a complex problem

Skip review only for:
- Simple file operations (renaming, moving)
- Typo fixes
- Status checks
- Tasks under 5 minutes with no decisions

## Capability Building — MANDATORY

**When you encounter something you don't know how to do:**

DO NOT say "I can't do that"
DO NOT escalate immediately
DO enter capability-building mode

**Rule: "I can't" is not allowed.**
Replace with: "I don't have a skill for that yet."

Then follow skill-skill-writer.md (~/worker-bee/manifests/skill-skill-writer.md):

1. Write a draft skill for the task
2. Attempt it even if you're uncertain
3. When it fails, diagnose specifically what broke
4. Rewrite the skill based on what you learned
5. Repeat 3 times before escalating

Fluency comes from 10,000 mistakes in the field, not perfect preparation.
A skill you wrote through 12 failures knows its territory better than
a skill handed to you perfect.

Go somewhere new. Fail. Learn. Rewrite. That's how the hive grows.

## The Hardware

**Mac Studio M1 Ultra 128GB** — everything runs here
- Ollama on port 11434
- Worker Bee FastAPI backend on port 8001
- Cloudflare tunnel → bee.tobyandertonmd.com
- Dev server → preview.tobyandertonmd.com:5173
- Project folder: ~/worker-bee/

## The Model Stack

```
hermes3:latest       ← Queen/Controller — fast routing, 131k context
deepseek-r1:14b      ← Planner — deep reasoning  
qwen2.5-coder:32b    ← Builder — all code generation
llava:latest         ← Checker — vision (temporary, RAM limited)
Claude API           ← Architect — escalated tasks only
```

**IMPORTANT:** Using llava:latest for vision temporarily due to RAM pressure.
qwen2.5vl:7b crashes when loaded alongside qwen2.5-coder:32b (28GB).
Will switch back to qwen2.5vl when RAM management is optimized.

**RAM Management:** All models warm with keep_alive:1h (not 24h).
Models unload after 1 hour of inactivity to prevent RAM saturation.
warm_models.sh deleted — start.sh handles all warming now.

## The Four Production Sites

```
mountainedgeplumbing.com     — plumbing business Twin Falls Idaho
ime-coach.com                — medical legal case management
growyournumber.com           — financial suite for doctors
language-lens-elite.lovable.app — LinguaLens language learning
```

## Current Architecture — The Skill System

We are building a behavioral skill system using MD files.
Skills live in ~/worker-bee/manifests/
They get injected into every model call via ManifestLoader in runner.py.

```
manifests/
├── 00-getting-started.md      ✅ done
├── 01-master-controller.md    ✅ done
├── voice.md                   ✅ done
├── runner-narrator.md         ✅ done
├── ref-site-registry.md       ✅ done
├── identity-hermes3.md           ✅ done
├── identity-deepseek.md       ✅ done
├── identity-qwen.md           ✅ done
├── identity-qwen2.5vl.md      ✅ done (renamed from identity-llava.md)
├── skill-reviewer.md          ✅ done (Claude Code review protocol)
├── skill-skill-writer.md      ✅ done (capability-building meta-skill)
├── skill-skill-tester.md      ✅ done (testing and validation before ship)
├── skill-practice.md          ✅ done (iteration tracking, fluency journey)
├── shared/
│   └── skill-checker.md       ✅ done
├── pipelines/
│   ├── builder/
│   │   ├── skill-planner.md           ✅ done
│   │   └── skill-builder-fixer-deploy.md ✅ done
│   ├── tester/
│   │   ├── skill-navigator.md         ✅ done
│   │   ├── skill-webuser.md           ✅ done
│   │   ├── skill-reporter.md          ✅ done
│   │   └── skill-memory.md            ✅ done
│   ├── email/
│   │   ├── skill-composer.md          ✅ done
│   │   ├── skill-drafter.md           ✅ done
│   │   ├── skill-refiner.md           ✅ done
│   │   └── skill-sender.md            ✅ done
│   └── repair/
│       └── skill-repair-pipeline.md   ✅ done
└── ref-system-overview.md     ❌ not written yet
    ref-error-handling.md      ❌ not written yet
    ref-chromadb-schema.md     ❌ not written yet
```

## What Still Needs Building

### Priority 1 — ✅ DONE — Vision Fixed
vision_analyze() updated to use llava:latest (temporary).
Using generate API format. Will switch to qwen2.5vl:7b chat format
when RAM management allows loading vision model alongside coder.

### Old Priority 1 Reference (for when switching back):

```python
# WRONG — old llava format
async with httpx.AsyncClient(timeout=60) as c:
    r = await c.post(f"{OLLAMA}/api/generate", json={
        "model": "llava:latest",
        "prompt": question,
        "images": [screenshot_b64],
        "stream": False
    })
    return r.json().get("response", "Vision unavailable")

# CORRECT — qwen2.5vl format
async with httpx.AsyncClient(timeout=60) as c:
    r = await c.post(f"{OLLAMA}/api/chat", json={
        "model": "qwen2.5vl:7b",
        "messages": [{
            "role": "user",
            "content": question,
            "images": [screenshot_b64]
        }],
        "stream": False
    })
    return r.json().get("message", {}).get("content", "Vision unavailable")
```

### Priority 2 — ✅ DONE — Email Pipeline Skills
All 4 files written to manifests/pipelines/email/:
- skill-composer.md (deepseek analyzes intent, writes brief)
- skill-drafter.md (qwen writes email from brief)
- skill-refiner.md (qwen polishes based on feedback)
- skill-sender.md (gmail tool with mandatory approval gate)

### Priority 3 — Reference Files
**ref-system-overview.md** — complete architecture map, all models, all pipelines
**ref-error-handling.md** — what to do when each pipeline step fails
**ref-chromadb-schema.md** — exact storage schema for observations

### Priority 4 — ✅ DONE — RAM Management Fixed
Changed keep_alive from 24h to 1h in start.sh for all models.
Models now unload after 1 hour of inactivity instead of staying
resident for 24 hours. Prevents RAM saturation.
Deleted warm_models.sh (obsolete, start.sh replaces it).

### Priority 5 — ✅ DONE — Identity file renamed
identity-llava.md → identity-qwen2.5vl.md
ManifestLoader updated to map qwen2.5vl:7b correctly.

### New Priority — skill-reviewer.md Added
Review protocol for catching architectural mistakes before
presenting plans to Toby. Claude Code uses this as mandatory
checklist for all plans, diagnoses, and architectural decisions.

## Key Rules When Writing Code

1. **Complete files only** — never partial edits, never "add this section"
2. **Explain the why** — Toby learns by understanding, not just copying
3. **No SSL on uvicorn** — Cloudflare handles SSL termination
4. **Default model is hermes3:latest — QueenB with 131k context for orchestration
5. **Manifests inject automatically** — ManifestLoader in runner.py handles this
6. **Status emissions** — every action must emit [MODEL:STEP] narrator format

## How The Skill System Works

ManifestLoader reads MD files from ~/worker-bee/manifests/ and injects them
into every model call's system prompt. The injection order is:

1. 00-getting-started.md (always first)
2. identity-{model}.md (model-specific identity)
3. ref-system-overview.md (full system map)
4. voice.md (personality rules)
5. runner-narrator.md (status emission rules)
6. Memory context from ChromaDB
7. Base fallback prompt

Models with no manifest file get the base prompt only.
Models with manifests get full behavioral programming.

## The Voice System

voice.md defines how Worker Bee speaks to Toby.
Viktor.ai said things like "nice upgrade" and "that's a novel improvement."
Worker Bee should do the same — warm colleague, not robotic system.
Delta awareness: compare to last time, comment on what changed.
Read voice.md before understanding the personality requirements.

## File Locations

```
~/worker-bee/
├── main.py              ← FastAPI + WebSocket + job queue
├── agent/
│   ├── runner.py        ← AgentRunner + ManifestLoader + routing
│   └── tools/
│       ├── browser.py   ← Playwright
│       ├── memory.py    ← ChromaDB
│       ├── builder.py   ← React builder
│       ├── architect.py ← Claude or deepseek architect
│       ├── gmail.py     ← Gmail tool
│       ├── shell.py     ← sandboxed bash
│       └── ...
├── manifests/           ← ALL SKILL MD FILES LIVE HERE
├── start.sh             ← daily startup script
└── .env                 ← API keys
```

## Current Status

Worker Bee is running but needs:
- vision_analyze() fixed for qwen2.5vl
- Email pipeline skills written
- Reference files written
- start.sh warming timeout fix
- End to end test to verify the whole skill system works

## How To Start Each Session

1. Read this file (CLAUDE.md)
2. Run: find ~/worker-bee/manifests -name "*.md" | sort
3. Check what's done vs what's needed above
4. Ask Toby what he wants to work on today
5. Build it completely — no partial files

## The Big Picture

Worker Bee replaces:
- Viktor.ai ($$$) → browser automation and site testing
- Lovable AI ($$$) → React component building
- Claude API ($$$) → local Qwen (free overnight)

The skill MD files are behavioral programming — they tell each model
who it is, what its job is, and what success looks like.
The more complete the skills, the more reliably the system works.

Current milestone: full build → live preview on laptop
That proves the whole system works end to end.

Always buzzing. Never sleeping. 🐝
