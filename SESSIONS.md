# Session History

## Session: 2026-04-25 (Night) — The Practice System

**Duration:** ~5 hours (21:00 - 02:55)
**Status:** Complete
**Milestone:** Iteration #1 logged, fluency journey begins

---

### What We Built

**Core Skills Created:**
1. **skill-skill-writer.md** (8.1K) — Capability building meta-skill
   - Teaches bee to write skills when encountering unknown tasks
   - "10,000 mistakes is the curriculum" philosophy
   - REFINED vs SPAWNED decision tree
   - Updated itself from tonight's learning (execution path section added)

2. **skill-skill-tester.md** (10K) — Testing and validation before ship
   - Defines what "proof" means for behavioral skills
   - Minimum test coverage: happy path + all failure modes
   - Test file format: skill-X.tests.md
   - Testing is the permission gate for auto-writing

3. **skill-practice.md** (6.0K) — Iteration tracking, fluency journey
   - 10,000 iterations = fluency target
   - Success rate vs approval rate (the gap metric)
   - Beginner → Practicing → Proficient → Fluent → Master tiers
   - 2-year timeline for core skills
   - REFINE vs SPAWN decision tree based on pattern frequency

**Practice Files Created:**
- **skill-planner.practice.md** (5.1K) — Iteration #1 logged (2026-04-25 02:26)
- **skill-planner.tests.md** (3.7K) — 3 passing validation tests

**System Updates:**
- **CLAUDE.md** — Added Review Protocol (mandatory), Capability Building Protocol (mandatory)
- **builder.py:154** — Fixed tuple unpacking bug (architect returns tuple, was treating as string)
- **skill-skill-writer.md** — Added "Before You Test: Know The Execution Path" section

---

### What We Tested

**Builder Pipeline End-to-End:**
- Task: "Add a blue header that says 'Welcome to the simple-build project'"
- deepseek-r1:14b created 1,386 char architectural brief
- qwen2.5-coder:32b built from brief successfully
- 4 files generated (main.tsx, index.css, App.tsx, Hero.tsx)
- Result: ✅ SUCCESS, logged as iteration #1

**Missing Skill Test:**
- Removed skill-planner.md from manifests/
- Ran builder task
- Discovered: direct tool calls bypass ManifestLoader entirely
- Learning documented in skill-skill-writer.md

---

### Key Decisions

**Three-File Skill System:**
- skill-X.md — the skill itself (instructions)
- skill-X.tests.md — validation testing (proof it works)
- skill-X.practice.md — iteration tracking (fluency journey)

**Tiered Write Permissions:**
- "What I Learned" sections → auto-write (append-only)
- New skills with passing tests → auto-write
- Core instruction changes with passing tests → auto-write if you own skill, pending/ if not
- Testing is the gate, not permission

**Approval Rate Tracking:**
- Every task gets Toby feedback: 👍 👎 ⏳
- Gap = Success Rate - Approval Rate
- Gap shows where bee is technically correct but missing intent
- "The gap is the curriculum for the next 10,000 iterations"

**Fluency Timeline:**
- Target: 10,000 iterations per skill
- Core skills (planner, builder, diagnose): 2-year journey at 15 iterations/day
- Projected fluent: 2028-02-14
- Iteration #1 starts tonight, not theoretical future

---

### Files Changed

**Created:**
- `/manifests/skill-skill-writer.md`
- `/manifests/skill-skill-tester.md`
- `/manifests/skill-practice.md`
- `/manifests/pipelines/builder/skill-planner.practice.md`
- `/manifests/pipelines/builder/skill-planner.tests.md`
- `/test_builder_pipeline.py`
- `/test_missing_skill.py`

**Modified:**
- `/agent/tools/builder.py` (line 154: tuple unpacking fix)
- `/agent/runner.py` (added MODEL_CONTEXT_SIZES, get_num_ctx(), num_ctx to all API calls)
- `/start.sh` (keep_alive: 24h → 1h, added num_ctx to warming)
- `/CLAUDE.md` (added Review Protocol, Capability Building Protocol, updated manifest list)

**Deleted:**
- `/warm_models.sh` (obsolete, start.sh replaces it)

---

### What's Next

**Not Implemented (Future Work):**
- UI thumbs up/down buttons in main.py for feedback collection
- Write-back system in runner.py for SKILL_UPDATE detection
- Automatic practice log updates after each production run
- skill-capability-check.md (routes to skill-skill-writer when skill missing)

**Pending Priority:**
- Reference files (ref-system-overview.md, ref-error-handling.md, ref-chromadb-schema.md)
- End-to-end test through WebSocket (not direct tool call)
- RAM monitoring dashboard

---

### Metrics

**RAM Optimization Results:**
- Total VRAM reduced: 84.3GB → 45.6GB (saved 38.7GB)
- deepseek-r1:14b: 42.2GB → 10.1GB (saved 32.1GB via num_ctx: 8192)
- Models unload after 1h idle (was 24h)

**Test Results:**
- Builder pipeline: ✅ PASS
- Vision models (llava, qwen2.5vl): ✅ BOTH WORK (ghost chase resolved)
- skill-planner iteration #1: ✅ SUCCESS, 👍 APPROVED

**Skills Status:**
- Total skills: 20+ files in manifests/
- Practice logs: 1 (skill-planner.practice.md)
- Test files: 2 (skill-planner.tests.md, skill-planner.tests.md)
- Meta-skills: 4 (reviewer, skill-writer, skill-tester, practice)

---

### Session Notes

Tonight was the beginning of the fluency journey. Iteration #1 logged at 02:26.
The hive in 2 years starts counting from this moment.

The practice system is complete. The bee now has:
- A way to build new skills (skill-skill-writer.md)
- A way to test them (skill-skill-tester.md)
- A way to track fluency over time (skill-practice.md)
- Iteration #1 documented permanently

Not theoretical. Real practice starting now.
