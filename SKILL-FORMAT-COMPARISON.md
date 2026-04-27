# Skill Format Comparison: Hermes Agent vs Worker Bee

## Summary

**Hermes Agent** skills are **user-facing procedural guides** with rich metadata, examples, and reference docs.  
**Worker Bee** skills are **model-facing behavioral scripts** for pipeline orchestration with hard gates and status emissions.

**Key insight:** They serve different purposes. Hermes teaches the agent HOW to use tools. Worker Bee tells models WHAT to do in pipelines.

---

## Format Breakdown

### Hermes Agent Format

**Example:** `optional-skills/devops/cli/SKILL.md`

```yaml
---
name: inference-sh-cli
description: "Run 150+ AI apps via inference.sh CLI..."
version: 1.0.0
author: okaris
license: MIT
metadata:
  hermes:
    tags: [AI, image-generation, video, LLM, search]
    related_skills: []
---

# Skill Title

Brief overview paragraph.

## When to Use
- Trigger conditions (when agent should activate this skill)
- User intent patterns
- Common keywords

## Prerequisites
- Required tools/packages
- Installation commands
- Auth setup

## Workflow
Step-by-step procedure with explanations

## Common Commands
Concrete examples with actual syntax

## Pitfalls
Common mistakes and how to avoid them

## Reference Docs
- links to supporting docs in references/ subdirectory
```

**Supporting structure:**
- `references/` subdirectory with detailed docs
- `DESCRIPTION.md` for category-level overview
- Hierarchical organization (category/subcategory/SKILL.md)

### Worker Bee Format

**Example:** `manifests/pipelines/builder/skill-planner.md`

```yaml
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
Emit: [PLANNER:READING] understanding the request

## Step 2 — Identify All Files
List every file that will need to be created or modified.

## Step 3 — Write The Brief
[Template structure with exact format requirements]

## Hard Gate
<HARD-GATE>
The brief is not complete until qwen could build this
without asking a single question.
</HARD-GATE>

Emit: [PLANNER:BRIEF_COMPLETE] → handing to builder
```

**Supporting structure:**
- `runner-narrator.md` for status emission protocol
- `01-master-controller.md` for pipeline orchestration
- `identity-{model}.md` for model-specific context

---

## What Hermes Has That We Don't

### 1. **Rich Metadata**
```yaml
version: 1.0.0
author: okaris
license: MIT
metadata:
  hermes:
    tags: [AI, image-generation, video]
    related_skills: []
```

**Why it matters:** Enables skill discovery, versioning, attribution. Could power skill marketplace.

**Worth adopting:** YES, but simplified
```yaml
version: 1.0.0
metadata:
  pipeline: builder
  step: 1
  hands_off_to: skill-builder
  tags: [planning, technical-brief]
```

### 2. **When to Use / Trigger Conditions**
Explicit list of when the skill should activate:
```markdown
## When to Use
- User asks to generate images (FLUX, Reve, Seedream)
- User asks about inference.sh or infsh
- User wants to run AI apps without managing APIs
```

**Why it matters:** Helps QueenB make better routing decisions. Currently QueenB uses `pick_model()` in runner.py with keyword matching. Skills could declare their own triggers.

**Worth adopting:** YES
```markdown
## Routing Triggers
- Keywords: ["build", "create", "generate", "component", "landing page"]
- Requires: existing project or scaffold decision
- Prerequisites: project structure exists (or will be created)
```

### 3. **Pitfalls Section**
Common mistakes documented upfront:
```markdown
## Pitfalls
1. Never guess app IDs — always run `infsh app list --search <term>` first
2. Always use `--json` — raw output is hard to parse
3. Check authentication — if commands fail with auth errors, run `infsh login`
```

**Why it matters:** Models learn faster from explicit "don't do this" guidance.

**Worth adopting:** YES
```markdown
## Common Mistakes
- Don't output partial files (apply_changes breaks)
- Don't skip existing code scan (context-blind changes)
- Don't write code without Scout's brief
```

### 4. **Reference Docs Subdirectory**
```
optional-skills/devops/cli/
├── SKILL.md
└── references/
    ├── authentication.md
    ├── app-discovery.md
    ├── running-apps.md
    └── cli-reference.md
```

**Why it matters:** Keeps SKILL.md focused, detailed docs separate. Models can load references when needed.

**Worth adopting:** MAYBE
Could be useful for complex skills like TESTER pipeline:
```
manifests/pipelines/tester/
├── skill-navigator.md
└── references/
    ├── playwright-selectors.md
    ├── common-patterns.md
    └── recovery-strategies.md
```

### 5. **Example Workflows**
Concrete multi-step examples:
```markdown
## Example Workflows

**Sign up for a service:**
1. create_inbox (username: "signup-bot")
2. Use the inbox address to register
3. list_threads to check for verification email
4. get_thread to read the verification code
```

**Why it matters:** Models learn patterns from examples better than abstract descriptions.

**Worth adopting:** YES, but as concrete brief examples
```markdown
## Example Briefs

**Contact Form Component:**
COMPONENT NAME: ContactForm
FILE PATH: src/components/ContactForm.tsx
PURPOSE: Capture user contact info and send to email endpoint
[full example brief]
```

---

## What We Have That Hermes Doesn't

### 1. **Pipeline Orchestration**
```markdown
**Model:** deepseek-r1:14b
**Called by:** 01-master-controller (Builder pipeline)
**Hands off to:** skill-builder
```

**Why it matters:** Worker Bee is a coordinated team. Hermes is a single agent. Our skills know their place in the hive.

### 2. **Status Emission Protocol**
```markdown
## Follow runner-narrator.md for all status emissions.

Emit: [PLANNER:READING] understanding the request
Emit: [PLANNER:BRIEF_COMPLETE] → handing to builder
```

