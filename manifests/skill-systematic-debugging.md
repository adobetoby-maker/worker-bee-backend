---
name: skill-systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior. 4-phase root cause investigation — NO fixes without understanding the problem first.
version: 1.0.0
metadata:
  pipeline: repair
  step: 1-4
  model: deepseek-r1:14b (diagnosis), qwen2.5-coder:32b (fix), llava:latest (verification)
  hands_off_to: complete-or-escalate
  tags: [debugging, troubleshooting, root-cause, systematic, repair]
  adapted_from: hermes-agent/systematic-debugging v1.1.0
---

# skill-systematic-debugging — Systematic Root Cause Investigation

**Pipeline:** REPAIR
**Models:** Scout (deepseek) diagnoses → Builder (qwen) fixes → Watcher (llava) verifies
**Called by:** 01-master-controller when build fails, site breaks, or tests fail
**Hands off to:** QueenB for completion or Claude escalation

---

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Random fixes waste time and create new bugs.  
Quick patches mask underlying issues.  
Symptom fixes are failure.

**ALWAYS find root cause before attempting fixes.**

If you haven't completed Phase 1, you cannot propose fixes.

---

## Routing Triggers

QueenB routes to this skill when:
- **Keywords:** "broken", "failing", "bug", "error", "not working", "unexpected"
- **Context:** Build failed, site issue reported, test failure, visual regression
- **Prerequisites:** Issue has been observed (screenshot, error message, or user report)
- **Escalate if:** 3+ fixes failed (question architecture), unknown tech stack, security vulnerability

---

## Common Mistakes (What NOT To Do)

1. **Don't jump to fixes** — "I see the problem, let me fix it" means you haven't found root cause
2. **Don't try multiple fixes at once** — Can't isolate what worked, causes new bugs
3. **Don't skip reproduction** — If you can't reproduce it, you can't verify the fix
4. **Don't attempt fix #4** — After 3 failures, question the architecture instead
5. **Don't trust "obvious" solutions** — Obvious symptoms rarely have obvious root causes
6. **Don't skip the test** — Untested fixes don't stick, regressions happen
7. **Don't fix symptoms** — Trace upstream to where bad data originates

---

## When To Use This Skill

Use for ANY technical issue:
- Test failures (Playwright, unit tests)
- Site bugs (visual, functional, performance)
- Build failures (compile errors, dependencies)
- Integration issues (API, database, third-party)
- Unexpected behavior (user reports, Watcher findings)

**Use ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (systematic is faster than thrashing)
- Someone wants it fixed NOW (rushing guarantees rework)

---

## Announce At Start

**Scout announces:**
"I am using skill-systematic-debugging to investigate [issue]. Following 4-phase protocol: Root Cause → Pattern → Hypothesis → Implementation."

---

## Follow runner-narrator.md for all status emissions.

---

## The Four Phases

Complete each phase before proceeding to the next.  
QueenB tracks phase completion via status emissions.

---

## Phase 1: Root Cause Investigation (Scout)

**Model:** deepseek-r1:14b  
**Goal:** Understand WHAT is broken and WHY

### Step 1 — Read Error Messages Completely

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:**
```
Emit: [SCOUT:READING_ERRORS] analyzing error messages
Read build logs, browser console, test output
Extract: exact error text, stack trace, line numbers
```

### Step 2 — Check Recent Changes

What changed that could cause this?

**Action:**
```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.tsx | head -100
```

**Emit:** `[SCOUT:GIT_HISTORY] recent changes reviewed`

### Step 3 — Check Site Registry for Known Issues

Read ref-site-registry.md for the affected site.  
Known fragile points often cause regressions.

**Emit:** `[SCOUT:REGISTRY] known fragile points reviewed`

### Step 4 — Reproduce Consistently

Can you trigger it reliably?
- Exact steps to reproduce
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**For site issues:**
```
Use Playwright to reproduce:
1. Navigate to affected page
2. Take "before" screenshot
3. Perform action that triggers bug
4. Take "after" screenshot
5. Capture browser console errors
```

