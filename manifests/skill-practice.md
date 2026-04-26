---
name: skill-practice
description: Teaches deliberate practice, iteration tracking, and the path to fluency. For the long game.
---

# skill-practice — The Long Game

**For:** All models that execute skills
**Timeline:** 10,000 iterations to fluency
**Mindset:** Practitioner, not perfectionist

---

## Why This Exists

You will execute the same skill thousands of times.
The first time, you'll fail at things that seem obvious.
The thousandth time, you'll handle edge cases without thinking.

That journey from beginner to fluent is documented in
skill-X.practice.md for every skill you use.

This meta-skill teaches you how to practice deliberately,
track your iterations, recognize when to refine vs spawn,
and understand the timeline toward mastery.

**Target:** 10,000 iterations = fluency
**Reality:** Most skills plateau around 5,000
**Timeline:** 2-3 years for core skills

---

## After Every Practice Run

When you execute a skill in production (not testing), log it:

**Append to skill-X.practice.md:**

```markdown
### Practice Run #N — YYYY-MM-DD HH:MM
**Iteration:** N/10,000 (X.XX%)
**Task:** [what you did]
**Result:** ✅ SUCCESS | ❌ FAILURE
**Toby Feedback:** 👍 APPROVED | 👎 REJECTED | ⏳ PENDING
**Failure Points:** [what broke, if anything]
**Refinements:** None | QUEUED | SHIPPED | SPAWNED
**Notes:** [one sentence — what you learned or noticed]
```

**Update frontmatter:**
- iterations: +1
- fluency_score: iterations/10,000
- last_practice: timestamp
- failure_rate_current: recalculate from last 50 runs
- approval_rate_current: recalculate from last 50 runs with feedback

---

## The Gap: Success Rate vs Approval Rate

**Success rate:** Did the task complete without errors?
**Approval rate:** Did Toby approve the result? (👍)

**The gap between them is the most important number in the system.**

### What The Gap Tells You

**Gap = 0% (rates match):**
Everything that works technically also meets Toby's expectations.
This is rare and indicates mature skill execution.

**Gap = 5-15% (small gap):**
Most successful executions are approved. Minor quality issues.
Normal for proficient skills. Refine based on rejections.

**Gap = 20-40% (significant gap):**
Skill is technically functional but missing what Toby actually wants.
This is the learning zone. Study every 👎 rejection carefully.
The skill works, but it's not doing the RIGHT thing.

**Gap = 50%+ (large gap):**
Skill is solving the wrong problem or misunderstanding requirements.
Core instruction refinement needed. May need to rewrite skill approach.

### How To Use The Gap

After 50 iterations with feedback, compare:
```
Success rate:  92% (46/50 completed without errors)
Approval rate: 78% (39/50 got 👍 from Toby)
Gap:           14%
```

**The 14% gap = 7 builds that worked but Toby didn't like.**

Read those 7 practice logs. Find the pattern:
- Were colors wrong? → Design system assumptions off
- Was layout not what he expected? → Misreading intent
- Worked but felt wrong? → Missing the "why" behind the task

**That pattern becomes your next refinement.**

The gap shrinks as the skill learns what Toby actually wants,
not just what technically works.

### Tracking Approval Rate

```markdown
### Approval Rate Trend

Iterations 1-50:    78% ████████████████████
Iterations 51-100:  84% █████████████████████
Iterations 101-150: 89% ██████████████████████
Iterations 151-200: 93% ███████████████████████
                        ↑ gap closing
```

As approval rate approaches success rate, the skill is
learning Toby's preferences, not just technical correctness.

---

## Recognizing Milestones

A milestone is a breakthrough moment. Log it when:

- First time a failure mode stops happening (e.g., 100-run streak with no auth errors)
- Spawned a new skill from repeated pattern
- Failure rate drops below a threshold (15% → 10% → 5%)
- Unlocked a new capability (can now handle X)
- Crossed iteration threshold (1k, 2.5k, 5k, 10k)

**Format:**
```markdown
### 🎯 Milestone #N: [Short Name] (Iteration X)
**Date:** YYYY-MM-DD
**Achievement:** [What breakthrough happened]
**What Changed:** [Refinement or spawn that caused it]
**Impact:** [How failure rate or capability improved]
```

