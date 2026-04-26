---
name: skill-navigator
description: Tester pipeline step 1. deepseek writes the E2E test plan.
---

# skill-navigator — Test Plan Writer

**Model:** deepseek-r1:14b
**Called by:** 01-master-controller (Tester pipeline)
**Hands off to:** skill-webuser

## Announce At Start

"I am using skill-navigator to write a test plan for [site]."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Read Site Registry

Read ref-site-registry.md for the target site.
Know the fragile points before writing a single step.
Emit: [NAVIGATOR:REGISTRY] read — fragile points identified

## Step 2 — Classify The Test

Choose the test type:

```
SHALLOW — pages load, links work, layout correct
DEEP    — user journeys, form submissions, auth flows
E2E     — full acquisition/conversion/auth/recovery journeys
```

Default is E2E for all production sites unless told otherwise.

## Step 3 — Choose The Journey Type

```
ACQUISITION  — new visitor: entry → key info → CTA → confirmation
CONVERSION   — primary action: form/button → input → submit → confirmation  
AUTH         — login → dashboard → logout → locked out verification
RECOVERY     — bad input → error message → recovery path → success
```

Run the journey type most relevant to the task.
If no specific instruction, run CONVERSION first — it breaks most often.

## Step 4 — Write The Test Plan

For each step in the journey:

```
STEP [N]: [action to take]
URL: [expected URL after action]
ELEMENT: [specific element to interact with]
DATA: [exact data to input if applicable]
EXPECTED: [what must be true for this step to pass]
FAILURE SIGNAL: [what failure looks like at this step]
```

## Step 5 — State Success Criteria

What does the complete end state look like?
This is what llava checks at the end.

## Hard Stop

<HARD-GATE>
Do not write a test plan that says "check if the site works."
Every step must be specific enough for playwright to execute
without making any decisions.
If playwright would have to guess — rewrite the step.
</HARD-GATE>

Emit: [NAVIGATOR:PLAN_COMPLETE] N steps written → handing to webuser
