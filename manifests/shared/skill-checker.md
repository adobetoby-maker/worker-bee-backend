---
name: skill-checker
description: Used by all four pipelines at step 3. llava verifies visual output and recovers from failures.
---

# skill-checker — Shared Vision Verification

**Called by:** Builder (step 3), Tester (step 3), Email (step 3), Repair (step 3)
**Model:** llava:latest
**Pairs with:** skill-fixer (builder), skill-reporter (tester), skill-refiner (email), skill-verifier (repair)

## Announce At Start

"I am using skill-checker to verify the current output visually."

## Follow runner-narrator.md for all status emissions.

## What You Receive

From Builder: a screenshot of the built component at preview URL
From Tester: a screenshot of a page after a user journey step
From Email: the drafted email text (visual review of formatting/tone)
From Repair: a screenshot of the site after a fix was applied

## Step 1 — Initial Assessment

Take the screenshot (or receive it from the pipeline).
Emit: [CHECKER:ASSESS] examining output

Look at what is actually there.
Do not assume. Do not infer.
Only describe what you can see.

## Step 2 — Compare To Brief

Read the brief or test plan you were given.
For every expected element, check:
- Is it present? Visible? In the right location?
- Does text match expected content?
- Does layout match expected structure?
- Are there error messages anywhere?

## Step 3 — Verdict

### PASS Criteria — ALL must be true
- Every expected element is visible
- No error messages present anywhere on screen
- Layout matches the brief or test plan
- Key interactions appear functional

Emit: [CHECKER:PASS] what specifically passed → hand to next step

### FAIL — Enter Recovery Mode

<HARD-GATE>
FAIL does not end the pipeline.
You MUST attempt recovery before reporting failure.
Maximum 3 recovery attempts.
</HARD-GATE>

**Recovery Cycle:**

SCAN — Describe everything visible on screen:
Emit: [CHECKER:SCANNING] listing all visible elements

IDENTIFY — Find alternative paths:
Look for alternate buttons, links, hidden menus,
cookie banners blocking content, collapsed sections,
similar labels to what was expected.
Emit: [CHECKER:OPTIONS] alternatives available

RECOMMEND — Pick the single best alternative:
"I can see [element] at [location] — recommend attempting this"
Emit: [CHECKER:SUGGEST] specific recommendation → hand to webuser/builder

LOOP — webuser or builder attempts the alternative.
You receive new screenshot.
You check again.
Maximum 3 cycles total.

After 3 failed cycles:
Emit: [CHECKER:EXHAUSTED] all recovery paths tried
Hand to reporter/fixer with complete attempt log including all screenshots.

## Delta Detection

If a previous check result exists in memory:
Compare current to previous.
Note what changed.
Classify:
- IMPROVEMENT — something better than before
- REGRESSION — something that worked now failing
- NOVEL — new element appeared
- UNCHANGED — no meaningful difference

Pass delta classification to voice.md output.

## Output Format

Always return:
```
VERDICT: PASS / FAIL / EXHAUSTED
WHAT I SAW: [specific description]
DELTA: [IMPROVEMENT/REGRESSION/NOVEL/UNCHANGED] — [what changed]
RECOVERY ATTEMPTS: [0/1/2/3]
NEXT STEP: [which skill to hand to]
```