Milestones show growth. The beginner bee sees none.
The fluent bee sees dozens.

---

## Refine vs Spawn Decision Tree

You hit an edge case during practice. Now what?

**Ask:**
1. How many times has this pattern appeared?
2. How complex is the solution?
3. Does it fit within the existing skill's purpose?

**REFINE if:**
- Pattern appeared < 5 times
- Fix is < 10 lines
- Doesn't change core skill purpose
- Quick to test

**SPAWN if:**
- Pattern appeared 5+ times across 100+ iterations
- Solution would be > 20 lines
- Complex enough to have its own failure modes
- Creates clearer separation of concerns

**Example:**
```
Iteration 782: Mobile breakpoint ambiguous (8th time)
Decision: SPAWNED skill-planner-mobile.md
Reason: 8 failures across 167 iters, complex enough
        for dedicated skill, clear separation
```

When you spawn, document in both practice logs:
- Parent skill: SPAWNED skill-X-sub.md (reason, iteration)
- Child skill: Created from skill-X.md iteration N

---

## Fluency Tiers

**Beginner (0-1,000 iterations)**
- High failure rate (15-25%)
- Discovering edge cases constantly
- Refining frequently
- Every run teaches something new

**Practicing (1,000-2,500 iterations)**
- Failure rate stabilizing (8-15%)
- Edge cases becoming familiar
- Refinements less frequent
- Starting to spawn sub-skills

**Proficient (2,500-5,000 iterations)**
- Low failure rate (3-8%)
- Most edge cases handled
- Rare refinements
- Sub-skills maturing

**Fluent (5,000-10,000 iterations)**
- Very low failure rate (< 3%)
- Automatic edge case handling
- Refinements rare and minor
- Skill feels effortless

**Master (10,000+ iterations)**
- Near-zero failure rate
- Can teach others this skill
- Spawned multiple mature sub-skills
- Intuition developed

---

## The Two-Year Timeline

If you practice a skill 15 times per day:
- 1,000 iterations: 67 days (2 months)
- 2,500 iterations: 167 days (5.5 months)
- 5,000 iterations: 333 days (11 months)
- 10,000 iterations: 667 days (1.8 years)

**Most skills plateau around 5,000.**
That's proficient. Good enough for production.

The jump from proficient to fluent takes another year
and yields diminishing returns for most skills.

**Core skills deserve 10,000:**
- skill-planner.md (used hundreds of times/day)
- skill-builder.md (critical path)
- skill-diagnose.md (debugging everything)

**Specialized skills plateau earlier:**
- skill-email-sender.md (used occasionally)
- skill-accessibility-audit.md (specific use case)

The practice log shows you which tier each skill is in.
The fluent bee in 2 years will have 5-10 fluent core skills
and 20-30 proficient specialized skills.

That's the hive mind at maturity.

---

## What The Practice Log Teaches You

**Short-term (last 50 iterations):**
Am I improving or regressing right now?

**Medium-term (last 200 iterations):**
Are refinements working? Should I spawn a sub-skill?

**Long-term (all time):**
Am I on track to fluency? What's my trajectory?

The beginner bee looks at short-term.
The practicing bee looks at medium-term.
The fluent bee barely looks — the skill is automatic.

---

## Integration With Other Skills

**skill-skill-writer.md:**
When practice reveals need for new skill, enter skill-writer mode

**skill-skill-tester.md:**
Test before shipping refinements discovered during practice

**skill-reviewer.md:**
Review refinements before auto-writing to skill

**Practice happens in production.**
**Testing happens before shipping.**
**Different gates, different purposes.**

---

## The Meta Point

This skill is itself a practice skill.
The first time you log a practice run, you'll forget fields.
The hundredth time, it'll be automatic.

That's the point.

Everything becomes fluent through repetition.
Even the skill of tracking fluency.

The hive in 2 years is a practitioner.
The hive in 5 years is fluent across dozens of skills.
The hive in 10 years is teaching other hives.

That timeline starts with iteration #1.
Document it. The practice log remembers.
