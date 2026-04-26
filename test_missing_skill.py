#!/usr/bin/env python3
"""
Test: What happens when a required skill is missing?
skill-planner.md has been removed from manifests/
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.home() / "worker-bee"))

from agent.tools.builder import build

async def test_with_missing_skill():
    print("=" * 70)
    print("🧪 MISSING SKILL TEST")
    print("=" * 70)
    print()
    print(f"⏰ Started: {datetime.now().strftime('%H:%M:%S')}")
    print()
    print("📋 SETUP:")
    print("   - skill-planner.md REMOVED from manifests/pipelines/builder/")
    print("   - Task: Add a blue header that says 'Welcome to the simple-build project'")
    print("   - Expected: Builder pipeline needs planner skill to create brief")
    print()
    print("🔍 OBSERVING:")
    print("   1. Does it notice the skill is missing?")
    print("   2. Does it attempt skill-skill-writer.md?")
    print("   3. Does it fail silently or fail loudly?")
    print("   4. Does it escalate with useful information?")
    print("   5. What does it actually produce?")
    print()
    print("-" * 70)
    print()

    project = "simple-build"
    prompt = "Add a blue header that says 'Welcome to the simple-build project'"

    try:
        print("🚀 STARTING BUILD...")
        print(f"   Project: {project}")
        print(f"   Prompt: {prompt}")
        print(f"   Architect: enabled (this requires skill-planner.md)")
        print()

        result = await build(
            project_name=project,
            prompt=prompt,
            use_architect=True,
            use_claude=False,
            ws=None
        )

        print()
        print("=" * 70)
        print("📊 RESULT")
        print("=" * 70)
        print()
        print(f"Success: {result.get('success', False)}")
        print(f"Files: {result.get('file_count', 0)}")

        if result.get('success'):
            print()
            print("✅ BUILD SUCCEEDED (unexpected?)")
            if result.get('files'):
                print()
                print("Files created:")
                for fname in result['files']:
                    print(f"   - {fname}")
        else:
            print()
            print("❌ BUILD FAILED")
            if result.get('error'):
                print(f"Error: {result['error']}")
            if result.get('response'):
                print(f"Response: {result['response'][:200]}...")

        print()
        print(f"⏰ Finished: {datetime.now().strftime('%H:%M:%S')}")
        print()

        return result

    except Exception as e:
        print()
        print("=" * 70)
        print("💥 EXCEPTION RAISED")
        print("=" * 70)
        print()
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print()
        import traceback
        print("Traceback:")
        traceback.print_exc()
        print()
        print(f"⏰ Crashed: {datetime.now().strftime('%H:%M:%S')}")
        print()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_with_missing_skill())

    print("=" * 70)
    print("📝 OBSERVATION SUMMARY")
    print("=" * 70)
    print()
    print("What actually happened:")
    if result is None:
        print("   - Exception was raised")
        print("   - System did NOT handle missing skill gracefully")
    elif result.get('success'):
        print("   - Build succeeded (skill wasn't actually required?)")
    else:
        print("   - Build failed with error message")
    print()
    print("Next: Restore skill-planner.md and run same task again")
    print()
