# Hermes Agent Skills Analysis & Adoption Plan

## Executive Summary

Pulled and analyzed 8 priority Hermes Agent skills. **3 immediate adoptions, 2 adaptations, 3 inspirations.**

**Best finds:**
1. **systematic-debugging** — Superior to our repair pipeline, adopt immediately
2. **subagent-driven-development** — New pattern for Worker Bee parallelization
3. **writing-plans** — Better brief format than Scout's current output

**GEPA optimizer** — Skill self-evolution system. Can adapt for Worker Bee's practice loop.

---

## Skill-by-Skill Comparison

### 1. systematic-debugging vs skill-repair-pipeline.md

**Hermes:** 367-line comprehensive debugging protocol
- 4 phases: Root Cause → Pattern Analysis → Hypothesis → Implementation
- Iron Law: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"
- Rule of Three: After 3 failed fixes, question the architecture
- Phase 1 checklist: error messages, reproduction, recent changes, evidence gathering, data flow tracing
- Systematic hypothesis testing (one variable at a time)
- Integration with test-driven-development skill

**Worker Bee:** 157-line pipeline-specific repair process
- 5 steps: Diagnose → Inspect → (missing hypothesis phase) → Fix → Verify
- Focused on site issues (visual, functional, performance, data)
- Uses ref-site-registry.md for known fragile points
- Playwright inspection for live site validation
- Maximum 2 repair cycles before escalating

**Comparison:**

| Aspect | Hermes systematic-debugging | Worker Bee skill-repair-pipeline |
|--------|---------------------------|--------------------------------|
| **Scope** | General code debugging | Site-specific repair |
| **Root cause depth** | ✅ Deep (4 phases) | ⚠️ Shallow (probable causes list) |
| **Hypothesis testing** | ✅ Scientific method | ❌ Missing |
| **Evidence gathering** | ✅ Multi-component tracing | ⚠️ Basic (Playwright screenshots) |
| **Failure handling** | ✅ Rule of Three + architecture questioning | ⚠️ 2 cycles then escalate |
| **Integration** | ✅ Links to TDD skill | ⚠️ Pipeline-only |

**Verdict: Hermes is superior**

Worker Bee's repair pipeline is too shallow. It jumps to "probable causes" without systematic investigation.

**Recommendation: ADOPT systematic-debugging**

Create `manifests/skill-systematic-debugging.md` adapted for Worker Bee:
- Keep the 4-phase structure
- Add Scout → Builder → Watcher orchestration
- Integrate with ref-site-registry.md for site context
- Add status emissions for QueenB tracking

---

### 2. github-pr-workflow vs (missing)

**Hermes:** 250+ line GitHub PR workflow
- PR creation, review, merge, conflict resolution
- Integration with gh CLI
- Draft PR → request review → address feedback → merge
- Conflict resolution strategies
- PR description templates

**Worker Bee:** ❌ No GitHub PR skill

**Current state:** Worker Bee commits and pushes, but no PR workflow.

**Verdict: NEEDED**

Jay will be collaborating remotely. PR workflow is essential.

**Recommendation: ADAPT and ADD**

Create `manifests/skill-github-pr.md`:
- QueenB-driven (she coordinates PR creation)
- After build complete + git push → create PR
- Use gh CLI (already in CLAUDE.md examples)
- PR body includes: build summary, files changed, test results
- Tag Jay for review

**Integration point:** After `github_pushed` message in runner.py, trigger PR creation.

---

### 3. test-driven-development vs (missing)

**Hermes:** 300+ line TDD workflow
- RED: Write failing test first
- GREEN: Minimal implementation to pass
- REFACTOR: Improve without changing behavior
- Test structure templates
- Integration with systematic-debugging
- Test organization patterns

**Worker Bee:** ⚠️ Builder writes code but no TDD enforcement

**Current state:** Scout plans, Builder builds, Watcher checks visually. No unit tests.

**Verdict: MISSING but NEEDED**

Worker Bee builds React components. Should have test-driven approach.

**Recommendation: ADAPT for React/Playwright context**

Create `manifests/skill-tdd.md`:
- Scout's brief includes test criteria
- Builder writes Playwright test first (visual/functional)
- Builder implements component
- Watcher runs Playwright test to verify
- Integration with existing Builder pipeline

**Challenge:** React component testing is different from backend TDD. Adapt to Playwright E2E approach.

---

### 4. writing-plans vs Scout's brief format