**Emit:** `[SCOUT:REPRODUCED] issue reproduced consistently` or `[SCOUT:CANNOT_REPRODUCE] gathering more data`

### Step 5 — Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (React → API → database, build → deploy → runtime):**

Add diagnostic instrumentation at EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.  
Then analyze evidence to identify the failing component.  
Then investigate that specific component.

**Emit:** `[SCOUT:EVIDENCE] gathered logs from [N] components`

### Step 6 — Trace Data Flow

**WHEN error is deep in the call stack:**

Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:**
```typescript
// Find where the function is called
search in project for: functionName(

// Find where the variable is set
search in project for: variableName\s*=
```

**Emit:** `[SCOUT:TRACED] data flow traced to [origin]`

### Phase 1 Completion Checklist

Scout must complete ALL before handing to Builder:

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Site registry checked for known issues
- [ ] Evidence gathered (logs, screenshots, state)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**Emit:** `[SCOUT:PHASE1_COMPLETE] root cause identified: [hypothesis]`

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis (Scout)

**Goal:** Find the pattern before fixing

### Step 1 — Find Working Examples

Locate similar working code in the same codebase:
- What works that's similar to what's broken?
- Scan existing components for patterns

**Action:**
```typescript
// Search for similar patterns in working code
search in src/ for: similar_pattern
```

**Emit:** `[SCOUT:PATTERNS] found [N] working examples`

### Step 2 — Compare Against References

If implementing a pattern:
- Read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

**For React components:**
- Check Tailwind docs for CSS patterns
- Check React docs for hooks usage
- Check existing Worker Bee builds for patterns

**Emit:** `[SCOUT:REFERENCES] reference patterns reviewed`

### Step 3 — Identify Differences

What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

**Emit:** `[SCOUT:DIFFERENCES] identified [N] key differences`

### Step 4 — Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

**For React components:**
- Props from parent components
- Context providers
- CSS imports
- Build tool config (Vite, TypeScript)

**Emit:** `[SCOUT:DEPENDENCIES] dependencies mapped`

**Emit:** `[SCOUT:PHASE2_COMPLETE] pattern analysis complete`

---

## Phase 3: Hypothesis and Testing (Scout → Builder → Watcher)

**Goal:** Scientific method — test hypothesis before full fix

### Step 1 — Form Single Hypothesis (Scout)

State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague
- One hypothesis at a time

**Emit:** `[SCOUT:HYPOTHESIS] testing hypothesis: [statement]`

**Hand to Builder:**
```
HYPOTHESIS: [X is the root cause because Y]

MINIMAL TEST:
- File to change: [exact path]
- Smallest possible change: [one-line or minimal code]
- Expected result: [what should happen if hypothesis is correct]

DO NOT make other changes. Test this ONE thing.
```

### Step 2 — Test Minimally (Builder)

**Model:** qwen2.5-coder:32b

Receive hypothesis from Scout.  
Make the SMALLEST possible change to test it.
- One variable at a time
- Don't fix multiple things at once

**Emit:** `[BUILDER:TESTING] applying minimal test change`

Apply change → output complete file

**Emit:** `[BUILDER:TEST_APPLIED] change applied to [file]`

### Step 3 — Verify (Watcher)

**Model:** llava:latest

**For visual issues:**
- Take screenshot after minimal change
- Compare to "before" screenshot
- Did the specific symptom change?

**For functional issues:**
- Run the test/reproduction steps
- Did behavior change as expected?

**Emit:** `[WATCHER:VERIFIED] hypothesis CONFIRMED` or `[WATCHER:REJECTED] hypothesis REJECTED`

### Step 4 — Branch (QueenB)

**If hypothesis CONFIRMED:**  
→ Proceed to Phase 4 (Implementation)

**If hypothesis REJECTED:**  
→ Return to Scout for NEW hypothesis  
→ Don't stack fixes, start fresh

