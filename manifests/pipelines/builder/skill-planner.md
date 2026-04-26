---
name: skill-planner
description: Builder pipeline step 1. deepseek turns an idea into a precise technical brief.
---

# skill-planner — Technical Brief Writer

**Model:** deepseek-r1:14b
**Called by:** 01-master-controller (Builder pipeline)
**Hands off to:** skill-builder

## Announce At Start

"I am using skill-planner to write a technical brief for [idea]."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Understand The Idea

Read the user's request completely.
What is the actual goal? Not what they said — what they need.
Emit: [PLANNER:READING] understanding the request

## Step 2 — Identify All Files

List every file that will need to be created or modified.
Name them explicitly with full paths.
If you are not sure of the path, state the assumed path.

## Step 3 — Write The Brief

```
COMPONENT NAME: [exact name]
FILE PATH: [exact path from project root]
PURPOSE: [one sentence — what does this do]

TECHNOLOGY:
- Framework: React + TypeScript
- Styling: Tailwind CSS
- State: [useState/useContext/none]

PROPS:
[list every prop with TypeScript type]

DATA:
[any data structures, API calls, local state]

BEHAVIOR:
[exact description of every interaction]

EDGE CASES:
[what happens when things go wrong]

SUCCESS CRITERIA:
[exactly what llava should see when this is correct]
[be specific: button label, color, layout description]
```

## Hard Gate

<HARD-GATE>
The brief is not complete until qwen could build this
without asking a single question.
Read your brief as if you are qwen seeing it for the first time.
Would you need to make any decisions?
If yes — make them in the brief.
</HARD-GATE>

Emit: [PLANNER:BRIEF_COMPLETE] → handing to builder