**Why it matters:** Real-time pipeline visibility. Toby sees progress. QueenB tracks completion.

### 3. **Hard Gates (Validation Rules)**
```markdown
<HARD-GATE>
The brief is not complete until qwen could build this
without asking a single question.
</HARD-GATE>
```

**Why it matters:** Quality gates before handoff. Scout's brief must be complete or Builder can't execute.

### 4. **Announce At Start**
```markdown
## Announce At Start
"I am using skill-planner to write a technical brief for [idea]."
```

**Why it matters:** Models announce what they're doing. Transparency for autonomous operation.

### 5. **Model-Specific Skills**
```markdown
**Model:** deepseek-r1:14b
```

Skills are tied to specific models in the hive. Hermes skills are model-agnostic (any model can use any skill).

**Why it matters:** Specialization. Scout plans, Builder builds, Watcher checks. Skills match model capabilities.

---

## Recommendations: What To Adopt

### 1. **Add Metadata Block (High Priority)**
```yaml
---
name: skill-planner
description: Builder pipeline step 1. deepseek turns an idea into a precise technical brief.
version: 1.0.0
metadata:
  pipeline: builder
  step: 1
  model: deepseek-r1:14b
  hands_off_to: skill-builder
  tags: [planning, technical-brief, context-gathering]
---
```

**Benefit:** Enables versioning, better discovery, clearer pipeline relationships.

### 2. **Add "When To Use" / Routing Triggers (High Priority)**
```markdown
## Routing Triggers
- User intent: ["build a component", "create a page", "generate code"]
- Keywords: ["build", "create", "component", "landing page", "website"]
- Prerequisites: project exists OR user confirms scaffold
- Escalate if: architecture decisions, multi-site changes, production deployment
```

**Benefit:** QueenB makes better routing decisions. Currently uses crude keyword matching in runner.py.

### 3. **Add Pitfalls Section (Medium Priority)**
Every skill gets a "Common Mistakes" section:
```markdown
## Common Mistakes (What NOT To Do)
1. Don't output partial files — apply_changes breaks
2. Don't skip context scan — read existing code before planning
3. Don't write code without Scout's brief — you'll miss requirements
4. Don't refactor unrelated code — only touch what the brief specifies
```

**Benefit:** Faster learning, fewer repeated errors.

### 4. **Add Example Outputs (Medium Priority)**
```markdown
## Example Brief (Good)
[complete example that passes all hard gates]

## Example Brief (Bad - Incomplete)
[example that would fail hard gate with explanation why]
```

**Benefit:** Models learn from concrete examples better than abstract rules.

### 5. **Consider Reference Docs for Complex Skills (Low Priority)**
For TESTER pipeline or complex integrations:
```
manifests/pipelines/tester/
├── skill-navigator.md
└── references/
    ├── playwright-selectors.md
    └── recovery-patterns.md
```

**Benefit:** Keeps main skill focused, detailed docs loaded on-demand.

---

## What NOT To Adopt

### ❌ Model-Agnostic Skills
Hermes: Any model can use any skill.  
Worker Bee: Skills are model-specific (Scout skills ≠ Builder skills).

**Why keep ours:** The hive architecture requires specialization. Scout plans, Builder builds. They need different skills.

### ❌ User-Facing Documentation Style
Hermes skills explain HOW to use tools (user education).  
Worker Bee skills instruct WHAT to do in pipelines (model orchestration).

**Why keep ours:** Our skills are behavioral scripts, not tutorials.

### ❌ Installation/Prerequisites in Every Skill
Hermes includes setup instructions in each skill.  
Worker Bee assumes environment is ready (tools installed, MCP configured).

**Why keep ours:** Our skills run in controlled environment. Prerequisites belong in CLAUDE.md and setup docs, not repeated in every skill.

---

## Action Items

**Immediate:**
1. Add metadata block to all skill files (version, tags, pipeline info)
2. Add "Routing Triggers" section to pipeline skills
3. Add "Common Mistakes" to Builder and Checker skills

**Short-term:**
4. Create example briefs (good + bad) for skill-planner
5. Document pitfalls for skill-builder (partial files, context-blind changes)
6. Add workflow examples to TESTER pipeline skills

**Consider:**
7. references/ subdirectory for complex skills (TESTER, REPAIR)
8. Skill versioning system for tracking iterations
9. Tags for skill discovery (if we build skill marketplace later)

---

## Bottom Line

**Hermes Agent skills** = procedural guides for tool usage  
**Worker Bee skills** = behavioral scripts for pipeline execution

Both are valid. Ours are specialized for orchestration. Theirs are generalized for tool education.

**Best synthesis:** Adopt their metadata, triggers, and pitfalls sections while keeping our pipeline orchestration, hard gates, and status emissions.

**Updated skill template:**
```yaml
---
name: skill-name
description: One-line purpose
version: 1.0.0
metadata:
  pipeline: builder|tester|email|repair
  step: 1|2|3|4
  model: specific-model-name
  hands_off_to: next-skill
  tags: [relevant, keywords]
---

# Skill Title

**Model:** model-name
**Called by:** orchestrator
**Hands off to:** next-skill

## Routing Triggers
- Keywords that should route here
- User intent patterns
- Prerequisites

## Announce At Start
"What the model says when starting"

## Common Mistakes (What NOT To Do)
1. Don't do X because Y
2. Don't skip Z — it breaks W

## Step 1 — Action
Instructions
Emit: [MODEL:STATUS] message

## Hard Gate
<HARD-GATE>
Validation rule before handoff
</HARD-GATE>

## Example Outputs
[Good example]
[Bad example with explanation]
```

This gives us Hermes's discoverability + Worker Bee's orchestration.
