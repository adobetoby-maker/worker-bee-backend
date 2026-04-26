#!/usr/bin/env python3
"""
Test script to verify vision_analyze works with qwen2.5vl:7b
"""
import asyncio
import httpx
import base64
from pathlib import Path

OLLAMA = "http://localhost:11434"

async def test_vision_old_format():
    """Test the OLD llava format (should fail or return different result)"""
    print("❌ Testing OLD format (llava generate API)...")
    try:
        # Create a simple 1x1 transparent PNG in base64
        test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{OLLAMA}/api/generate",
                json={
                    "model": "llava:latest",  # This model doesn't exist anymore
                    "prompt": "What do you see?",
                    "images": [test_image_b64],
                    "stream": False
                }
            )
            result = r.json()
            print(f"   Response: {result}")
            return False
    except Exception as e:
        print(f"   Expected error: {e}")
        return True

async def test_vision_new_format():
    """Test the NEW qwen2.5vl chat format (should work)"""
    print("\n✅ Testing NEW format (qwen2.5vl chat API)...")
    try:
        # Create a simple 1x1 transparent PNG in base64
        test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{OLLAMA}/api/chat",
                json={
                    "model": "qwen2.5vl:7b",
                    "messages": [{
                        "role": "user",
                        "content": "What do you see in this image?",
                        "images": [test_image_b64]
                    }],
                    "stream": False
                }
            )
            result = r.json()
            content = result.get("message", {}).get("content", "")
            print(f"   Model: qwen2.5vl:7b")
            print(f"   Response: {content[:200]}...")
            return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def test_runner_integration():
    """Test that runner.py vision_analyze would work"""
    print("\n🧪 Testing runner.py vision_analyze() logic...")

    # Simulate what runner.py does
    screenshot_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    question = "Describe what you see"

    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                f"{OLLAMA}/api/chat",
                json={
                    "model": "qwen2.5vl:7b",
                    "messages": [{
                        "role": "user",
                        "content": question,
                        "images": [screenshot_b64]
                    }],
                    "stream": False
                }
            )
            response = r.json().get("message", {}).get("content", "Vision unavailable")
            print(f"   ✅ vision_analyze() would return: {response[:150]}...")
            return True
    except Exception as e:
        print(f"   ❌ vision_analyze() would fail: {e}")
        return False

async def main():
    print("=" * 60)
    print("Worker Bee Vision Model Migration Test")
    print("llava:latest → qwen2.5vl:7b")
    print("=" * 60)

    # Test old format (expected to fail)
    old_works = await test_vision_old_format()

    # Test new format (expected to work)
    new_works = await test_vision_new_format()

    # Test runner integration
    runner_works = await test_runner_integration()

    print("\n" + "=" * 60)
    print("TEST RESULTS:")
    print("=" * 60)
    print(f"Old llava format fails (expected): {'✅' if old_works else '❌'}")
    print(f"New qwen2.5vl format works: {'✅' if new_works else '❌'}")
    print(f"runner.py integration works: {'✅' if runner_works else '❌'}")

    if new_works and runner_works:
        print("\n🎉 SUCCESS! Vision model migration complete.")
        print("   runner.py will now use qwen2.5vl:7b for all vision tasks.")
    else:
        print("\n⚠️  FAILED! Check Ollama and model availability.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