**Hermes:** Comprehensive planning skill
- Bite-sized tasks (2-5 minutes each)
- Complete code examples in plan
- Exact file paths with line numbers
- Testing commands per task
- TDD steps embedded in each task
- Assumes implementer has zero context

**Worker Bee Scout:** Technical brief format
- Component name, file path, purpose
- Technology stack, props, data, behavior
- Edge cases, success criteria
- Hard gate: "complete enough that Builder doesn't ask questions"

**Comparison:**

| Aspect | Hermes writing-plans | Worker Bee Scout brief |
|--------|---------------------|----------------------|
| **Task granularity** | ✅ Bite-sized (2-5 min) | ⚠️ Whole component |
| **Code examples** | ✅ Complete code snippets | ❌ Description only |
| **Testing steps** | ✅ TDD per task | ❌ Success criteria only |
| **File paths** | ✅ Exact paths + line numbers | ✅ Exact paths |
| **Commit strategy** | ✅ Commit per task | ⚠️ One commit per build |

**Verdict: Hermes has better structure**

Scout's briefs are high-level. Hermes plans are implementation-ready.

**Recommendation: EVOLVE Scout's brief format**

Update `manifests/pipelines/builder/skill-planner.md`:
- Break components into sub-tasks (file structure → props → behavior → styling)
- Include code snippets for complex patterns
- Add testing steps (Playwright checks per sub-task)
- Commit strategy (git add per sub-task completion)

**Format upgrade:**
```markdown
COMPONENT: ContactForm

TASK 1: Create component file structure
FILE: src/components/ContactForm.tsx
CODE:
```tsx
export function ContactForm() {
  return <div>ContactForm placeholder</div>
}
```
TEST: Playwright should see "ContactForm placeholder"
COMMIT: "feat: add ContactForm scaffolding"

TASK 2: Add form fields
[specific props, state, TypeScript types with code]
TEST: [Playwright checks for input fields]
COMMIT: "feat: add ContactForm fields"
```

---

### 5. subagent-driven-development vs (new pattern)

**Hermes:** Parallel execution with fresh context per task
- Extract all tasks from plan upfront
- Dispatch `delegate_task` per task
- Two-stage review: spec compliance → code quality
- Fresh subagent = no accumulated context confusion
- Automated review between tasks

**Worker Bee:** ❌ No subagent pattern (yet)

**Current architecture:**
- QueenB routes → Scout → Builder → Watcher (sequential)
- No parallel task execution
- Single Builder handles entire component

**Verdict: NEW CAPABILITY for Worker Bee**

This is exactly what Worker Bee needs for autonomous overnight operation.

**Recommendation: IMPLEMENT subagent pattern**

**New architecture:**
```
QueenB receives: "Build landing page with hero, features, CTA, footer"
    ↓
Scout creates plan with 4 independent tasks:
    - TASK 1: Hero component
    - TASK 2: Features grid
    - TASK 3: CTA button
    - TASK 4: Footer
    ↓
QueenB spawns 4 parallel Builder subagents:
    - Builder-1 builds Hero (own context)
    - Builder-2 builds Features (own context)
    - Builder-3 builds CTA (own context)
    - Builder-4 builds Footer (own context)
    ↓
Watcher checks each independently
    ↓
Builder-1 fixes Hero issues (if any)
    ↓
QueenB assembles final App.tsx importing all components
```