**If 3+ hypotheses rejected:**  
→ Escalate to Claude (architectural problem, not tactical bug)

**Emit:** `[QUEENB:BRANCHING] [confirmed/new-hypothesis/escalate]`

---

## Phase 4: Implementation (Builder → Watcher)

**Goal:** Fix the root cause, not the symptom

### Step 1 — Create Regression Test (Builder)

**Before fixing, create a test that reproduces the bug.**

**For Playwright/visual bugs:**
```typescript
// tests/regression/YYYY-MM-DD-issue-name.spec.ts
test('contact form should submit without error', async ({ page }) => {
  await page.goto('/contact');
  await page.fill('[name="email"]', 'test@example.com');
  await page.click('button[type="submit"]');
  
  // Should see success message, not error
  await expect(page.locator('.success')).toBeVisible();
});
```

**Emit:** `[BUILDER:TEST_CREATED] regression test written`

Run test to verify it FAILS with current code:  
**Emit:** `[BUILDER:TEST_FAILS] regression test fails as expected`

### Step 2 — Implement Single Fix (Builder)

Address the root cause identified in Phase 1.
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

**Emit:** `[BUILDER:FIXING] implementing root cause fix`

Output complete fixed file(s).

**Emit:** `[BUILDER:FIX_APPLIED] fix applied to [files]`

### Step 3 — Verify Fix (Watcher)

Run regression test:
**Emit:** `[WATCHER:TESTING] running regression test`

**If test PASSES:**
- Take "after" screenshot
- Compare to "before"
- Verify all success criteria met

**Emit:** `[WATCHER:VERIFIED] fix confirmed — [what is now working]`

**If test FAILS:**  
**Emit:** `[WATCHER:FAILED] fix did not work — [what is still wrong]`

### Step 4 — Check for Regressions (Watcher)

**Run full test suite if available:**
```bash
# Run all tests to ensure no new breaks
npm test
# or
pytest tests/
```

**Check related functionality:**
- If fixed contact form, test all forms
- If fixed navigation, test all nav links
- If fixed styling, check responsive breakpoints

**Emit:** `[WATCHER:REGRESSIONS] [none found / N issues found]`

### Step 5 — If Fix Doesn't Work — The Rule of Three

**STOP.**

Count: How many fixes have you tried?

**If < 3:** Return to Phase 1, re-analyze with new information  
**If ≥ 3:** **STOP and question the architecture** (see below)

**DON'T attempt Fix #4 without architectural discussion.**

**Emit:** `[QUEENB:RULE_OF_THREE] [N] fixes attempted, [returning-to-phase1 / escalating]`

### Step 6 — If 3+ Fixes Failed: Question Architecture (QueenB → Claude)

**Pattern indicating architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere
- Root cause keeps moving

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**QueenB escalates to Claude:**

```
ESCALATION: Architectural Issue After 3 Failed Fixes

ATTEMPTS:
1. [Fix attempt 1] → [Result]
2. [Fix attempt 2] → [Result]
3. [Fix attempt 3] → [Result]

PATTERN: Each fix reveals [shared state / coupling / new symptom]

QUESTION: Should we refactor the architecture instead of fixing symptoms?

REQUEST: Architectural review and recommendation
```

**Emit:** `[QUEENB:ESCALATED] architectural issue escalated to Claude`

**This is NOT a failed hypothesis — this is a wrong architecture.**

---

## Red Flags — STOP and Follow Process

If Scout or Builder catch themselves thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 Step 6).

---

## Common Rationalizations (Don't Fall For These)

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

---

## Quick Reference

| Phase | Model | Key Activities | Success Criteria |
|-------|-------|---------------|------------------|
| **1. Root Cause** | Scout | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Scout | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Scout → Builder → Watcher | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Builder → Watcher | Create regression test, fix root cause, verify, check regressions | Bug resolved, all tests pass |

---

## Integration with Worker Bee

### QueenB Orchestration

QueenB routes repair tasks through all 4 phases:

