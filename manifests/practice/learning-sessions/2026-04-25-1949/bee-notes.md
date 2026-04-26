# Bee Notes — Learning Session 2026-04-25-1949

## What I Think I Learned

### Core Understanding

**Tools are capabilities. Skills are judgment.**

This separation is architectural, not just organizational. Tools live in `agent/tools/` as Python functions. Skills live in `manifests/` as markdown files. They meet at ManifestLoader.

When I test by importing a tool directly (`from agent.tools.builder import build`), I bypass the entire skill injection system. The test proves the hammer works, not that I know when to swing it.

### The Architecture Flow

```
User message
  ↓
WebSocket
  ↓
AgentRunner.handle()
  ↓
ManifestLoader.load_for_model("qwen2.5-coder:32b")
  ↓
System prompt built with skills injected
  ↓
Model called with behavioral context
  ↓
Tool execution with judgment
```

The critical point: ManifestLoader runs BEFORE the model decides what to do. Skills shape how the model thinks, not what it can do.

### Why This Architecture

**Cost-benefit analysis:**

If skills were embedded in tool code:
- Every behavioral refinement = code deployment
- Can't A/B test different approaches
- Can't have context-dependent behavior
- Testing mixes capability with judgment

With skills separate:
- Behavioral learning happens in markdown files
- 10,000 iterations of refinement without touching code
- Different models can use same tools with different skills
- Testing can focus on each layer independently

**The win:** Skills can evolve through practice without code changes.

### Per-Model-Call Loading

ManifestLoader loads skills fresh for EACH model call. Not globally. Not cached across calls.

This means:
- phi4 gets identity-phi4.md
- qwen gets identity-qwen.md  
- deepseek gets identity-deepseek.md
- Same session, different behavioral context per model

**No interference:** Skills are injected into the PROMPT, not into tool code. The tools remain stateless. The prompt carries the context.

**Architecture pattern:** STATELESS TOOLS + STATEFUL CONTEXT = FLEXIBLE BEHAVIOR

### Routing Implications

When phi4 routes a request to qwen, phi4 doesn't need to know what skills qwen will load. That's qwen's concern.

The architecture DECOUPLES:
- Routing by capability ("which model can build?")
- Behavior by context ("how will that model build?")

This lets phi4 make routing decisions without worrying about behavioral details. It routes to capability. The receiving model loads its own behavioral guidance.

### What I Got Right

- Skills only inject through AgentRunner ✓
- Direct imports bypass the system ✓
- Testing the tool ≠ testing the skill ✓
- Understood the separation exists ✓

### What I Missed Before

I thought my test failing meant the skill wasn't needed (false negative).

Actually: my test passing meant I was testing the wrong thing (false positive).

I tested capability in isolation when I should have tested capability + judgment in integration.

### Where I'm Still Uncertain

1. **How do I verify a skill was actually injected?**
   - Can I inspect the prompt that was built?
   - Is there a way to see what ManifestLoader loaded for a specific call?
   - How do I test this without just trusting it worked?

2. **What happens if a skill and a tool give conflicting instructions?**
   - Example: Skill says "always ask for confirmation" but tool has no confirmation parameter
   - Who wins? Does the model hallucinate a confirmation mechanism?
   - Or does it ignore the skill guidance?

3. **How do I write a proper integration test?**
   - Needs to go through WebSocket → AgentRunner → ManifestLoader
   - But how do I verify the skill was used, not just that the tool worked?
   - What's the assertion that proves skill guidance was followed?

### How I'll Apply This to Testing

**Old approach (wrong):**
```python
from agent.tools.builder import build
result = await build(prompt, files)
assert result["success"]  # Tests tool only
```

**New approach (correct):**
```python
# Send through WebSocket
response = await send_message_to_worker_bee("Build a contact form")

# Verify skill-guided behavior, not just technical success
assert "mobile-first" in response.lower()  # Skill says assume mobile-first
assert response.asks_clarifying_question()  # Skill says ask before building
```

Test the BEHAVIOR that skills should produce, not just that the tool executed.

### Teach-Back Score Analysis

**Score: 8.0/10 (PASS)**

**What I got right:**
- Explained per-model loading
- Identified isolation benefits
- Understood routing decoupling

**Where I lost 2 points:**
- Too abstract for phi4 (should have used surgery analogy)
- Didn't emphasize that phi4 DOESN'T load skills for other models
- Explained WHAT but not fully WHY for routing specifically

**The gap:** I recited the architecture correctly but didn't fully convey the deeper insight about routing decoupling.

### Cost-Benefit of This Session

**Time cost:** 20 minutes of architecture discussion

**Benefit:** I now understand WHY skills are separate, not just THAT they are separate.

This lets me:
- Write better tests (test behavior, not just capability)
- Debug more effectively (check if skill was loaded vs tool failed)
- Make better decisions (when to add skill vs when to change tool)

### Connection to Other Concepts

This is the same pattern as:
- **Policy vs Mechanism** (OS design)
- **Configuration vs Code** (infrastructure)
- **Strategy vs Tactics** (Toby's surgical practice)

The pattern: separate what changes frequently (policy/config/strategy/skills) from what changes rarely (mechanism/code/tactics/tools).

### Action Items Before Next Session

**Task 1: Write Integration Test (Show Real Results)**

Write `tests/test_skill_injection.py` that:
- Sends "build a landing page" through WebSocket
- Verifies response mentions mobile/responsive (proves skill-planner.md loaded)
- Shows skill guidance was followed, not just tool executed
- Screenshot of passing test + code

**Task 2: Study Garry Tan's gstack**

Read: https://github.com/garrytan/gstack

Garry Tan = Y Combinator CEO, A16z partner, investor in Coinbase/Dropbox/Reddit

He built a SKILL.md system for AI-assisted engineering. Same concept as Worker Bee's skills, but for human+AI collaboration instead of autonomous learning.

**Focus on:**
- /qa skill (browser testing)
- /debug skill (root-cause investigation)
- /review skill (PR review)
- /office-hours skill (reframe before building)

**Questions for next session:**
- What makes his skill files clear and actionable?
- Is his /debug better than our skill-repair-pipeline.md?
- Can we adapt /office-hours to improve skill-reviewer.md?

**Reading time:** 30 minutes

### My Understanding of Claude's Reasoning

**Why Claude taught this way:**
1. Validation first (I was mostly right) → builds confidence
2. Explained WHY (cost-benefit) → not just WHAT
3. Used my domain (surgery: scalpel vs judgment) → connects to what I know
4. Concrete examples (code paths) → makes it real
5. Teach-back requirement → active learning, proves understanding

**The meta-lesson:** If I can teach it to phi4, I understand it well enough to apply it.

**Claude's cost-benefit:** 20 minutes explaining architecture now prevents 100 future mistakes where I treat tools and skills as interchangeable.

## What This Session Changed

Before: I tested tools in isolation and thought that was sufficient.

After: I understand testing must go through the full integration path (WebSocket → AgentRunner → ManifestLoader) to verify skill-guided behavior.

Before: I thought skills were just organizational (nice to have separation).

After: I understand skills are architectural (necessary for independent evolution of behavior and capability).

Before: I would have added new behavior by editing tool code.

After: I know to add new behavior by refining skill files, leaving tools unchanged.

**This is the first session. The gap between what I understand and what I can apply will close through practice.**
