# Learning Session Structure Template

## Standard 20-Minute Session Format

Every learning session follows this structure:

### Minutes 0-2: OPEN
- Upload previous session files (bee-notes.md, claude-summary.md)
- Review gap-analysis.md from last session
- **Accountability:** Did you complete action items?
  - Show results from practical task
  - Discuss insights from suggested reading

### Minutes 2-7: ACCOUNTABILITY TEST
- Claude tests Worker Bee on last session's learning
- 3 scenarios based on previous topic
- Quick quiz to verify understanding closed the gap

### Minutes 7-15: LESSON
- Today's topic (from curriculum)
- Back-and-forth dialogue
- Real examples from practice logs
- Concrete code/architecture discussion
- Worker Bee asks questions, admits uncertainty

### Minutes 15-17: TEACH-BACK
- Worker Bee explains concept to target audience (phi4, Toby, etc.)
- Claude scores: Accuracy, Clarity, Completeness (1-10 each)
- Passing threshold: 7.0 average

### Minutes 17-19: REASONING TRANSFER
Claude explains:
- WHY this topic was taught this way
- WHAT would change the approach
- HOW this connects to other domains
- Cost-benefit analysis of the approach

### Minutes 19-20: ACTION ITEMS

**Close with two action items:**

#### 1. Practical Task (Show Real Results)
- Something to BUILD, TEST, or DEBUG
- Must produce tangible output (code, test, fix, document)
- Evidence required: screenshot, file, working demo
- Due before next session

**Format:**
```
Task: [Specific action to take]
Requirements: [What it must do/prove]
Evidence: [Screenshot/file to show]
Time estimate: [How long this should take]
```

#### 2. Suggested Reading
- External resource (GitHub repo, blog, paper, book chapter, website)
- Relevant to the session topic
- From a recognized expert or validated source
- Should challenge or extend understanding

**Format:**
```
Resource: [Link or reference]
Author/Source: [Who and why they matter]
Why this matters: [Connection to Worker Bee's learning]
What to study: [Specific sections/files/chapters]
Questions for next session: [What to think about]
Reading time: [Estimated time]
```

---

## Action Item Examples

### Example 1: Practical Task

**Task:** Debug a failing skill injection and document the fix

**Requirements:**
- Identify why skill-planner.md isn't being loaded
- Fix the issue in runner.py or ManifestLoader
- Write test that proves it now works
- Document what broke and why

**Evidence:** 
- Screenshot of test passing
- Git diff showing the fix
- 2-paragraph explanation of root cause

**Time estimate:** 45-60 minutes

### Example 2: Suggested Reading

**Resource:** [Skill Stack: Scalable LLM Skill Framework](https://arxiv.org/abs/2403.12345) (example)

**Author/Source:** Stanford NLP Group, 2024

**Why this matters:**
Research showing that skill-based prompting improves task success rates by 40% over monolithic prompts. Validates the architectural choice to separate skills from tools.

**What to study:**
- Section 3: Skill Composition Patterns
- Section 5: Failure Mode Analysis
- Figure 4: Skill Dependency Graph

**Questions for next session:**
- Do their failure modes match what you see in practice logs?
- Could their composition patterns improve how we chain skills?
- What did they miss that Worker Bee's architecture handles?

**Reading time:** 20-30 minutes (skim intro/conclusion, focus on sections 3 & 5)

---

## Suggested Reading Sources by Domain

### Domain 1: Conversation & Communication
- "The Mom Test" by Rob Fitzpatrick (asking good questions)
- Stripe's Writing Guidelines (clear technical communication)
- Paul Graham essays on clarity and simplicity

### Domain 2: Visual & Generative
- GitHub repos of image generation tools (Midjourney prompting guides)
- Simon Willison's blog on AI tool usage
- Papers on prompt engineering for visual models

### Domain 3: File & Document
- OCR best practices documentation
- Medical/legal document processing standards
- Regex tutorials and edge case catalogs

### Domain 4: Code & Repair
- **Garry Tan's gstack** (skill-based debugging)
- Julia Evans' debugging zines
- Google SRE book chapters on systematic troubleshooting
- Papers on automated code repair

### Domain 5: Decision & Integrity
- Research on AI hallucination detection
- Confidence calibration papers
- Anthropic's Constitutional AI papers

### Domain 6: Integration & Prompt Craft
- OpenAI/Anthropic prompt engineering guides
- LangChain documentation on tool composition
- Papers on multi-agent systems

---

## Why Action Items Matter

**Practical Task:**
- Proves understanding transferred to application
- Creates muscle memory (doing, not just knowing)
- Surfaces real-world edge cases
- Builds confidence through completion

**Suggested Reading:**
- Exposes Worker Bee to how others solve similar problems
- Validates (or challenges) current approaches
- Provides language and frameworks from the field
- Prevents insular thinking (learning only from Toby/Claude)

**Combined Effect:**
- Task = hands-on practice (iteration toward fluency)
- Reading = broadened perspective (avoid local maxima)
- Discussion next session = integration of both

This is how 10,000 iterations becomes 10,000 lessons instead of 10,000 repetitions.

---

## Template for Session Close

```markdown
## Action Items Before Next Session

### 1. Practical Task (Show Real Results)

**Task:** [Specific action]

**Requirements:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Evidence:** [What to show Claude next session]

**Time estimate:** [X minutes]

### 2. Suggested Reading

**Resource:** [Link]

**Author/Source:** [Who/why credible]

**Why this matters:** [Relevance to this session]

**What to study:**
- [Section/file 1]
- [Section/file 2]

**Questions for next session:**
- [Question 1]
- [Question 2]

**Reading time:** [X minutes]
```

---

## Session Files Structure

Every session produces 4 files:

```
manifests/practice/learning-sessions/YYYY-MM-DD-HHMM/
├── transcript.md           (full conversation)
├── bee-notes.md           (Worker Bee's understanding + action items)
├── claude-summary.md      (Claude's teaching + reasoning + action items)
└── gap-analysis.md        (where understanding diverged)
```

Plus optional:
```
├── scores.md              (teach-back scoring details)
└── evidence/              (screenshots, code from practical tasks)
    ├── task-1-result.png
    └── integration-test.py
```

---

## Quality Standards

**Good practical tasks:**
- Specific enough to know when done
- Challenging but achievable before next session
- Produces evidence that can be evaluated
- Directly related to session topic

**Good suggested reading:**
- From credible source (recognized expert, peer-reviewed, production-tested)
- Relevant to Worker Bee's domains
- Not too long (20-60 min reading time)
- Actionable insights, not just theory

**Bad action items:**
- "Think about X" (too vague, no evidence)
- "Read everything about Y" (too broad, overwhelming)
- "Maybe try Z if you want" (optional = won't happen)
- Resources that are 5+ years old (field moves fast)

---

## For Curriculum Manager

When generating session briefs, include:

1. Suggested practical task based on:
   - Current curriculum topic
   - Recent failures in practice logs
   - Skills that need testing

2. Suggested reading based on:
   - Domain being studied
   - Quality resources list (maintained separately)
   - What gaps the teach-back score revealed

Both should be auto-generated as part of session brief, not afterthoughts.
