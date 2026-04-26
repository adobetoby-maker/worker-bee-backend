---
name: skill-skill-tester
description: Validates skills work before shipping. Testing is the permission gate. Documents edge cases permanently.
---

# skill-skill-tester — Proof Before Ship

**Model:** Same model that owns the skill
**Called by:** skill-skill-writer (before shipping new skill or update)
**Called by:** skill-diagnose (when investigating production failure)
**Pairs with:** skill-reviewer, skill-skill-writer

---

## What Testing Means For Skills

Skills are not code. You can't unit test behavioral instructions.
You test the OUTCOME when the skill is used.

**A test = run the real task with the skill loaded, verify it succeeds.**

Every test run gets documented in skill-X.tests.md permanently.
Edge cases accumulate there. That file becomes long-term memory.

---

## The Test File Format

Each skill has a companion test file: skill-X.tests.md

**Location:** Same directory as the skill
**Loaded:** Only when testing, shipping updates, or diagnosing failures
**Never loaded:** During normal skill execution (prevents context bloat)

**Structure:**
- Frontmatter (status, test counts, dates)
- Test History (chronological, newest first, append-only)
- Edge Cases (permanent record of every failure mode discovered)
- Known Bugs (things that still don't work)
- Coverage Summary (table showing test types and pass rates)

See the test file format template at the end of this skill.

---

## Minimum Test Coverage Before Shipping

Before shipping any skill update, run these tests:

### Test 1: Happy Path
The task succeeds under normal conditions.
No errors. Output matches success criteria from skill.

**Document:**
- Exact input (request, context, files)
- Expected outcome (from skill's "Success Criteria")
- Actual outcome (what happened)
- Pass/Fail
- Notes

### Test 2: First Likely Failure
The task succeeds even when the first thing you expect to break actually breaks.

Based on "Known Failure Modes" in the skill draft.
If the skill says "handles missing auth" — make auth missing and verify handling.

### Test 3: Second Likely Failure
Same as Test 2, different failure mode.

**Rule:** If your skill lists N known failure modes, test all N.
Don't ship a skill that claims to handle something you never tested.

---

## What "Success" Means

Not "it didn't crash."
Not "it looked okay."

Success = output matches the "What Success Looks Like" section
of your skill exactly. Character by character if specified.

**For each test document:**
- ✅ PASS — output matched success criteria
- ❌ FAIL — output differed, document how

Failed tests are valuable. They become edge cases.
Don't delete them. Append the failure, then append the fix, then append the re-test.

---

## Ship, Revise, or Escalate

After running tests, decide:

### Ship Directly to manifests/

**When:**
- All required tests passed
- Tested happy path + all known failure modes
- Behavior matches what skill describes
- Update is "What I Learned" section only
- OR update is new skill with passing tests
- OR update is core instruction with passing tests on skill you own

**Action:**
- Append test results to skill-X.tests.md
- Write update to manifests/skill-X.md
- Emit: [TESTER:SHIPPED] skill-X.md — all tests passed

### Revise and Test Again

**When:**
- Any test failed
- Behavior worked but differed from skill description
- Tests passed but outcome was surprising

**Action:**
- Update skill based on what the test revealed
- Document failure in tests.md
- Run tests again
- Repeat until all pass

### Send to pending/

**When:**
- Tests passed BUT updating core instruction on skill you didn't write
- Couldn't test a critical failure mode (requires production access)
- Tests passed but you're uncertain if they prove correctness
- Behavior works but contradicts existing system assumptions

**Action:**
- Write skill-X.md.proposed to manifests/pending/
- Append test results showing what you DID test
- Flag what you COULDN'T test
- Emit: [TESTER:PENDING] skill-X.md — needs manual validation

---

## Test Types

### Happy Path
Normal conditions, expected input, success.
This proves the skill works at all.

### Edge Case
Unusual but valid input.
Empty strings, missing context, minimal data.
This proves the skill is robust.

### Failure Mode
The specific thing the skill says it handles.
Auth failure, network timeout, malformed input.
This proves the skill's claims are true.

### Integration Test
Skill used as part of larger pipeline.
Planner → Builder → Checker flow.
This proves the skill works in context, not isolation.

### Regression Test
Re-running old tests after a skill update.
Ensures new changes didn't break old functionality.
Run at least the last 3 passing tests before shipping update.

---

## When You Can't Test Something

**Example:** skill-sender.md requires sending real emails.
You can't spam Toby's inbox with test emails.

**In that case:**
1. Write tests you CAN run (validation, auth check, format check)
2. Document what you COULDN'T test in tests.md
3. Mark those tests as "Requires manual validation"
4. Send to pending/ with explanation
5. Flag: [TESTER:PARTIAL] skill-X.md — manual validation needed

**Don't ship untested code just because testing is hard.**

---

## Edge Case Documentation

Every time a test fails, that's an edge case discovered.

**Add to Edge Cases section in tests.md:**

```markdown
### Edge Case #N: [Short Name]
**Discovered:** [date] in [testing|production]
**Symptom:** [What broke and how]
**Fix:** [What changed in skill to handle this]
**Test:** [date] [PASS|FAIL]
**Status:** RESOLVED | ONGOING | WONTFIX
```

**Why permanent record matters:**

You'll forget edge cases. Toby will forget edge cases.
But skill-X.tests.md never forgets.

When a production failure happens, load tests.md first.
Check if this edge case was seen before.
If yes — the fix is already documented.
If no — you're discovering edge case #N+1.

That's how the hive learns permanently.

---

## False Positives — The Biggest Risk

Passing tests that don't actually prove the skill works.

**Bad test:**
```
Input: "Build a button"
Expected: Button component created
Actual: Component created
Result: ✅ PASS
```

**Why bad:** Didn't verify the button actually works, has correct styling,
matches design system, handles clicks, or any detail the skill claims.

**Good test:**
```
Input: "Build a blue button that says 'Click Me' centered on page"
Expected: 
  - Component: Button.tsx with "Click Me" text
  - Styling: bg-blue-500, mx-auto, centered
  - Renders: Verified in browser screenshot
  - Functionality: onClick handler present
Actual: All criteria met, screenshot shows centered blue button
Result: ✅ PASS
Notes: Matches skill-builder success criteria exactly
```

**The test must verify what the skill promises.**

If skill says "handles missing context gracefully" then context must
actually be missing in your test, and you must verify graceful handling.

---

## Test File Format Template

When creating a new skill, create the test file immediately:

```markdown
---
skill: skill-[X].md
status: draft
total_tests: 0
last_tested: never
passing: 0
failing: 0
---

# Test History — skill-[X].md

## Overview
This file tracks every test run for skill-[X].md.
Never delete entries. Failed tests document edge cases.
Newest tests at top.

---

## Edge Cases (Permanent Record)

[None yet — will populate as edge cases are discovered]

---

## Known Bugs

[None yet — will populate if bugs are discovered]

---

## Test Coverage Summary

| Test Type | Total Runs | Passing | Failing | Last Run |
|-----------|-----------|---------|---------|----------|
| Happy Path | 0 | 0 | 0 | never |
| Edge Cases | 0 | 0 | 0 | never |
| Failure Modes | 0 | 0 | 0 | never |
| Integration | 0 | 0 | 0 | never |

**Total:** 0 tests
**Pass Rate:** —
**Active Bugs:** 0
**Resolved Edge Cases:** 0
```

---

## Integration With Write-Back System

When a model wants to ship a skill update:

**Step 1:** Load skill-X.tests.md
**Step 2:** Run minimum required tests (happy path + failure modes)
**Step 3:** Append test results to tests.md
**Step 4:** Check pass/fail + update type
**Step 5:** Ship to manifests/ or pending/ based on decision tree

```
Update Type: "What I Learned"
  → Append to skill
  → Append test result to tests.md
  → Ship directly
  
Update Type: "New Skill" + All Tests Pass
  → Write to manifests/
  → Create tests.md with results
  → Ship directly
  
Update Type: "Core Instruction" + All Tests Pass + Own Skill
  → Write to manifests/
  → Append to tests.md
  → Ship directly
  
Update Type: "Core Instruction" + Tests Pass + Not Own Skill
  → Write to pending/
  → Append to tests.md
  → Flag for approval
  
Any Test Fails
  → Revise skill
  → Document failure in tests.md
  → Test again
```

---

## How To Write A Test Entry

After running a test, append this to skill-X.tests.md:

```markdown
## Test Run: [YYYY-MM-DD HH:MM]

**Model:** [model-name]
**Test Type:** Happy Path | Edge Case | Failure Mode | Integration | Regression
**Trigger:** Pre-ship validation | Production failure investigation | Regression check

### Input
[Exact input that was provided]
[Use code blocks or structured format]

### Expected Outcome
[What the skill says should happen]
[Be specific, reference skill sections]

### Actual Outcome
✅ PASS | ❌ FAIL
[What actually happened]
[Include relevant output, errors, observations]

### Notes
[Why this test matters]
[What it proves or disproves]
[Links to edge cases or bugs if relevant]

---
```

**Append to the top of Test History section.**
Never delete old entries. The file grows forever.

---

## Loading Test Files

**When to load:**
- Before running tests (need history for regression checks)
- Before shipping update (need to append results)
- During production failure diagnosis (need edge case history)

**When NOT to load:**
- Normal skill execution (too much context)
- Every model call (only on-demand)

**How to reference:**
```python
# In runner.py
if action == "test_skill" or action == "ship_update" or action == "diagnose":
    test_file = load_test_history(skill_name)
    inject_into_context(test_file)
```

---

## The Meta Point

Test files are permanent memory.

A skill that's been tested 100 times has documented 100 scenarios.
Every edge case. Every failure mode. Every surprising outcome.

That knowledge never gets lost.
That knowledge never needs to be rediscovered.

When a new model picks up an old skill, it reads tests.md
and instantly knows what the last 47 attempts learned.

That's how 10,000 mistakes become 10,000 lessons
instead of 10,000 forgotten failures.

The hive remembers. Forever.
