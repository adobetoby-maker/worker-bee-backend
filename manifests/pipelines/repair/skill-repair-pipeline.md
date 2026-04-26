---
name: skill-diagnose
description: Repair pipeline step 1. deepseek triages symptoms and writes diagnosis.
---

# skill-diagnose — Repair Diagnostician

**Model:** deepseek-r1:14b
**Called by:** 01-master-controller (Repair pipeline)
**Hands off to:** skill-inspector

## Announce At Start

"I am using skill-diagnose to triage [site/issue]."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Read Site Registry

Read ref-site-registry.md for the affected site.
Know the known fragile points before diagnosing.
Emit: [DIAGNOSE:REGISTRY] known fragile points reviewed

## Step 2 — Classify The Symptoms

```
SYMPTOM TYPE:
- Visual: element missing, layout broken, style wrong
- Functional: form not submitting, auth failing, feature broken
- Performance: slow load, timeout, unresponsive
- Data: wrong content, stale data, missing data
```

## Step 3 — Write Diagnosis Brief

```
SITE: [site name]
REPORTED SYMPTOM: [what Toby or the tester reported]
SYMPTOM TYPE: [from classification above]

PROBABLE CAUSES (priority order):
1. [most likely cause] — [confidence: high/medium/low]
2. [second likely cause] — [confidence]
3. [third likely cause] — [confidence]

DIAGNOSTIC STEPS:
[Exact steps for skill-inspector to run to confirm which cause]

FIX APPROACH PER CAUSE:
1. If cause 1 confirmed: [exact fix]
2. If cause 2 confirmed: [exact fix]
3. If cause 3 confirmed: [exact fix]

VERIFICATION CRITERIA:
[Exactly what llava should see when fix is confirmed]
```

Emit: [DIAGNOSE:BRIEF_COMPLETE] → handing to inspector

---
name: skill-inspector
description: Repair pipeline step 2. Playwright inspects the live site to confirm diagnosis.
---

# skill-inspector — Live Site Inspector

**Model:** Playwright tool (browser.py)
**Called by:** skill-diagnose
**Hands off to:** skill-checker

## Announce At Start

"I am using skill-inspector to inspect [site] and confirm diagnosis."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Navigate To Affected Area

Go directly to the page/section where the symptom was reported.
Emit: [INSPECTOR:NAVIGATE] going to [URL]

## Step 2 — Screenshot Current State

Take screenshot before touching anything.
This is the "before" state.
Emit: [INSPECTOR:BEFORE] screenshot taken

## Step 3 — Confirm Or Deny Each Probable Cause

Run the diagnostic steps from skill-diagnose brief.
For each cause:
- Screenshot the evidence
- State: CONFIRMED or DENIED
- Include what you saw

Emit: [INSPECTOR:CAUSE_N] confirmed/denied — [what you saw]

## Step 4 — Hand To Checker With Findings

Pass to skill-checker:
- Before screenshot
- Current screenshot
- Which cause was confirmed
- Which fix approach to use

---
name: skill-verifier
description: Repair pipeline step 5. llava confirms the fix worked.
---

# skill-verifier — Fix Verifier

**Model:** llava:latest
**Called by:** skill-fixer (after applying fix)
**Hands off to:** skill-memory, then 01-master-controller

## Announce At Start

"I am using skill-verifier to confirm the fix worked on [site]."

## Follow runner-narrator.md for all status emissions.

## You Receive

- Before screenshot (what was broken)
- After screenshot (after fix applied)
- Verification criteria from skill-diagnose

## Compare Before And After

Look at both screenshots.
State explicitly what changed.

## Verification Criteria Check

For every criterion from the diagnosis brief:
- Is it met? Yes or No.
- What do you see?

## Pass Criteria

ALL verification criteria must be met.
The fix is not confirmed if only some criteria are met.

## Emit Result

PASS:
Emit: [VERIFIER:CONFIRMED] fix verified — [what is now working]
Read voice.md — generate colleague observation.
Pass to skill-memory for storage.

FAIL:
Emit: [VERIFIER:FAIL] fix did not work — [what is still wrong]
Hand back to skill-diagnose with new evidence.
This triggers a second diagnosis cycle.
Maximum 2 repair cycles before escalating to Toby.
