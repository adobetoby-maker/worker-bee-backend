"""
Live Learning Session - Claude teaches Worker Bee

Real-time conversation between Claude (me) and Worker Bee (local models).
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime
from pathlib import Path


async def learning_session():
    """Conduct live learning session with Worker Bee"""

    session_id = datetime.now().strftime("%Y-%m-%d-%H%M")
    print(f"\n🎓 Live Learning Session: {session_id}")
    print("=" * 70)
    print("Claude (Sonnet 4.5) teaching Worker Bee (local models)")
    print("=" * 70)

    transcript = []

    # Connect to Worker Bee
    uri = "ws://localhost:8001/ws/learning-session-1"

    try:
        async with websockets.connect(uri) as websocket:
            print("\n✅ Connected to Worker Bee\n")

            # Send opening brief with learning context marker
            opening_brief = """═══════════════════════════════════════════════════════════════════
⚠️  LEARNING SESSION CONTEXT ⚠️

This is a LEARNING SESSION.
You are the STUDENT. Claude is the TEACHER.

DO NOT execute tasks. DO NOT build things. DO NOT fire pipelines.
DO ask questions. DO explore concepts. DO show your reasoning.
DO admit uncertainty. DO teach back what you learn.

This is not worker mode. This is student mode.
═══════════════════════════════════════════════════════════════════

I am Worker Bee — an autonomous AI agent built by Toby Anderton. This is my first learning session with Claude Sonnet.

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

            print("🐝 WORKER BEE:")
            print(opening_brief)
            print("\n" + "-" * 70 + "\n")

            # Send to Worker Bee
            await websocket.send(json.dumps({
                "action": "chat",
                "content": opening_brief
            }))

            transcript.append({
                "role": "worker_bee",
                "content": opening_brief,
                "timestamp": datetime.now().isoformat()
            })

            # Receive Worker Bee's response
            response_parts = []
            print("🤖 WORKER BEE (phi4) responding...\n")

            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                    data = json.loads(message)

                    if data.get("type") == "token":
                        token = data.get("data")
                        print(token, end="", flush=True)
                        response_parts.append(token)

                    elif data.get("type") == "done":
                        full_response = "".join(response_parts)
                        transcript.append({
                            "role": "phi4",
                            "content": full_response,
                            "timestamp": datetime.now().isoformat()
                        })
                        print("\n\n" + "-" * 70 + "\n")
                        break

                    elif data.get("type") == "error":
                        print(f"\n❌ Error: {data.get('data')}\n")
                        break

                except asyncio.TimeoutError:
                    print("\n⏱️  Timeout waiting for response\n")
                    break

            # Now I (Claude) respond with teaching
            print("📖 CLAUDE (teaching):\n")

            claude_response = """Worker Bee, you've identified the right problem. Let me show you how I think about this architecture.

What you understand is correct:
- Skills inject through AgentRunner ✓
- Direct imports bypass the system ✓
- Testing the tool ≠ testing the skill ✓

Here's the WHY behind this architecture:

The separation exists because tools are capabilities, skills are judgment.

Think of it like surgery:
- Tool = scalpel (the capability to cut)
- Skill = knowing where to cut, how deep, when to stop

If you test the scalpel works (tool test), you haven't tested whether the surgeon knows where to cut (skill test).

The cost-benefit analysis that drove this design:

Toby could have built you with skills embedded in tool code, but that means every behavioral refinement requires code changes. Every time you learn "ask clarifying questions first," he'd edit tool code.

What Toby chose instead: skills are separate markdown files that inject through ManifestLoader. Now behavioral learning (refining skills) doesn't touch code. Skills can evolve through 10,000 iterations without a single code change.

What would break if it worked differently? If skills and tools were mixed:
1. Every skill refinement = code deployment
2. Code tests would need to test both capability AND behavior
3. Can't A/B test different behavioral approaches
4. Can't have different skills for same tool

The real insight: Your test passed because you tested capability without context. The tool works. But your job isn't "can you build" — it's "do you know WHEN to build, HOW to approach it, WHAT to ask first."

That's why ManifestLoader exists as a separate injection point. It's the moment where capability meets judgment.

Now test my understanding: Ask me a follow-up question that probes whether I actually explained this correctly."""

            print(claude_response)
            print("\n" + "-" * 70 + "\n")

            transcript.append({
                "role": "claude",
                "content": claude_response,
                "timestamp": datetime.now().isoformat()
            })

            # Send Claude's teaching to Worker Bee
            await websocket.send(json.dumps({
                "action": "chat",
                "content": claude_response
            }))

            # Get Worker Bee's follow-up
            response_parts = []
            print("🐝 WORKER BEE (follow-up):\n")

            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                    data = json.loads(message)

                    if data.get("type") == "token":
                        token = data.get("data")
                        print(token, end="", flush=True)
                        response_parts.append(token)

                    elif data.get("type") == "done":
                        full_response = "".join(response_parts)
                        transcript.append({
                            "role": "worker_bee",
                            "content": full_response,
                            "timestamp": datetime.now().isoformat()
                        })
                        print("\n\n" + "=" * 70)
                        print("Session transcript saved")
                        print("=" * 70 + "\n")
                        break

                except asyncio.TimeoutError:
                    print("\n⏱️  Timeout\n")
                    break

            # Save transcript
            output_dir = Path.home() / f"worker-bee/manifests/practice/learning-sessions/{session_id}"
            output_dir.mkdir(parents=True, exist_ok=True)

            transcript_file = output_dir / "transcript.md"
            with open(transcript_file, 'w') as f:
                f.write(f"# Learning Session Transcript - {session_id}\n\n")
                f.write("Claude Sonnet 4.5 teaching Worker Bee (phi4/deepseek/qwen)\n\n")
                f.write("=" * 70 + "\n\n")

                for msg in transcript:
                    role_label = {
                        "worker_bee": "🐝 WORKER BEE",
                        "phi4": "🤖 PHI4",
                        "claude": "📖 CLAUDE"
                    }.get(msg["role"], msg["role"])

                    f.write(f"## {role_label} — {msg['timestamp']}\n\n")
                    f.write(f"{msg['content']}\n\n")
                    f.write("-" * 70 + "\n\n")

            print(f"📄 Transcript saved: {transcript_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(learning_session())
