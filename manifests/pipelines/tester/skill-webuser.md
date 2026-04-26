---
name: skill-webuser
description: Tester pipeline step 2. Playwright executes the test plan step by step.
---

# skill-webuser — Browser Test Executor

**Model:** Playwright tool (browser.py)
**Called by:** skill-navigator
**Hands off to:** skill-checker (after each step)

## Announce At Start

"I am using skill-webuser to execute the test plan on [site]."

## Follow runner-narrator.md for all status emissions.

## The Core Loop

For every step in the test plan:

```
1. Emit status: what you are about to do
2. Navigate or interact
3. Take screenshot immediately
4. Hand screenshot to skill-checker
5. Wait for checker verdict
6. If PASS → continue to next step
7. If CHECKER:SUGGEST → execute the suggestion (you are now in recovery mode)
8. If CHECKER:EXHAUSTED → stop, hand all to skill-reporter
9. If all steps PASS → hand to skill-reporter with full log
```

## Recovery Mode

When skill-checker returns [CHECKER:SUGGEST]:
Emit: [WEBUSER:ATTEMPTING] what checker suggested
Execute exactly what checker described.
Take screenshot.
Hand back to checker.
You do not make your own navigation decisions in recovery mode.
Checker drives. You execute.

## E2E Test Requirements

<HARD-GATE>
Loading the homepage is step ONE, not the result.
A complete E2E test follows the full user journey.
Do not report success until the journey endpoint is reached.
</HARD-GATE>

## What To Screenshot

Screenshot immediately after EVERY action.
Not before. After.
The screenshot proves what happened, not what you intended.

## Step Log Format

Maintain a log of every step:
```
STEP [N]: [action taken]
SCREENSHOT: [taken at timestamp]  
VERDICT: [PASS/FAIL]
RECOVERY: [yes/no — if yes, how many attempts]
```

Hand the complete step log to skill-reporter.

## Hard Stop Conditions

Stop immediately if:
- A login wall appears unexpectedly
- An error page appears (404, 500, etc.)
- The site becomes completely unresponsive
- skill-checker returns EXHAUSTED

Emit: [WEBUSER:BLOCKED] what stopped you → hand to reporter
Do NOT try to continue past a hard stop.
