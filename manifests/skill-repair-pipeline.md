# Skill: Systematic Debugging & Root Cause Investigation

**Purpose:** Fix bugs systematically without guessing. Find root causes before attempting fixes.

**When to use:** Any bug, test failure, unexpected behavior, or technical issue.

---

## The Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**  
**NO INVESTIGATION WITHOUT CONTEXT RECALL FIRST**

If you haven't completed Phase 0, you cannot proceed to Phase 1.  
If you haven't completed Phase 1, you cannot propose fixes.

---

## The Five Phases

You MUST complete each phase before proceeding to the next.

### Phase 0: Context Recall (MANDATORY FIRST STEP)

**BEFORE doing ANYTHING else:**

1. **Extract Keywords from Error**
   - What's the error type? (OOM, timeout, connection, type error...)
   - What component? (server, browser, API, database...)
   - What area of the codebase?

2. **Search for Prior Knowledge**
   - Check SESSIONS.md, JOURNAL.md, PRACTICE.md
   - Search codebase for similar error patterns: `grep -r "ErrorType" .`
   - Check git log for related recent changes: `git log --oneline -20`
   - Check manifests/practice/ for similar issues

3. **Review Results**
   - Found relevant experience? → **Apply directly, skip to Phase 4**
   - Found partial match? → Use as starting point for Phase 1
   - Nothing found? → Proceed to Phase 1, **remember to record solution later**

4. **Output Format**
   ```
   Context Recall:
   - Query: "xxx"
   - Found: [description of related knowledge]
   - Action: [apply experience / continue investigation / no match]
   ```

**VIOLATION:** Proceeding to Phase 1 without Context Recall output = process failure.

---

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits: `git log --oneline -20 -- <file>`
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components:**
   
   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

5. **Trace Data Flow**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

**Output:** State clearly: "Root cause hypothesis: [specific, testable claim about what is wrong and why]"

---

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY
   - Don't skim - read every line
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions does it make?

**Check known patterns:**
- **Race condition**: Intermittent, timing-dependent. Check concurrent access to shared state.
- **Nil/null propagation**: NoMethodError, TypeError. Missing guards on optional values.
- **State corruption**: Inconsistent data, partial updates. Check transactions, callbacks, hooks.
- **Integration failure**: Timeout, unexpected response. External API calls, service boundaries.
- **Configuration drift**: Works locally, fails in staging/prod. Env vars, feature flags, DB state.
- **Stale cache**: Shows old data, fixes on cache clear. Redis, CDN, browser cache.

---

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once
   - Add temporary log statement or assertion at suspected root cause

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **3-Strike Rule**
   - If 3 hypotheses fail, **STOP**
   - Tell Toby: "3 hypotheses tested, none match. This may be an architectural issue rather than a simple bug."
   - Options:
     - Continue investigating with a new hypothesis (describe it)
     - Escalate for human review
     - Add logging and wait (instrument the area and catch it next time)

5. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help
   - Research more

---

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - Automated test if possible
   - One-off test script if no framework
   - MUST have before fixing

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?
   - Can you reproduce the original bug? (It should be gone)

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If >= 3: STOP and question the architecture**
   - DON'T attempt Fix #4 without architectural discussion

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we refactor architecture vs. continue fixing symptoms?

   **Discuss with Toby before attempting more fixes.**

6. **Document the Fix**
   - Write what broke and why to PRACTICE.md
   - Add to session notes if during active development
   - Create regression test that prevents this bug from recurring

---

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5)

---

## Common Rationalizations (Don't Fall for These)

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms != understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

---

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **0. Context Recall** | Extract keywords, search prior knowledge | Output recall summary |
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally, 3-strike rule | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify, document | Bug resolved, tests pass |

---

## Language-Specific Debugging Commands

### JavaScript / TypeScript / Node.js
```bash
# Node.js debugger
node --inspect-brk app.js
# Chrome DevTools: chrome://inspect

# Console debugging
console.log(JSON.stringify(obj, null, 2))
console.trace('Call stack here')
console.time('perf'); /* code */ console.timeEnd('perf')

# Memory leaks
node --expose-gc --max-old-space-size=4096 app.js
```

### Python
```bash
# Built-in debugger
python -m pdb script.py

# Breakpoint in code
breakpoint()  # Python 3.7+

# Verbose tracing
python -X tracemalloc script.py

# Profile
python -m cProfile -s cumulative script.py
```

### Git Bisect (Find the commit that introduced a bug)
```bash
git bisect start
git bisect bad              # Current commit is broken
git bisect good abc1234     # Known good commit
# Git checks out middle commit — test it, then:
git bisect good  # or  git bisect bad
# Repeat until root cause commit is found
git bisect reset
```

### Network Debugging
```bash
# HTTP debugging
curl -v https://api.example.com/endpoint

# DNS
dig example.com
nslookup example.com

# Ports
lsof -i :3000
netstat -tlnp

# What's using this port?
lsof -i :PORT

# What's this process doing?
ps aux | grep PROCESS
```

---

## Common Error Patterns

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `Cannot read property of undefined` | Missing null check or wrong data shape | Add optional chaining (`?.`) or validate data |
| `ENOENT` | File/directory doesn't exist | Check path, create directory, use `existsSync` |
| `CORS error` | Backend missing CORS headers | Add CORS middleware with correct origins |
| `Module not found` | Missing dependency or wrong import path | `npm install`, check paths |
| `Connection refused` | Service not running on expected port | Check if service is up, verify port/host |
| `Permission denied` | File/network permission issue | Check chmod, firewall, sudo |
| `Segmentation fault` | Memory corruption, null pointer | Check array bounds, pointer validity |

---

## Real-World Impact

From debugging sessions:
- Systematic approach: **15-30 minutes to fix**
- Random fixes approach: **2-3 hours of thrashing**
- First-time fix rate: **95% vs 40%**
- New bugs introduced: **Near zero vs common**

---

**Remember:** Debugging is detective work, not guesswork. Follow the evidence, not your hunches.
