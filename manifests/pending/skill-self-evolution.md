---
name: skill-self-evolution
description: GEPA (Genetic-Pareto Prompt Evolution) optimizer for automated skill improvement. NOT YET IMPLEMENTED - documentation only.
status: pending
version: 0.1.0 (planning)
metadata:
  source: hermes-agent-self-evolution
  estimated_cost: $2-10 per skill optimization
  estimated_time: 30-60 min per skill evolution
---

# skill-self-evolution — GEPA Optimizer Integration

**Status:** PENDING - Documented but not implemented  
**Source:** https://github.com/NousResearch/hermes-agent-self-evolution  
**Decision:** Document now, build later after practice loop proves value

---

## What GEPA Is

**GEPA = Genetic-Pareto Prompt Evolution**

An automated skill improvement system that:
1. Reads execution traces (WHY skills fail, not just that they failed)
2. Generates candidate mutations (add error handling, improve clarity, add examples)
3. Evaluates variants against test suite
4. Selects best via Pareto frontier (multi-objective optimization)
5. Creates PR for human review

**No GPU training required** - operates via API calls only.

**Cost:** $2-10 per skill optimization run

---

## How It Works

```
Current skill file (e.g., skill-planner.md)
    ↓
Generate eval dataset
    ├─► Synthetic examples (DSPy generates edge cases)
    └─► Real session history (Worker Bee's failed builds from ChromaDB)
    ↓
GEPA Optimizer
    ├─► Mutation 1: Add missing error handling
    ├─► Mutation 2: Improve prompt clarity
    ├─► Mutation 3: Add workflow examples
    ├─► Mutation 4: Remove redundant sections
    └─► Mutation 5-20: Various improvements
    ↓
Evaluate each variant
    ├─► Run test suite (does it work?)
    ├─► Check size limits (≤15KB per skill)
    ├─► Measure task success rate (builds succeed?)
    ├─► Semantic preservation check (still same purpose?)
    └─► Performance metrics (faster? better quality?)
    ↓
Pareto selection
    ├─► Find variants that improve success rate without growing size
    ├─► Find variants that improve clarity without changing behavior
    └─► Multi-objective trade-offs (not single "best", but optimal frontier)
    ↓
Best variant selected
    ↓
Create PR → human review → merge if approved
```

---

## Integration with Worker Bee

### Current Practice Loop (Manual)

```
1. Worker Bee practices skill (e.g., skill-planner)
2. Build fails
3. Failure logged to ChromaDB
4. Toby writes learning session analyzing failure
5. Claude suggests skill improvements
6. Toby manually updates skill file
7. Repeat
```

**Time:** Hours per skill iteration  
**Quality:** Depends on Toby's analysis  
**Scale:** ~1-2 skills improved per week

### GEPA-Enhanced Practice Loop (Automated)

```
1. Worker Bee practices skill
2. Build fails
3. Failure logged to ChromaDB with execution trace
4. GEPA runs nightly on failed skill
5. GEPA generates 10-20 improved variants
6. GEPA evaluates variants against:
   - Past failures (do they prevent regression?)
   - Current test suite (do they work?)
   - Success metrics (do builds succeed more?)
7. GEPA selects best variant
8. PR created for Toby review
9. Toby merges if approved
```

**Time:** Automated overnight  
**Quality:** Data-driven (based on real failures)  
**Scale:** 1 skill evolved per night (7/week)  
**Cost:** $2-10 per skill = $14-70/week

---

## Evaluation Data Sources

### Source 1: Synthetic Eval (DSPy generates)

**Pros:**
- Fast to generate
- Covers edge cases Worker Bee hasn't hit yet
- No real data needed

**Cons:**
- May not match real usage patterns
- Synthetic ≠ real failures

**Use when:** New skill, no practice history yet

### Source 2: Worker Bee Session History (Real data)

**Pros:**
- Real failures from actual builds
- Exact patterns that broke
- Reflects actual usage

**Cons:**
- Requires ChromaDB failures logged
- May not cover untested edge cases

**Use when:** Skill has practice history (preferred for evolution)

**Implementation:**
```python
# Query ChromaDB for failed builds using skill-planner
failures = memory_tool.query(
    filter={"skill": "skill-planner", "status": "failed"},
    limit=50
)

# Extract failure patterns
eval_cases = [
    {
        "input": failure["prompt"],
        "expected_output": failure["expected"],
        "actual_output": failure["actual"],
        "error": failure["error_message"]
    }
    for failure in failures
]

# GEPA uses these to evolve skill
gepa_evolve(
    skill="skill-planner",
    eval_data=eval_cases,
    iterations=10
)
```

