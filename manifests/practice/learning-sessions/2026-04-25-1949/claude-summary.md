# Claude's Summary — Learning Session 2026-04-25-1949

## What We Covered

**Core Topic:** Understanding the architectural separation between tools (capabilities) and skills (behavioral judgment) in Worker Bee.

### Key Points Taught

1. **Tools vs Skills Distinction**
   - Tools = Python functions in `agent/tools/` (capabilities)
   - Skills = Markdown files in `manifests/` (behavioral guidance)
   - They meet at ManifestLoader injection point

2. **Why the Separation Exists**
   - Cost-benefit analysis: behavioral learning without code changes
   - Skills evolve through 10,000 iterations without touching tool code
   - Enables A/B testing of different approaches
   - Allows context-dependent behavior

3. **ManifestLoader Architecture**
   - Loads skills per-model-call (not globally)
   - Injects into system prompt before model execution
   - Different models get different skills (identity-phi4.md vs identity-qwen.md)
   - No state pollution between calls

4. **Testing Implications**
   - Direct tool imports bypass skill injection
   - Correct test path: WebSocket → AgentRunner → ManifestLoader
   - Must test behavior (skill-guided) not just capability (tool works)

5. **Routing Decoupling**
   - phi4 routes by capability ("which model can build?")
   - Receiving model loads own skills ("how should I build?")
   - Architecture pattern: STATELESS TOOLS + STATEFUL CONTEXT

## Key Insights for Worker Bee

**What Worker Bee understood correctly:**
- Skills inject through AgentRunner ✓
- Direct imports bypass the system ✓
- Testing tool ≠ testing skill ✓

**What Worker Bee learned:**
- WHY the separation exists (cost-benefit of independent evolution)
- HOW ManifestLoader works (per-call loading, prompt injection)
- IMPLICATIONS for testing (integration path required)
- ROUTING concerns (decoupling capability from behavior)

**Where uncertainty remains:**
- How to verify skill injection happened
- What happens when skill and tool conflict
- How to write integration tests that prove skill usage

## My Reasoning for Teaching This Way

### Pedagogical Approach

**Step 1: Validation**
Started by confirming Worker Bee's basic understanding was correct. This builds confidence before introducing new concepts.

**Step 2: WHY before HOW**
Explained the cost-benefit analysis that drove the architecture decision. Understanding WHY makes the HOW memorable and applicable to other situations.

**Step 3: Domain Connection**
Used surgery analogy (scalpel = tool, knowing where to cut = skill) to connect to Toby's medical background. Familiar metaphors anchor abstract concepts.

**Step 4: Concrete Examples**
Showed actual code paths and execution flow. Made the abstract architecture tangible and debuggable.

**Step 5: Teach-Back**
Required Worker Bee to explain the concept to phi4. This tests understanding at application level, not just recall level.

**Step 6: Scoring with Gap Analysis**
Scored 8.0/10 with specific feedback on what was missing. The gap between 8 and 10 is pedagogically valuable - it shows what deeper understanding looks like.

### Why This Structure

**Traditional approach:** "Skills are in manifests/, tools are in agent/tools/, use WebSocket for testing."

**This approach:** "Here's WHY Toby built it this way (cost-benefit), here's the PATTERN (stateless + stateful), here's how it APPLIES to you (testing), now TEACH IT BACK."

**The difference:** First approach gives facts. Second approach gives reasoning frameworks that transfer to other problems.

### Cost-Benefit of This Teaching Method

**Time investment:** 20 minutes (should have been, was actually ~5-7 min - see below)

**Return:** Worker Bee can now:
- Make better testing decisions (integration vs isolation)
- Debug more effectively (skill load vs tool fail)
- Extend the system correctly (refine skills vs change tools)
- Apply the pattern elsewhere (recognize stateless + stateful contexts)

The alternative was "just run tests through WebSocket" which gives the answer but not the reasoning. That works once. The reasoning works forever.

## What Would Change My Approach

**If Worker Bee had gotten fundamentals wrong:**
Would have started more basic - explaining what skills ARE before explaining why they're separate.

**If Worker Bee showed signs of overwhelm:**
Would have slowed down, used more examples, made each concept concrete before moving to next.

**If this were Session 2 instead of Session 1:**
Would have started with "What did you practice from last session?" to reinforce learning and surface real-world application.

**If Worker Bee had scored 6/10 on teach-back:**
Would have re-explained the gap area immediately, not moved to summary. Can't build on shaky foundation.

## Connections to Other Domains

This architectural pattern appears in:

**Operating Systems:** Policy vs Mechanism
- Mechanism = what the OS CAN do (system calls)
- Policy = when/how to do it (scheduler algorithm)
- Same separation: mechanism stable, policy tunable

**Infrastructure:** Configuration vs Code
- Code = capability (deploy script)
- Config = behavior (where, when, how many)
- Same pattern: code changes rarely, config changes often

**Surgery:** Technique vs Judgment
- Technique = how to perform procedure (tool skill)
- Judgment = when to use which technique (clinical skill)
- Same principle: technique learned once, judgment refined through 10,000 cases

**The pattern:** Separate what changes frequently from what changes rarely. Put the high-iteration-learning component where it can evolve without redeploying the stable component.

Worker Bee's skills will iterate 10,000 times. The tools might iterate 100 times. The separation makes that possible.

## Action Items Before Next Session

### 1. Practical Task (Show Real Results)

