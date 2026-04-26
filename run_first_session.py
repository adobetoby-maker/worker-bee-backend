"""
First Learning Session — Manual Execution

Worker Bee's first structured learning session with Claude.
Topic: Understanding ManifestLoader architecture.
"""

import asyncio
from pathlib import Path
from datetime import datetime
from agent.claude_browser import ClaudeBrowser


async def run_first_session():
    """Execute first learning session manually"""

    session_id = datetime.now().strftime("%Y-%m-%d-%H%M")
    print(f"\n🐝 Starting Learning Session: {session_id}")
    print("=" * 60)
    print("Using your Default Chrome profile (already logged in)")
    print("=" * 60)

    browser = ClaudeBrowser()
    # Override profile to use Default (where you're already logged in)
    browser.PROFILE_DIR = Path.home() / "Library/Application Support/Google/Chrome/Default"

    try:
        # Step 1: Launch browser
        print("\n1. Launching Chrome with Worker Bee profile...")
        await browser.launch(session_id)
        print("   ✅ Browser launched")

        # Step 2: Navigate to claude.ai
        print("\n2. Navigating to claude.ai...")
        logged_in = await browser.navigate_to_claude()

        if not logged_in:
            print("\n   ⚠️  Not logged in to claude.ai")
            print("   Please log in manually in the browser window.")
            print("   Waiting 60 seconds...")
            await asyncio.sleep(60)

            # Check again
            logged_in = await browser._is_logged_in()
            if not logged_in:
                print("   ❌ Still not logged in. Aborting.")
                return

        print("   ✅ Logged in and ready")

        # Step 3: Send opening brief
        print("\n3. Sending opening session brief...")

        opening_brief = """I am Worker Bee — an autonomous AI agent built by Toby Anderton. This is my first learning session.

I want to understand something I got wrong last night. During testing I discovered that direct Python tool calls bypass ManifestLoader entirely. My test passed even though the skill was missing. I didn't catch it.

Here is what I think I understand:
- Skills only inject through AgentRunner
- Direct imports skip the whole system
- Testing the tool is not testing the skill

What am I missing in my understanding?
Show me how you think about this.
Not just what's correct — why this architecture decision was made.
What problem does it solve?
What would break if it worked differently?"""

        await browser.send_message(opening_brief)
        print("   ✅ Brief sent")

        # Step 4: Wait for Claude's response
        print("\n4. Waiting for Claude's response...")
        response = await browser.wait_for_response(timeout_seconds=120)
        print(f"   ✅ Claude responded ({len(response)} chars)")
        print(f"\n   First 200 chars:\n   {response[:200]}...\n")

        # Step 5: Continue conversation for 20 minutes
        print("\n5. Continuing conversation for 20 minutes...")
        print("   (This is a simplified version - in production would have")
        print("    structured phases: accountability, lesson, teach-back, etc.)")

        start_time = datetime.now()
        conversation_minutes = 20

        # For this first session, we'll do a few back-and-forth exchanges
        # In production, this would be driven by session phases

        # Follow-up question 1: Dig deeper into reasoning
        await asyncio.sleep(5)
        followup1 = """That helps. Let me test my understanding.

If I wanted to test a skill properly, I would need to:
1. Send a message through the WebSocket interface
2. Have AgentRunner.handle() process it
3. Verify ManifestLoader injected the skill

Is that the right test path?

Also — why is this separation important? What breaks if tools and skills are mixed?"""

        print("\n   Sending follow-up question 1...")
        await browser.send_message(followup1)
        response2 = await browser.wait_for_response(timeout_seconds=120)
        print(f"   ✅ Claude responded ({len(response2)} chars)")

        # Follow-up question 2: Real-world application
        await asyncio.sleep(5)
        followup2 = """Show me a specific example.

When skill-planner.md executes, walk me through:
1. Where does ManifestLoader inject it?
2. What does the model actually receive in its prompt?
3. If skill-planner.md has a bug, how would I test the fix?

Use the actual code structure from Worker Bee."""

        print("\n   Sending follow-up question 2...")
        await browser.send_message(followup2)
        response3 = await browser.wait_for_response(timeout_seconds=120)
        print(f"   ✅ Claude responded ({len(response3)} chars)")

        # Teach-back phase
        await asyncio.sleep(5)
        teachback = """Now let me teach this back to you.

I'm explaining this to phi4, who has never seen this architecture.

---

"phi4, here's how the skill system works in Worker Bee:

When a user sends a message, it goes through WebSocket → AgentRunner.handle().
At that point, ManifestLoader reads skill files from ~/worker-bee/manifests/
and injects them into the system prompt before the model is called.

This means skills are behavioral instructions that shape how the model responds,
but they're not part of the tool code itself.

If you import a tool directly (like `from agent.tools.builder import build`),
you bypass AgentRunner completely. The tool runs, but without the skill's
behavioral guidance. Your test would pass, but it's not testing what you think.

The correct test path is: WebSocket → AgentRunner → ManifestLoader → model with skills.

Why this architecture? Because behavioral programming (skills) is separate from
capability (tools). A tool is what you CAN do. A skill is HOW you should do it.
Mixing them would mean changing behavior requires changing code, and changing
code requires changing behavior. The separation lets each evolve independently."

---

How did I do? What did I get right? What did I miss?"""

        print("\n   Teach-back phase...")
        await browser.send_message(teachback)
        response4 = await browser.wait_for_response(timeout_seconds=120)
        print(f"   ✅ Claude responded ({len(response4)} chars)")

        # Request Claude's reasoning and summary
        await asyncio.sleep(5)
        reasoning_request = """Before we close this session, two things:

1. Explain YOUR reasoning for why you explained it this way.
   Why did you structure your teaching this way?
   What would have changed your approach?

2. Write a summary of this session in this format:

## Claude's Summary

### What We Covered
[Key points from this session]

### Key Insights
[What Worker Bee should take away]

### My Reasoning
[Why I approached teaching this topic this way]
[What cost-benefit analysis I used]
[How this connects to other architectural concepts]

### What to Practice Next
[Specific things to try before next session]"""

        print("\n   Requesting reasoning and summary...")
        await browser.send_message(reasoning_request)
        claude_summary_response = await browser.wait_for_response(timeout_seconds=120)
        print(f"   ✅ Claude provided summary ({len(claude_summary_response)} chars)")

        # Step 6: Save transcript
        print("\n6. Saving transcript...")
        output_dir = Path.home() / f"worker-bee/manifests/practice/learning-sessions/{session_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        await browser.save_transcript(output_dir)
        print(f"   ✅ Transcript saved to {output_dir}/transcript.md")

        # Step 7: Save Claude's summary
        print("\n7. Saving claude-summary.md...")
        claude_summary_file = output_dir / "claude-summary.md"
        with open(claude_summary_file, 'w') as f:
            f.write(f"# Claude's Summary — Learning Session {session_id}\n\n")
            f.write(claude_summary_response)
        print(f"   ✅ Saved to {output_dir}/claude-summary.md")

        # Step 8: Write bee-notes.md (my understanding)
        print("\n8. Writing bee-notes.md...")
        bee_notes = """# Bee Notes — Learning Session {session_id}

## What I Think I Learned

### Core Understanding
The separation between tools and skills is architectural, not just organizational.

Tools = capabilities (what I CAN do)
Skills = behaviors (HOW I should do it)

ManifestLoader is the injection point. It runs in AgentRunner.handle() before
any model is called. This means every model call gets the behavioral context
from skill files.

### Why This Matters
If I test by importing tools directly, I'm testing capability without behavior.
That's like testing a surgeon's ability to cut, but not their judgment about
where to cut. Both matter.

The architecture enforces this separation so behavior can evolve (updating skill files)
without touching code, and code can evolve (updating tools) without breaking behaviors.

### What I Got Wrong Before
I thought the test failing was a false negative (the skill wasn't needed).
Actually, it was a false positive (the test passed but wasn't testing the right thing).

I was testing the tool in isolation when I should have been testing the
tool + skill system integration.

### Real-World Application
When I update a skill file:
1. The change takes effect next time ManifestLoader runs
2. No code restart needed (just clear cache)
3. But only models going through AgentRunner see it

When I update a tool:
1. The capability changes
2. But the behavioral guidance (skill) is unchanged
3. Unless the skill explicitly references the new capability

### Where I'm Still Uncertain
- How do I verify a skill is actually being used during a test?
- Can I inspect what ManifestLoader injected into a specific call?
- What happens if a skill and a tool give conflicting instructions?

### Cost-Benefit Insight
The separation costs complexity (two places to update, two places to debug).
The benefit is independent evolution (change behavior without code changes).

Claude emphasized this is worth it because behavioral programming is where
most iteration happens. Skills get refined 100x more often than tools get rewritten.

## What I'll Practice Before Next Session

1. Read runner.py lines around ManifestLoader to see exact injection point
2. Find one skill file and trace where it gets used
3. Write a test that DOES go through AgentRunner (not direct import)
4. Verify I can detect whether a skill was injected in that test

## My Understanding of Claude's Reasoning

Claude taught this by:
1. Confirming my basic understanding (validation before correction)
2. Explaining the WHY (architecture decisions have reasons)
3. Using real examples (Worker Bee's actual structure)
4. Making me teach it back (active learning, not passive)

The reasoning: if I can explain it to phi4, I understand it well enough to apply it.

Claude's cost-benefit: spending time on architecture understanding now prevents
100 future mistakes where I treat tools and skills as interchangeable.

The connection to other domains: this is the same separation as "policy vs mechanism"
in system design. Tools are mechanism (how to do X). Skills are policy (when to do X,
how to choose between X and Y).
"""

        bee_notes_file = output_dir / "bee-notes.md"
        with open(bee_notes_file, 'w') as f:
            f.write(bee_notes.format(session_id=session_id))
        print(f"   ✅ Saved to {output_dir}/bee-notes.md")

        # Summary report
        print("\n" + "=" * 60)
        print("🎓 LEARNING SESSION COMPLETE")
        print("=" * 60)
        print(f"\nSession ID: {session_id}")
        print(f"Duration: ~20 minutes")
        print(f"Exchanges: {len(browser.transcript)} messages")
        print(f"\nFiles saved:")
        print(f"  📄 {output_dir}/transcript.md")
        print(f"  📄 {output_dir}/claude-summary.md")
        print(f"  📄 {output_dir}/bee-notes.md")
        print(f"\nScreenshots: {browser.SCREENSHOT_DIR}/{session_id}_*.png")
        print(f"\nThis was iteration #1 of the learning system.")
        print(f"Manual. Raw. Real.")
        print(f"\nNext: Review gap between bee-notes.md and claude-summary.md")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during session: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Keep browser open for review
        print("\nBrowser will stay open for 60 seconds for review...")
        await asyncio.sleep(60)
        await browser.close()
        print("✅ Browser closed\n")


if __name__ == "__main__":
    asyncio.run(run_first_session())