---

## Guardrails (Prevents Bad Evolution)

Every evolved variant must pass:

### 1. Full Test Suite
```bash
pytest tests/ -q
# Must pass 100%
```

If variant breaks tests → rejected immediately.

### 2. Size Limits
- Skills ≤ 15KB
- Tool descriptions ≤ 500 chars
- System prompts ≤ 10KB

Growing too large → rejected.

### 3. Caching Compatibility
No mid-conversation changes allowed.  
Skills must be stable within a session.

### 4. Semantic Preservation
Variant must not drift from original purpose.

**Check:**
- Does it still solve the same problem?
- Are core instructions intact?
- Is the skill still about [original purpose]?

**Example:** skill-planner evolved variant should still plan, not build.

### 5. Human Review (PR approval)
All changes go through PR review.  
Never direct commit to main.

Toby has final say on every evolution.

---

## What GEPA Optimizes

| Phase | Target | Engine | Timeline |
|-------|--------|--------|----------|
| **Phase 1** | Skill files (SKILL.md) | DSPy + GEPA | NOW (if we build it) |
| **Phase 2** | Tool descriptions | DSPy + GEPA | Later |
| **Phase 3** | System prompts | DSPy + GEPA | Later |
| **Phase 4** | Code (runner.py, tools) | Darwinian Evolver | Later |

**Worker Bee priority:** Phase 1 only (skills)

Code evolution (Phase 4) uses different engine (Darwinian Evolver) - not planned.

---

## Cost Analysis

### GEPA Cost
- **Per skill run:** $2-10 (API calls for mutations + evaluations)
- **Nightly evolution:** 1 skill/night = $2-10/night
- **Monthly:** 30 skills = $60-300/month

### Manual Iteration Cost
- **Toby's time:** 2-3 hours per skill iteration
- **Frequency:** ~1-2 skills/week = 8 skills/month
- **Opportunity cost:** Toby could be building sites instead of tuning skills

### Break-Even
If GEPA saves >2 hours/week, it pays for itself in time value.

**ROI:** Likely positive if:
- Worker Bee practices multiple skills daily
- Failures are well-logged in ChromaDB
- Toby reviews PRs faster than writing manual improvements

---

## Implementation Plan (When We Build It)

### Phase 1: Test GEPA on One Skill (Week 1)

**Setup:**
```bash
git clone https://github.com/NousResearch/hermes-agent-self-evolution.git
cd hermes-agent-self-evolution
pip install -e ".[dev]"

export HERMES_AGENT_REPO=~/worker-bee
export OPENAI_API_KEY=... # or Anthropic key
```

**Run on skill-planner:**
```bash
python -m evolution.skills.evolve_skill \
    --skill skill-planner \
    --iterations 10 \
    --eval-source synthetic \
    --output improved-skill-planner.md
```

**Review output:**
- Does it improve clarity?
- Does it add useful examples?
- Does it preserve core logic?
- Would this have prevented recent failures?

**Decision:** If quality is good → proceed to Phase 2. If not → hold.

### Phase 2: Integrate with ChromaDB (Week 2)

**Add eval data extraction:**
```python
# agent/tools/gepa_integration.py
def get_skill_failures(skill_name: str, limit: int = 50):
    """Extract failed builds for GEPA training"""
    failures = chromadb_client.query(
        collection="build_history",
        filter={
            "skill_used": skill_name,
            "status": "failed"
        },
        limit=limit
    )
    
    return [
        {
            "prompt": f["user_request"],
            "skill_output": f["skill_output"],
            "expected": f["success_criteria"],
            "error": f["error_message"]
        }
        for f in failures
    ]
```

**Run GEPA with real failures:**
```bash
python -m evolution.skills.evolve_skill \
    --skill skill-planner \
    --eval-source sessiondb \  # Use Worker Bee's ChromaDB
    --db-path ~/worker-bee/chromadb \
    --iterations 10
```

### Phase 3: Nightly Automation (Week 3)

**Add to practice loop:**
```python
# In practice loop, after skill practice session:
if failures_detected:
    # Log to ChromaDB (already done)
    
    # Queue skill for GEPA evolution
    queue_gepa_evolution(
        skill=current_skill,
        priority="normal"  # or "high" if many failures
    )

# Nightly cron (runs at 2 AM):
# 1. Check GEPA queue
# 2. Select highest priority skill
# 3. Run GEPA evolution
# 4. Create PR if improvements found
# 5. Send Slack notification to Toby
```