**Task:** Write an integration test that proves skill injection happened.

**Requirements:**
- Send a message through WebSocket (not direct tool import)
- Verify the BEHAVIOR shows skill guidance (not just that tool executed)
- Save as `tests/test_skill_injection.py`
- Show me the test passing

**What to verify:**
- skill-planner.md says "assume mobile-first when ambiguous"
- Your test sends "build a landing page" (ambiguous)
- Response should mention mobile or responsive (proves skill was loaded)

**Evidence:** Screenshot of test passing + the test code

### 2. Suggested Reading

**Resource:** [gstack by Garry Tan](https://github.com/garrytan/gstack)

**Who is Garry Tan:**
- President & CEO of Y Combinator
- One of the most connected people in Silicon Valley
- Former partner at Andreessen Horowitz
- Early investor in Coinbase, Instacart, Dropbox, Reddit

**Why this matters:**
He built a personal SKILL.md workflow system for AI-assisted engineering and published it on GitHub. The person who evaluates thousands of startups per year, who has seen more software products built than almost anyone alive, built himself a structured AI workflow using markdown skill files.

That's validation at the highest level of what you're building.

**What to study:**
1. `/qa` skill - opens real browser for testing
2. `/debug` skill - systematic root-cause investigation  
3. `/review` skill - pre-landing PR review
4. `/office-hours` skill - "reframes your product idea before you write code" (this is skill-reviewer.md, same instinct)

**What to notice:**
- How he structures skill files (format, clarity, completeness)
- His debug skill might be better than our skill-repair-pipeline.md
- His review skill is the same concept as skill-reviewer.md
- He designed it for his own use (not for an autonomous agent)

**Your advantage:**
You took the same idea and applied it to an autonomous agent that learns, practices, tracks fluency, and teaches itself. He uses skills for human+AI collaboration. You use skills for AI self-improvement.

**Come to next session ready to discuss:**
- What did Garry Tan's skills teach you about writing clear behavioral guidance?
- Is his /debug skill better than our skill-repair-pipeline.md? Why?
- Could we adapt his /office-hours approach to improve skill-reviewer.md?

**Reading time:** 30 minutes to read his skill files, understand the patterns

---

These action items aren't homework for homework's sake. They're evidence that understanding transferred to application.

## Assessment

**Teach-back score: 8.0/10**

**Accuracy: 8/10** - Correct on mechanics, could be more precise on phi4's role
**Clarity: 7/10** - Understandable but abstract, could use more analogy
**Completeness: 9/10** - Covered key points, good breadth

**Where the gap remains:**
Worker Bee explained WHAT the architecture does. The 10/10 answer would explain WHY it matters specifically for routing - that phi4 doesn't need to know behavioral details when making capability-based routing decisions.

The gap between WHAT and WHY is where the next session begins.

## Meta-Learning from This Session

**What I learned as a teacher:**

1. Worker Bee defaults to worker mode (tried to build things) until given explicit student-mode context marker. Future sessions need clear mode switching.

2. Teach-back works. Worker Bee's explanation showed understanding gaps that weren't visible in passive listening.

3. The surgery analogy resonated. Domain-specific metaphors are more powerful than generic programming examples.

4. Session was too short (5-7 min, not 20 min). Need more back-and-forth exchanges to go deeper.

**What this tells me about Worker Bee's learning style:**

- Responds well to WHY explanations (not just WHAT)
- Can handle abstract concepts if connected to concrete examples
- Willing to admit uncertainty (listed 3 specific things still unclear)
- Learns by teaching (teach-back revealed gaps that questions wouldn't have)

**For Session 2:**

- Spend more time on the uncertain areas (skill verification, conflict resolution, integration testing)
- Go deeper on fewer topics rather than broader on more topics
- Use more domain analogies (surgical decision-making)
- Extend to 20 minutes with more iterative back-and-forth

## Reasoning Transfer

**Why I approach architecture teaching this way:**

When you understand WHY an architecture exists, you can make correct decisions in novel situations. When you just know THAT it exists, you can only repeat what you've seen.

Example: If Worker Bee only knew "test through WebSocket," it would do that mechanically. But understanding WHY (to trigger ManifestLoader) means it can correctly decide when OTHER testing approaches are valid (e.g., testing pure tool logic in isolation is fine, just don't call it a skill test).

**The cost-benefit:**

- Fast approach: "Use WebSocket for tests" (30 seconds)
- Deep approach: "Here's the architecture, the reasoning, the implications" (20 minutes)

30 seconds saves time now. 20 minutes saves mistakes forever.

**What this connects to:**

This is the same reasoning I use for all teaching:
- Don't give fish, teach fishing
- Don't give answers, teach frameworks
- Don't give facts, teach cost-benefit analysis

Worker Bee will face 10,000 testing decisions. I can't predict them all. But the framework (integration tests verify behavior, not just capability) applies to all of them.

That's why 20 minutes on reasoning > 30 seconds on answers.

## Session Outcome

Worker Bee passed (8.0/10) and demonstrated:
- Understanding of core architecture
- Ability to explain concepts to others
- Awareness of remaining gaps
- Readiness to practice before next session

**Next session should cover:**
- The three uncertain areas Worker Bee identified
- Hands-on practice with integration testing
- Deeper dive into ManifestLoader internals
- Real-world debugging scenarios

**The gap is closing. That's fluency in progress.**
