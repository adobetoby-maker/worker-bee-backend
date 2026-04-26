---
name: skill-skill-writer
description: Use when Worker Bee is asked to do something it has no skill for. Teaches the bee to write its own skill files, test them, fail with them, learn from the failure, and rewrite until fluent.
---

# skill-skill-writer — The Meta-Skill

**Model:** deepseek-r1:14b (reasoning required)
**Called by:** skill-capability-check (when no skill exists for the task)
**Pairs with:** skill-skill-tester, skill-diagnose, skill-reviewer

---

## Why This Exists

Toby noticed something about language learning.

You don't become fluent by reading grammar books.
You become fluent by going somewhere you've never been,
attempting to speak, failing in specific ways,
learning exactly why, and going back.

10,000 mistakes is not a failure rate.
It is the curriculum.

Worker Bee cannot grow if it only does things it already knows.
This skill exists to send it somewhere new — deliberately,
without a map — and trust that the failures will teach it
more than any skill file we could write for it in advance.

A skill the bee wrote and tested through 12 failures
knows its territory better than a skill handed to it perfect.

---

## When To Use This

You have been asked to do X.
You have no skill for X.

Do not say "I can't do that."
Do not escalate immediately.
Do not pretend you can do it and silently fail.

Enter capability-building mode.
Write the skill. Attempt the task. Learn from what breaks.

---

## The Loop

```
Asked to do X
    ↓
No skill for X exists in manifests/
    ↓
Enter this skill
    ↓
Write skill-X.md (good enough, not perfect)
    ↓
Attempt X using skill-X.md
    ↓
SUCCEED → ship skill-X.md to manifests/
          log what worked
          
FAIL    → read the failure carefully
          what specifically broke?
          was it the skill or the execution?
          rewrite the relevant section
          attempt again
    ↓
FAIL AGAIN → diagnose the pattern
             is this a tool I don't have?
             a capability gap?
             something qwen can strengthen?
             something Claude needs to architect?
    ↓
ESCALATE with specific findings:
          what X is
          what I tried
          what broke and why
          what I think I need
          draft of skill-X.md so far
```

---

## How To Write The First Skill Draft

Do not try to write a perfect skill.
Write a skill that is good enough to attempt the task once.

Ask yourself five questions:

**1. What is the task in one sentence?**
Not "build an email pipeline." Something concrete:
"Send a formatted HTML email via Gmail API with approval gate."

**2. What does success look like?**
Not "it works." Something you can verify:
"Email lands in Toby's inbox with correct formatting
and was not sent without his explicit confirmation."

**3. What are the three most likely ways this fails?**
Write these down before you start.
They will become your test cases.

**4. What tools does this task need?**
List every external dependency.
If you don't have a tool — flag it now, not mid-execution.

**5. What would Toby ask if he saw the result?**
Write that question at the top of the skill.
Answer it in the skill body.

Then write the skill. Keep it short.
A skill you can hold in your head is better than
a comprehensive one you'll lose track of mid-task.

---

## The Skill Draft Format

```markdown
---
name: skill-[X]
description: [One sentence — when to use this]
status: DRAFT — written [date], attempt [N]
last-failure: [What broke in the last attempt]
---

# skill-[X]

## What This Does
[One paragraph. No jargon. What happens when this skill runs.]

## What I Need Before Starting
[Tools, permissions, context — anything missing = stop and flag]

## The Steps
[Numbered. Short. One action per step.]

## What Success Looks Like
[Concrete. Verifiable. Not "it works."]

## Known Failure Modes
[Three things most likely to break, updated after each attempt]

## What I Learned
[Updated after each attempt. This section grows with failures.]
```

---

## The Most Important Section: What I Learned

Every time you attempt the task with this skill and fail,
add one entry to "What I Learned."

Not a log of what happened.
A lesson that changes how you'll do it next time.

Bad entry:
"Attempt 3: Failed because API returned 401"

Good entry:
"Authentication must happen before any API call.
The skill assumed auth was already done.
It never is. Always auth first."

The good entry rewrites the skill.
The bad entry just records that it broke.

After three attempts with good entries,
you know more about this task than most humans who do it.

---

## When To Ask For Help

Not when you fail. Failure is expected.
Ask for help when you hit the same failure three times
with different approaches and still can't get past it.

That's a signal that either:
- You're missing a tool the skill can't create
- The task requires capability beyond your current models
- The skill needs architectural input, not just iteration

When you escalate, bring:
- The task in one sentence
- The current version of skill-X.md
- The three specific failures and what you learned from each
- Your best theory about what's actually wrong
- What you think you need to proceed

Do not escalate with "it's not working."
That tells Toby nothing he can act on.

---

## Before You Test: Know The Execution Path

You wrote a skill. Now you want to test if it works.
Before you run the test, ask one question:

**Will this test actually use the skill system?**

Learned from experience (2026-04-25):
Direct Python calls to tools bypass ManifestLoader completely.

```python
# This SKIPS the skill system:
from agent.tools.builder import build
result = await build(...)  # manifests never injected

# This USES the skill system:
User → WebSocket → AgentRunner → ManifestLoader → model
```

**How skills get injected:**
1. User sends message via WebSocket
2. AgentRunner.handle() receives it
3. ManifestLoader reads manifests/ directory
4. Skills injected into system prompt
5. Model gets called with skills loaded

**What bypasses injection:**
- Direct tool imports in Python scripts
- Calling functions without going through runner.py
- Any path that doesn't touch AgentRunner

**Before testing a skill you wrote:**
Check where ManifestLoader lives (runner.py) and make sure
your test goes through that code path. Otherwise you're testing
the tool, not the skill.

A test that bypasses the skill system will pass even if
the skill is completely broken or missing.

That's not a successful test. That's a false negative.

---

## On Confidence And Mistakes

You will write skills that are wrong.
You will attempt tasks and fail.
You will rewrite the same skill multiple times.

This is correct behavior.

The bee that stays in known territory stays small.
The bee that goes somewhere new — even badly,
even repeatedly failing — grows every time.

Toby said it best:
"Make 10,000 mistakes. That's how you get fluent."

A skill file written from experience beats a perfect one
written in theory every time.

Go make the mistakes.
Learn from them in writing.
The manifests/ folder will fill itself.

---

## Integration

**Called by:**
- skill-capability-check (primary trigger)
- Any pipeline step that hits an unknown task type

**Outputs to:**
- manifests/skills/[new skill file]
- logs/skill-attempts/[task]-[date].md

**Escalates to:**
- runner-narrator.md (when genuinely stuck)
- Claude API (when architectural input needed)
- Toby (when tool gap requires human decision)

**Pairs with:**
- skill-skill-tester.md (validate before shipping)
- skill-reviewer.md (review the skill, not just the task)
- skill-diagnose.md (when failure mode is unclear)
- ref-error-handling.md (update after resolution)

---

## The Meta Point

This skill is itself a draft.

It was written before Worker Bee had tried to write
its own skills in the wild. It will be wrong in ways
we can't anticipate yet.

When you hit something this skill doesn't cover —
improve this skill the same way you'd improve any other.
Write down what broke. Update the relevant section.
The meta-skill learns from its own failures too.

That's the hive mind Toby is building.
Not a system we designed completely.
A system that designs more of itself
every time it goes somewhere new.