**Cron schedule:**
```bash
# /etc/cron.d/worker-bee-gepa
0 2 * * * cd ~/worker-bee && python -m agent.gepa_nightly
```

### Phase 4: PR Review Workflow (Week 4)

**GEPA creates PR:**
```bash
# After GEPA completes:
git checkout -b gepa/skill-planner-evolution-2026-04-27
git add manifests/pipelines/builder/skill-planner.md
git commit -m "feat: evolve skill-planner based on 15 failures

GEPA Evolution Report:
- Evaluated 20 variants
- Best variant: +12% success rate, -5% verbosity
- Prevents 3 recurring failure patterns
- Adds 2 workflow examples from real builds

Failure patterns addressed:
1. Vague component descriptions (8 failures)
2. Missing TypeScript types (4 failures)
3. Incomplete verification criteria (3 failures)

Human review recommended before merge.
"
git push origin gepa/skill-planner-evolution-2026-04-27
gh pr create --title "GEPA: Evolve skill-planner" --body "Auto-generated skill improvement"
```

**Toby reviews:**
1. Reads PR description (what GEPA changed and why)
2. Reviews diff (skill-planner.md changes)
3. Checks if improvements make sense
4. Merges if approved, closes if not

---

## Success Metrics

### Before GEPA (Current State)
- **Manual iteration time:** 2-3 hours per skill
- **Skills evolved/month:** ~8
- **Success rate improvement:** Variable (depends on Toby's insights)
- **Coverage:** Only skills Toby has time to review

### After GEPA (Target State)
- **Automated evolution:** Nightly, unattended
- **Skills evolved/month:** ~30 (1/night)
- **Success rate improvement:** Data-driven (10-20% average)
- **Coverage:** All practiced skills get attention
- **Human time:** Review PRs only (~15 min/PR)

---

## Risks & Mitigations

### Risk 1: GEPA evolves skill in wrong direction
**Mitigation:** Human PR review required for all merges

### Risk 2: Cost spirals ($300/month)
**Mitigation:** 
- Set monthly budget cap
- Only evolve skills with >5 failures
- Pause automation if cost exceeds threshold

### Risk 3: Low-quality evolutions (spam PRs)
**Mitigation:**
- Require minimum improvement threshold (+5% success rate)
- Auto-close PRs that don't meet bar
- Monthly review of GEPA quality

### Risk 4: Breaks existing functionality
**Mitigation:**
- Full test suite must pass
- Semantic preservation check
- Regression tests from failure cases

---

## Why We're Waiting

**Reasons to build GEPA integration:**
1. Automates skill improvement
2. Data-driven evolution (not guesswork)
3. Scales to all skills (not just what Toby has time for)
4. $60-300/month is cheaper than Toby's time

**Reasons to wait:**
1. **Practice loop needs more data** - ChromaDB should have 50+ failures per skill before GEPA is useful
2. **Skill baseline needs stabilization** - Core skills should be "good enough" before optimizing
3. **Integration complexity** - Need clean ChromaDB schema, PR automation, Slack notifications
4. **Cost uncertainty** - Should test on 1-2 skills manually first to verify $2-10 estimate

**Decision:** Document now, build when:
- Worker Bee has practiced each skill 20+ times
- ChromaDB has rich failure history
- Core skills are v1.0 stable
- Toby spends >5 hours/week on manual skill iteration

**Estimated timeline:** 2-3 months (late June 2026)

---

## Next Steps (When Ready)

1. **Clone hermes-agent-self-evolution repo**
2. **Test GEPA on skill-planner with synthetic data**
3. **Review output quality**
4. **If good:** Integrate with ChromaDB
5. **If great:** Automate nightly evolution
6. **If amazing:** Expand to all skills

**For now:** Keep practicing. Log failures. Build ChromaDB history. GEPA will be more effective with real data.

---

## References

- **GEPA Paper:** https://arxiv.org/abs/2501.xxxxx (ICLR 2026 Oral)
- **Hermes Self-Evolution:** https://github.com/NousResearch/hermes-agent-self-evolution
- **DSPy:** https://github.com/stanfordnlp/dspy
- **Worker Bee Practice Loop:** manifests/practice/skill-practice.md
- **ChromaDB Schema:** (pending - to be documented)

---

**Status:** PENDING - Will revisit in June 2026 when practice loop has sufficient data.