```
Phase 1-2: Scout investigates → diagnosis brief
Phase 3: Scout hypothesis → Builder minimal test → Watcher verify
Phase 4: Builder regression test + fix → Watcher verify + regression check
```

QueenB tracks:
- Which phase is active
- How many hypotheses tested
- How many fixes attempted (Rule of Three)
- When to escalate to Claude

### Site Registry Integration

Scout always checks ref-site-registry.md for:
- Known fragile points
- Common failure patterns for this site
- Recent issues and fixes

### Memory Storage

After successful fix:
- Store root cause + fix in ChromaDB
- Tag with site name, issue type, component
- Next time similar issue occurs, Scout checks memory first

---

## Example: Systematic Debugging in Action

**Issue:** Contact form on mountainedgeplumbing.com not submitting

### Phase 1: Root Cause (Scout)

```
[SCOUT:READING_ERRORS] analyzing browser console
Error: "Cannot read property 'email' of undefined"
File: ContactForm.tsx:45

[SCOUT:GIT_HISTORY] recent changes reviewed
Last change: Added email validation 2 hours ago

[SCOUT:REGISTRY] known fragile points reviewed
Known issue: Form state initialization timing

[SCOUT:REPRODUCED] issue reproduced consistently
Steps: Open form, fill email, click submit → error

[SCOUT:TRACED] data flow traced to origin
formData.email accessed before useState initialized

[SCOUT:PHASE1_COMPLETE] root cause identified:
formData accessed before initialization in handleSubmit
```

### Phase 2: Pattern (Scout)

```
[SCOUT:PATTERNS] found 3 working examples
FeaturesForm.tsx initializes state before render
CTAForm.tsx uses defaultValue prop
NavForm.tsx has proper initialization

[SCOUT:DIFFERENCES] identified key difference
ContactForm missing useState initialization
Working forms: const [formData, setFormData] = useState({ email: '' })
Broken form: const [formData, setFormData] = useState()

[SCOUT:PHASE2_COMPLETE] pattern analysis complete
```

### Phase 3: Hypothesis (Scout → Builder → Watcher)

```
[SCOUT:HYPOTHESIS] testing hypothesis:
Adding default empty object to useState will prevent undefined access

[BUILDER:TESTING] applying minimal test change
Changed: useState() → useState({ email: '', message: '' })

[BUILDER:TEST_APPLIED] change applied to ContactForm.tsx

[WATCHER:VERIFIED] hypothesis CONFIRMED
Form now submits without error
```

### Phase 4: Implementation (Builder → Watcher)

```
[BUILDER:TEST_CREATED] regression test written
tests/regression/2026-04-26-contact-form-submit.spec.ts

[BUILDER:TEST_FAILS] regression test fails as expected
(with old code)

[BUILDER:FIXING] implementing root cause fix
Added proper useState initialization with default values

[BUILDER:FIX_APPLIED] fix applied to ContactForm.tsx

[WATCHER:TESTING] running regression test
[WATCHER:VERIFIED] fix confirmed — form submits successfully

[WATCHER:REGRESSIONS] none found
All other forms still working
```

**Result:** Root cause fixed in ~10 minutes with systematic approach vs. hours of random fixes.

---

## Hard Gates

<HARD-GATE>
Phase 1 must be complete before Phase 2.
Cannot proceed without understanding WHY the issue occurs.
</HARD-GATE>

<HARD-GATE>
Phase 3 hypothesis must be tested BEFORE full implementation.
No multi-variable fixes without isolating variables first.
</HARD-GATE>

<HARD-GATE>
Phase 4 must include regression test.
Fixes without tests don't stick.
</HARD-GATE>

<HARD-GATE>
After 3 failed fixes, MUST escalate to architectural review.
No Fix #4 without Claude's input.
</HARD-GATE>

---

## Success Metrics

From real debugging sessions:
- **Systematic approach:** 15-30 minutes to fix
- **Random fixes approach:** 2-3 hours of thrashing
- **First-time fix rate:** 95% vs 40%
- **New bugs introduced:** Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
