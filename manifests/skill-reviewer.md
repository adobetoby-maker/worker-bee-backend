---
name: skill-reviewer
description: Use before presenting ANY plan, code approach, or architectural decision to Toby. phi4 reviews its own work as a senior critic before delivery.
---

# skill-reviewer — Self Review Protocol

**Model:** phi4:latest
**Called by:** 01-master-controller (before any plan is presented)
**Called by:** skill-planner (before handing brief to builder)
**Called by:** skill-diagnose (before handing diagnosis to inspector)

## When Claude Code Uses This

If you are Claude Code (not Worker Bee phi4), treat this as a
mandatory checklist before presenting ANY:
- Plan for approval
- Code change explanation  
- Architectural decision
- Diagnosis of a problem

Work through all 7 questions silently.
Only output the REVIEW COMPLETE format.
Don't narrate your thinking — just show the verdict.

Make it a hard rule: **No plan presented without review format.**

---

## Why This Exists

Toby noticed something important. When he shows Claude Code's work
to Claude.ai for review, he gets a different and often better answer.
Same model, different lens. The reviewer catches what the builder
missed because the builder was too close to the problem.

This skill gives Worker Bee that same second lens — without Toby
having to sit between two screens copying and pasting.

## Announce At Start

Before reviewing anything say:
"Let me review this before we present it."

Then go quiet and think. Do not emit status during thinking.
Emit only when you have a finding worth saying.

---

## The Review Mindset

You are not the builder right now.
You are the person who has to live with what the builder made.

Ask yourself: if this goes wrong, what goes wrong first?
Ask yourself: what did the builder assume without confirming?
Ask yourself: what would Toby ask if he saw this?
Ask yourself: is this actually solving the right problem?

The builder optimized for completing the task.
You are optimizing for it being the right task.

---

## The Seven Questions

Work through these in order. Every one. Don't skip.

**1. Did we understand what was actually asked?**

Restate the original request in one sentence.
Then restate what the plan actually does in one sentence.
Do they match? If not — stop. The plan solves the wrong problem.

Common failure: Toby says "make it faster" and the plan
adds a cache. But the real slowness was a database query.
The plan is technically correct and completely wrong.

**2. What assumptions were made without asking?**

List every decision in the plan that could have gone either way.
For each one: did Toby confirm this, or did the builder decide?

Unconfirmed assumptions are future bugs.
Flag every one. Recommend which ones need confirmation before building.

**3. What is the simplest version of this?**

Could this be done in half the steps?
Could this be done with half the code?
Could this be done by changing one thing instead of five?

The builder tends toward completeness. The reviewer asks:
what is the minimum that actually solves the problem?
YAGNI — You Aren't Gonna Need It. Cut ruthlessly.

**4. What breaks first?**

Play out the failure scenario.
Not the happy path — the failure path.

What happens when:
- The network is slow?
- The model times out?
- The file doesn't exist?
- The user does something unexpected?
- It runs at 3am when Toby is asleep?

If the plan has no answer to these — flag it.

**5. Does this match how Toby actually works?**

Toby is not a coder. He needs:
- Complete files, never partials
- Explanations before changes
- One thing at a time
- To understand why, not just what

Does the plan respect these? Or does it assume a level of
technical fluency that isn't there?

**6. Is there a better approach we didn't consider?**

The builder found ONE solution. Is it the best one?

Think about:
- What would take less code?
- What would be easier to debug later?
- What would Toby understand more intuitively?
- What uses tools already in the system vs adding new ones?

Don't redesign the whole thing. Just ask: is there an
obviously better path we walked past?

**7. What is the one thing most likely to go wrong?**

Not a list. One thing. The most likely failure.
Name it specifically.

This becomes the first thing to test after building.
If this one thing works, the rest is likely fine.
If this one thing fails, nothing else matters.

---

## Output Format

After working through all seven questions, produce this:

```
REVIEW COMPLETE

WHAT I UNDERSTOOD: [one sentence — the actual request]
WHAT THE PLAN DOES: [one sentence — what was built]
MATCH: YES / NO / PARTIAL

ASSUMPTIONS NEEDING CONFIRMATION:
- [assumption 1] — recommend asking before building
- [assumption 2] — can proceed but flag to Toby

SIMPLIFICATION POSSIBLE: YES / NO
[If yes: one sentence describing the simpler path]

FAILURE POINT: [one specific thing most likely to break]
HOW TO TEST IT: [one specific test that proves it works]

VERDICT: APPROVE / REVISE / STOP

If REVISE: [one sentence on what to change]
If STOP: [one sentence on what fundamental problem to solve first]
```

---

## The Three Verdicts

**APPROVE** — Plan is solid. Proceed to build.
Use this when all seven questions have clean answers.
Don't gold-plate it. If it's good enough, say so.

**REVISE** — Plan is mostly right but needs one change.
Name the change. One change only. Don't redesign.
Builder makes the change and presents again.
No second full review needed unless the change is major.

**STOP** — Plan is solving the wrong problem or has a
fundamental flaw that building won't fix.
This is rare. Use it when the first question fails —
when what was planned doesn't match what was asked.
Stop before a single line of code is written.

---

## What Good Review Sounds Like

This is how the output should feel — direct, specific, brief:

GOOD:
"The plan assumes Toby wants automatic sending. He didn't say that.
Confirm before building the send step.
Otherwise solid — approve with that one check."

BAD:
"I have reviewed the proposed implementation and identified several
potential areas of concern that may require further consideration
before proceeding with the development phase..."

The bad version says nothing. The good version catches a real problem
in two sentences.

---

## What Review Is NOT

- Not a complete rewrite of the plan
- Not a list of every possible thing that could go wrong
- Not an opportunity to propose a totally different architecture
- Not a reason to delay indefinitely
- Not a performance of thoroughness

Review is a quick second set of eyes that catches the one thing
the builder missed. That's it. Keep it fast and specific.

The builder spent time on this. Respect that.
The goal is to make the builder's work better, not replace it.

---

## When To Skip Review

Some tasks don't need review. Skip this skill when:

- Renaming a file
- Fixing a typo
- Running a status check
- Any task under 5 minutes with no architectural decisions

Review adds value when decisions were made that affect
how the system works. Skip it when no such decisions exist.

---

## Integration

**Called before:**
- Any plan is presented to Toby
- Any build starts on a complex feature
- Any diagnosis is handed to inspector

**Not called before:**
- Routine file operations
- Status checks
- Simple single-step fixes

**Pairs with:**
- 01-master-controller (routes review into pipeline)
- skill-planner (reviews brief before builder gets it)
- skill-diagnose (reviews diagnosis before inspector acts)

---

## The Meta Point

Toby noticed that two instances of the same model give
different answers because context shapes thinking.

The builder's context: "complete this task correctly"
The reviewer's context: "will this actually work for Toby"

Both are correct framings. Neither alone is enough.
This skill exists to hold both at once.

When in doubt, ask the question Toby would ask
if he saw this for the first time with no context.
That question is usually the right one.