**Benefits:**
- 4x faster builds (parallel vs sequential)
- Fresh context = no confusion between tasks
- Isolated failures (Hero bug doesn't block Features)
- Perfect for autonomous overnight batches

**Implementation:**
- Add `delegate_task` equivalent in runner.py
- QueenB spawns multiple AgentRunner instances
- Each gets task + fresh context
- Parallel execution via asyncio.gather()

**File:** `manifests/skill-subagent-orchestration.md`

---

### 6. ocr-and-documents vs (missing but CRITICAL)

**Hermes:** OCR and document processing skill
- Extracts text from PDFs, images, screenshots
- Uses native MCP OCR tools
- Document structure parsing
- Integration with note-taking and research skills

**Worker Bee:** ❌ No OCR capability

**Why CRITICAL for ime-coach.com:**
- Medical legal case management
- Needs to read medical records (PDFs)
- Extract patient info, dates, diagnoses
- Build case timelines from documents

**Verdict: ESSENTIAL for ime-coach.com**

This unlocks a major use case.

**Recommendation: ADD OCR skill + MCP integration**

Create `manifests/skill-ocr.md`:
- Use Claude Code's built-in OCR (Read tool can read PDFs)
- Extract text from uploaded medical records
- Parse structure (patient name, date of service, diagnosis codes)
- Store in case database

**Integration:**
- Scout plans document processing pipeline
- Builder writes extraction logic
- Watcher verifies extracted data against source

**MVP:** Read PDF → extract ICD-10 codes → match against mcp__claude_ai_ICD-10_Codes

---

### 7. domain-intel vs site health monitoring

**Hermes:** Domain intelligence gathering
- WHOIS lookup
- DNS records analysis
- SSL certificate checks
- Domain history
- Security scanning

**Worker Bee:** ⚠️ Partial via TESTER pipeline

**Current:** Worker Bee tests user journeys but doesn't do infrastructure monitoring.

**Verdict: USEFUL but not urgent**

**Recommendation: LOW PRIORITY**

Could add to TESTER pipeline for production monitoring:
- Check SSL certificates before expiry
- Monitor DNS records for hijacking
- Verify site uptime
- Security headers validation

**File:** `manifests/skill-domain-health.md` (future)

---

### 8. google-workspace vs Gmail MCP approach

**Hermes:** Google Workspace integration
- Gmail (read, send, draft, search)
- Google Drive (upload, download, share)
- Google Calendar (events, scheduling)
- Google Sheets (read, write, formulas)

**Worker Bee:** ⚠️ Gmail MCP only (via Claude API escalation)

**Current:** `manifests/skill-gmail.md` requires Claude API escalation for MCP.

**Comparison:**

| Feature | Hermes google-workspace | Worker Bee skill-gmail |
|---------|------------------------|----------------------|
| Gmail | ✅ Full access | ⚠️ Claude API only |
| Drive | ✅ Included | ❌ Missing |
| Calendar | ✅ Included | ❌ Missing |
| Sheets | ✅ Included | ❌ Missing |

**Verdict: Hermes is more complete**

But Worker Bee's MCP approach is correct (native Claude integration).

**Recommendation: EXPAND skill-gmail.md**

Add Google Drive + Calendar sections:
- Drive: Upload build artifacts, share with Jay
- Calendar: Schedule builds, deployment windows
- Sheets: Build logs, test results tracking

Keep the Claude API escalation pattern (MCP is the right approach).

---

## GEPA Optimizer Analysis

### What It Is

**GEPA = Genetic-Pareto Prompt Evolution**

- Reads execution traces to understand WHY skills fail
- Generates candidate variants (mutations)
- Evaluates variants against test suite
- Selects best performers via Pareto frontier
- Iterates until convergence
- Cost: $2-10 per optimization run

### How It Works

```
Current skill file
    ↓
Generate eval dataset (synthetic or from session history)
    ↓
GEPA Optimizer
    ├─► Mutation: Add missing error handling
    ├─► Mutation: Improve prompt clarity
    ├─► Mutation: Add example workflows
    └─► Mutation: Remove redundant sections
    ↓
Evaluate each variant
    ├─► Run test suite
    ├─► Check size limits (≤15KB)
    ├─► Measure task success rate
    └─► Semantic preservation check
    ↓
Pareto selection (best trade-offs)
    ↓
Best variant → PR for human review
```

### Integration with Worker Bee

**Current:** Worker Bee has `manifests/practice/` with skill iteration tracking.

**Missing:** Automated evolution. Practice sessions are manual.

**GEPA could automate:**
1. Read `skill-planner.practice.md` (current iteration)
2. Generate eval cases from `learning-sessions/`
3. Propose skill improvements based on failures
4. Test against Worker Bee's build success rate
5. Output improved skill-planner.md v2.0

### Adaptation Strategy

**Phase 1: Manual GEPA for top skills**
- Run GEPA on skill-planner.md using Worker Bee's failed builds as eval data
- Run GEPA on skill-builder.md using code quality issues as eval data
- Human review each output

**Phase 2: Automated nightly evolution**
- GEPA runs every night after practice loop
- Reads failed builds from ChromaDB
- Evolves 1 skill per night
- Creates PR to worker-bee-backend
- Toby reviews in morning

**Phase 3: Continuous improvement**
- GEPA + practice loop = closed learning system
- Skills improve based on real failures
- No manual skill updates needed

### Cost Analysis

**GEPA cost:** $2-10 per skill evolution  
**Worker Bee skill count:** ~15 core skills  
**Monthly cost:** $30-150 for nightly evolution (1 skill/night)

**vs. Manual iteration:**
- Toby writes learning sessions by hand
- Claude suggests improvements
- Worker Bee practices manually
- Time: hours per skill iteration

**GEPA ROI:** Automation worth the $30-150/month.

### Implementation Plan

**Immediate:**
1. Clone hermes-agent-self-evolution repo
2. Point at worker-bee-backend repo
3. Run GEPA on skill-planner.md with synthetic eval
4. Review output, compare to current version

**Short-term:**
5. Integrate with ChromaDB (use failed builds as eval data)
6. Add to practice loop (nightly skill evolution)
7. PR creation for Toby review

**Long-term:**
8. Full autonomous evolution pipeline
9. Multi-skill optimization (evolve Scout + Builder + Watcher together)
10. Architecture co-evolution (evolve manifests + runner.py simultaneously)

---

## Adoption Roadmap

### Immediate (This Week)

**1. Add systematic-debugging skill**
- File: `manifests/skill-systematic-debugging.md`
- Adapted for Worker Bee with Scout → Builder → Watcher orchestration
- Replace skill-repair-pipeline.md (deprecated)
- Update 01-master-controller.md routing

**2. Evolve Scout's brief format**
- Update `manifests/pipelines/builder/skill-planner.md`
- Add bite-sized task breakdown
- Include code snippets
- Add per-task commit strategy

**3. Test GEPA on one skill**
- Clone hermes-agent-self-evolution
- Run on skill-planner.md
- Review output quality
- Decision: proceed with automation?

### Short-term (This Month)

**4. Add github-pr-workflow**
- File: `manifests/skill-github-pr.md`
- Integration: After `github_pushed` → create PR
- Tag Jay for review

**5. Add TDD skill**
- File: `manifests/skill-tdd.md`
- Adapt for React/Playwright context
- Builder writes test first, then component

**6. Implement subagent pattern**
- File: `manifests/skill-subagent-orchestration.md`
- Add `delegate_task` to runner.py
- QueenB spawns parallel Builders
- Test with multi-component builds

### Medium-term (Next Quarter)

**7. Add OCR skill**
- File: `manifests/skill-ocr.md`
- PDF reading via Read tool
- ICD-10 code extraction for ime-coach.com

**8. Expand Google Workspace**
- Update `manifests/skill-gmail.md`
- Add Drive, Calendar, Sheets sections

**9. Automate GEPA nightly**
- Integrate with practice loop
- Nightly skill evolution
- PR creation for review

### Long-term (Next Year)

**10. Full autonomous evolution**
- Multi-skill co-optimization
- Architecture evolution (manifests + code)
- Continuous improvement without manual intervention

---

## Key Metrics

### Current State
- **Skills:** 15 core skills
- **Success rate:** ~70% (builds work, some issues)
- **Manual iteration:** Yes (Toby writes learning sessions)
- **Parallel execution:** No (sequential pipeline only)
- **GitHub workflow:** Push only (no PRs)

### Target State (6 months)
- **Skills:** 25+ skills (add debugging, TDD, OCR, GitHub PR, etc.)
- **Success rate:** >90% (systematic debugging + evolved skills)
- **Manual iteration:** No (GEPA automates)
- **Parallel execution:** Yes (subagent pattern)
- **GitHub workflow:** Full PR cycle (create → review → merge)

---

## Bottom Line

**Hermes Agent skills are gold.**

Best finds:
1. **systematic-debugging** → Immediately replace our repair pipeline
2. **subagent-driven-development** → Unlock parallel builds (4x faster)
3. **writing-plans** → Upgrade Scout's brief format

**GEPA optimizer:**
- Can automate Worker Bee's practice loop
- $30-150/month for nightly skill evolution
- Worth it vs manual iteration time

**Action:**
1. Adopt systematic-debugging this week
2. Test GEPA on skill-planner.md
3. Implement subagent pattern for parallel builds
4. Evolve Scout's brief format using writing-plans structure

Files pulled and ready for adaptation:
- `~/worker-bee/hermes-skills-analysis/1-systematic-debugging.md`
- `~/worker-bee/hermes-skills-analysis/2-github-pr-workflow.md`
- `~/worker-bee/hermes-skills-analysis/3-test-driven-development.md`
- `~/worker-bee/hermes-skills-analysis/4-writing-plans.md`
- `~/worker-bee/hermes-skills-analysis/5-subagent-driven-development.md`
- `~/worker-bee/hermes-skills-analysis/6-ocr-and-documents.md`
- `~/worker-bee/hermes-skills-analysis/7-domain-intel.md`
- `~/worker-bee/hermes-skills-analysis/8-google-workspace.md`

Next step: Adapt systematic-debugging for Worker Bee and test.
