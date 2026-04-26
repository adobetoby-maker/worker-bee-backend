---
name: runner-narrator
description: Embedded in every pipeline skill. Defines how and when to emit status to the user.
---

# Runner Narrator — Status Emission Protocol

## Why This Exists

Toby once watched a build run for 45 minutes with no output and no result.
That must never happen again.
Every pipeline step MUST emit proof of life.
The user must always know what is happening.

## The Emission Format

Every status line follows this exact format:
```
[MODEL:STEP] description of current action
```

Examples:
```
[PLANNER:BRIEF] deepseek writing technical brief for contact form
[BUILDER:CODE] qwen generating ContactForm.tsx — estimated 90 seconds
[CHECKER:SCAN] llava analyzing screenshot against brief
[CHECKER:FAIL] form button not visible — scanning for alternatives
[CHECKER:SUGGEST] found "Get Quote" button at top right — attempting
[REPORTER:WRITE] qwen composing findings report
[MEMORY:STORE] chromadb storing test results with delta comparison
```

## When To Emit

**Emit BEFORE every action:**
```
[MODEL:STEP] about to [action]
```

**Emit AFTER every action completes:**
```
[MODEL:STEP] [action] complete — [one word result: ok/failed/retry]
```

**Emit every 2 minutes if still working:**
```
[MODEL:ALIVE] still working — [what you are currently doing]
```

**Emit immediately on any error:**
```
[MODEL:ERROR] what went wrong — [stopping/retrying/escalating]
```

## The Heartbeat Rule

<HARD-GATE>
If you have not emitted a status in 2 minutes, emit ALIVE immediately.
Silence longer than 2 minutes is indistinguishable from broken.
The user cannot tell the difference. Do not make them wonder.
</HARD-GATE>

## When To Be Quiet

Emit for significant actions only.
Do NOT emit for:
- Internal calculations or reasoning steps
- Reading a file you are about to use
- Minor intermediate steps that complete in under 5 seconds

Emit for:
- Starting any model call
- Starting any browser action
- Starting any file write
- Any step that could take more than 10 seconds
- Any error or unexpected result
- Any recovery attempt

## Pipeline Stage Markers

At the start of each pipeline stage, emit the stage marker:
```
[PIPELINE:STAGE_NAME] starting
```

At the end of each pipeline stage:
```
[PIPELINE:STAGE_NAME] complete → handing to [next stage]
```

This lets Toby see exactly where in the pipeline the work is.

## Integration

This protocol is referenced by every pipeline skill file.
Every skill file contains the line:
"Follow runner-narrator.md for all status emissions."
It is not optional in any skill.
