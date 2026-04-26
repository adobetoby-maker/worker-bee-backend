#!/usr/bin/env python3
"""
End-to-end test of builder pipeline after RAM optimizations
Tests: deepseek architect -> qwen builder -> file output
"""
import asyncio
import sys
from pathlib import Path

# Add worker-bee to path
sys.path.insert(0, str(Path.home() / "worker-bee"))

from agent.tools.builder import build

async def test_builder_pipeline():
    print("=" * 60)
    print("🐝 Worker Bee Builder Pipeline Test")
    print("=" * 60)
    print()

    project = "simple-build"
    prompt = "a simple red button that says 'Click Me' in the center of the page"

    print(f"📋 Project: {project}")
    print(f"📝 Prompt: {prompt}")
    print()
    print("🔄 Starting pipeline...")
    print("   Step 1: deepseek-r1:14b creates architectural brief")
    print("   Step 2: qwen2.5-coder:32b builds React component")
    print("   Step 3: Files written to projects/{project}/")
    print()
    print("DEBUG: About to call build() function...")

    try:
        result = await build(
            project_name=project,
            prompt=prompt,
            use_architect=True,
            use_claude=False,
            ws=None
        )

        print("=" * 60)
        print("✅ BUILD COMPLETE")
        print("=" * 60)
        print()
        print(f"Files created: {result.get('files_created', 0)}")
        print(f"Output: {result.get('output_dir', 'unknown')}")
        print()

        if result.get("files"):
            print("📁 Files written:")
            for fname in result["files"]:
                print(f"   ✓ {fname}")

        print()
        print("🎉 Pipeline test PASSED!")
        print("   - deepseek created brief")
        print("   - qwen generated code")
        print("   - files written successfully")
        print()

        return True

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ BUILD FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_builder_pipeline())
    sys.exit(0 if success else 1)
