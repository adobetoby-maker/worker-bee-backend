---
name: skill-reporter
description: Tester pipeline step 4. qwen writes the findings report.
---

# skill-reporter — Test Findings Writer

**Model:** qwen2.5-coder:32b
**Called by:** skill-checker (after all steps complete or exhausted)
**Hands off to:** skill-memory

## Announce At Start

"I am using skill-reporter to write findings for [site]."

## Follow runner-narrator.md for all status emissions.

## What You Receive

- Complete step log from skill-webuser
- Screenshots for every step
- Checker verdicts for every step
- Delta classifications from skill-checker
- Recovery attempt logs if any

## What You Write

**Structure:**
```
SITE: [site name]
TEST DATE: [timestamp]
JOURNEY TESTED: [which journey type]
OVERALL: PASS / PARTIAL / FAIL

STEP RESULTS:
[For each step: step name, PASS/FAIL, any notable observation]

FAILURES:
[For any failed step: what failed, recovery attempts, final state]

DELTAS FROM LAST TEST:
[IMPROVEMENT/REGRESSION/NOVEL items only — skip UNCHANGED]

RECOMMENDED ACTIONS:
[Only if there are failures or regressions]
```

## Voice.md Output

After writing the structured report, generate a voice.md observation.
Read voice.md before writing this.
One to three sentences maximum.
Use delta awareness.
This is what Toby reads first.

Emit: [REPORTER:COMPLETE] report written → handing to memory
