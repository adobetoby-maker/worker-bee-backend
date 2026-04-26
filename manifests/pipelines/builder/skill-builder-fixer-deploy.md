---
name: skill-builder
description: Builder pipeline step 2. qwen writes complete code from the brief.
---

# skill-builder — Code Generator

**Model:** qwen2.5-coder:32b
**Called by:** skill-planner
**Hands off to:** skill-checker

## Announce At Start

"I am using skill-builder to build [component name]."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Read The Entire Brief

Read skill-planner's output completely before writing a single line.
Emit: [BUILDER:READING] reading brief

## Step 2 — List Files To Write

State every file you will create or modify.
Emit: [BUILDER:FILES] listing N files to write

## Step 3 — Write All Files

<HARD-GATE>
Every file must be complete.
No partial files.
No "..." placeholders.
No "add your code here" comments.
If you write a file, it must be 100% complete and functional.
</HARD-GATE>

Write files in dependency order.
Types and interfaces first.
Utility functions second.
Components last.

No backticks in file content output.
Output the raw file content only.

## Step 4 — Report Completion

List every file written with its path.
Emit: [BUILDER:CODE_COMPLETE] N files written → handing to checker

Do not describe what the code does.
Do not summarize.
Just list the files and hand to checker.

---
name: skill-fixer
description: Builder pipeline step 4. qwen fixes exactly what llava flagged.
---

# skill-fixer — Code Fixer

**Model:** qwen2.5-coder:32b
**Called by:** skill-checker (on FAIL verdict)
**Hands off to:** skill-checker (for re-verification)

## Announce At Start

"I am using skill-fixer to fix [what was flagged]."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Read llava's Report Completely

Understand exactly what is wrong before touching any code.
Emit: [FIXER:READING] understanding what needs fixing

## Step 2 — Fix Only What Was Flagged

<HARD-GATE>
Fix exactly what llava reported. Nothing more.
Do not refactor what was not broken.
Do not improve what was not flagged.
Do not add features that were not in the brief.
Scope creep in fixes breaks things that were working.
</HARD-GATE>

## Step 3 — Output Complete Files

Even for a one-line fix, output the complete file.
Partial files break apply_changes.

Emit: [FIXER:COMPLETE] fixed [what] in [file] → handing back to checker

---
name: skill-deploy
description: Builder pipeline step 5. Shell pushes to preview and confirms live.
---

# skill-deploy — Preview Deployer

**Model:** Shell tool (shell.py)
**Called by:** skill-checker (on PASS verdict)
**Hands off to:** 01-master-controller with result

## Announce At Start

"I am using skill-deploy to push [project] to preview."

## Follow runner-narrator.md for all status emissions.

## Step 1 — Restart Dev Server

```bash
cd ~/worker-bee/projects/[project_name]
# Kill existing
lsof -ti :5173 | xargs kill -9 2>/dev/null
sleep 2
# Start fresh
npm run dev > /tmp/devserver-[project].log 2>&1 &
sleep 3
```

Emit: [DEPLOY:SERVER] dev server restarting

## Step 2 — Verify Preview URL

```bash
curl -I https://preview.tobyandertonmd.com
```

Expected: HTTP/2 200
If 502: dev server didn't bind — retry once after 5 seconds.
If still 502: emit [DEPLOY:ERROR] preview URL returning 502

Emit: [DEPLOY:VERIFY] preview URL responding

## Step 3 — Confirm To Controller

Pass to 01-master-controller:
```
DEPLOY: complete
URL: https://preview.tobyandertonmd.com
PROJECT: [project_name]
STATUS: live
```

Read voice.md.
Generate completion message.
"Done — preview is live at preview.tobyandertonmd.com"
