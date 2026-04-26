"""
Continuous Practice Loop - 24/7 Skill Practice System

Runs whenever Worker Bee is idle (no active WebSocket connections).
Practices skills in round-robin rotation every 5 minutes.
Logs all practice sessions to skill-X.practice.md files.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List
import httpx


class ContinuousPracticeLoop:
    """
    24/7 autonomous skill practice system.
    Runs when idle, yields to user sessions.
    """

    def __init__(self):
        self.base_dir = Path.home() / "worker-bee"
        self.practice_dir = self.base_dir / "manifests/practice"
        self.state_file = self.practice_dir / "practice-state.json"

        # Ensure directories exist
        self.practice_dir.mkdir(parents=True, exist_ok=True)

        # 9 autonomous-compatible skills in round-robin rotation
        self.skills = [
            "skill-seo",
            "skill-repair-pipeline",
            "skill-web-architect",
            "skill-image-gen",
            "skill-navigator",
            "skill-planner",
            "skill-builder",
            "skill-reviewer",
            "skill-checker"
        ]

        # State tracking
        self.state = self.load_state()
        self.current_skill_index = self.state.get("current_skill_index", 0)
        self.circuit_breakers = self.state.get("circuit_breakers", {})
        self.last_activity_time = time.time()

        # Backend health check
        self.backend_url = "http://localhost:8001/health"

    def load_state(self) -> dict:
        """Load practice state from JSON file"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading state: {e}")
                return {}
        return {}

    def save_state(self):
        """Save practice state to JSON file"""
        state = {
            "current_skill_index": self.current_skill_index,
            "circuit_breakers": self.circuit_breakers,
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving state: {e}")

    async def is_idle(self) -> bool:
        """
        Check if Worker Bee is idle.
        Idle = no active WebSocket connections AND backend healthy.
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.backend_url)
                if response.status_code == 200:
                    data = response.json()
                    # Check for active jobs or runners
                    active_jobs = data.get("active_jobs", 0)
                    active_runners = data.get("active_runners", 0)

                    # Idle if no active jobs (WebSocket sessions are jobs)
                    return active_jobs == 0
                return False
        except Exception:
            # If backend not reachable, not idle (or not ready)
            return False

    def is_circuit_breaker_active(self, skill: str) -> bool:
        """Check if circuit breaker is active for this skill"""
        if skill not in self.circuit_breakers:
            return False

        breaker = self.circuit_breakers[skill]
        expires_at = datetime.fromisoformat(breaker["expires_at"])

        if datetime.now() < expires_at:
            return True
        else:
            # Circuit breaker expired, remove it
            del self.circuit_breakers[skill]
            self.save_state()
            return False

    def activate_circuit_breaker(self, skill: str, duration_seconds: int = 3600):
        """Activate circuit breaker for skill (default 1 hour pause)"""
        expires_at = datetime.now() + timedelta(seconds=duration_seconds)
        self.circuit_breakers[skill] = {
            "activated_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "reason": "3 consecutive failures"
        }
        self.save_state()
        print(f"🔴 Circuit breaker activated for {skill} until {expires_at.strftime('%H:%M')}")

    def get_next_skill(self) -> str:
        """Get next skill in round-robin rotation"""
        skill = self.skills[self.current_skill_index]
        self.current_skill_index = (self.current_skill_index + 1) % len(self.skills)
        self.save_state()
        return skill

    async def run_practice_task(self, skill: str, timeout: int = 180) -> dict:
        """
        Run a practice task for the given skill.
        Returns result dict with success/failure and details.
        """
        start_time = time.time()

        try:
            # Generate practice task based on skill type
            task = self.generate_practice_task(skill)

            # Execute with timeout
            result = await asyncio.wait_for(
                self.execute_practice_task(skill, task),
                timeout=timeout
            )

            duration = time.time() - start_time

            return {
                "success": result.get("success", False),
                "skill": skill,
                "task": task,
                "result": result.get("output", ""),
                "duration": round(duration, 2),
                "timestamp": datetime.now().isoformat()
            }

        except asyncio.TimeoutError:
            duration = time.time() - start_time
            return {
                "success": False,
                "skill": skill,
                "task": task,
                "result": f"Timeout after {timeout}s",
                "duration": round(duration, 2),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "skill": skill,
                "task": task if 'task' in locals() else "unknown",
                "result": f"Error: {str(e)}",
                "duration": round(duration, 2),
                "timestamp": datetime.now().isoformat()
            }

    def get_difficulty_level(self, skill: str) -> str:
        """
        Get next difficulty level for skill.
        Rotates: Easy → Medium → Hard → Real
        """
        # Load last difficulty from state
        last_difficulty = self.state.get("last_difficulty", {}).get(skill, "Real")

        difficulty_cycle = ["Easy", "Medium", "Hard", "Real"]
        current_index = difficulty_cycle.index(last_difficulty) if last_difficulty in difficulty_cycle else 0
        next_index = (current_index + 1) % len(difficulty_cycle)
        next_difficulty = difficulty_cycle[next_index]

        # Save for next time
        if "last_difficulty" not in self.state:
            self.state["last_difficulty"] = {}
        self.state["last_difficulty"][skill] = next_difficulty
        self.save_state()

        return next_difficulty

    def generate_practice_task(self, skill: str) -> str:
        """
        Generate autonomous practice task for skill with varying difficulty.

        Difficulty levels:
        - Easy: Happy path, clear requirements
        - Medium: Ambiguous request, missing context
        - Hard: Edge case, conflicting requirements
        - Real: Actual content from production sites
        """

        # Four production sites for real scenarios
        REAL_SITES = [
            "mountainedgeplumbing.com",
            "ime-coach.com",
            "growyournumber.com",
            "language-lens-elite.lovable.app"
        ]

        difficulty = self.get_difficulty_level(skill)

        # Task templates by skill and difficulty
        tasks = {
            "skill-seo": {
                "Easy": "Audit the homepage title tag and meta description for mountainedgeplumbing.com",
                "Medium": "Find SEO issues on the site - check what matters most for local business",
                "Hard": "Site has good content but low rankings - what's wrong with technical SEO vs on-page?",
                "Real": f"Audit {REAL_SITES[hash(skill) % len(REAL_SITES)]} for missing schema markup and suggest implementation"
            },
            "skill-repair-pipeline": {
                "Easy": "Review the last git commit message - does it follow best practices?",
                "Medium": "Something broke after the last deploy - what's the debugging process?",
                "Hard": "Users report intermittent form failures but can't reproduce - systematic approach?",
                "Real": f"Analyze practice logs for {REAL_SITES[hash(skill + 'debug') % len(REAL_SITES)]} - what patterns indicate real bugs?"
            },
            "skill-web-architect": {
                "Easy": "Review mountainedgeplumbing.com homepage - suggest one color palette improvement",
                "Medium": "Site looks dated but not sure why - identify the aesthetic issues",
                "Hard": "Design needs to be modern but still appeal to 60+ demographic - how to balance?",
                "Real": f"Analyze {REAL_SITES[hash(skill + 'design') % len(REAL_SITES)]} design - what's one bold improvement that fits the brand?"
            },
            "skill-image-gen": {
                "Easy": "Generate a prompt for a professional headshot photo",
                "Medium": "Need hero image but brand voice unclear - what questions to ask first?",
                "Hard": "Generate image that works for both medical (serious) and financial (trustworthy) contexts",
                "Real": f"Create hero image prompt for {REAL_SITES[hash(skill + 'image') % len(REAL_SITES)]} that matches their brand aesthetic"
            },
            "skill-navigator": {
                "Easy": "Write steps to test the contact form submit button on mountainedgeplumbing.com",
                "Medium": "Form has validation but not sure what fields are required - test plan?",
                "Hard": "Form works on desktop, fails on mobile Safari - how to isolate the issue?",
                "Real": f"Plan browser automation for {REAL_SITES[hash(skill + 'nav') % len(REAL_SITES)]} critical user flow (signup/contact/booking)"
            },
            "skill-planner": {
                "Easy": "Plan adding a testimonials section to mountainedgeplumbing.com homepage",
                "Medium": "Client wants 'better engagement' - what does that actually mean? Plan questions first",
                "Hard": "Add booking system but existing form code is messy - rebuild or extend?",
                "Real": f"Plan enhancement for {REAL_SITES[hash(skill + 'plan') % len(REAL_SITES)]} based on their current business model"
            },
            "skill-builder": {
                "Easy": "Review a simple button component - check accessibility and styling",
                "Medium": "Component works but code is hard to read - what refactoring would help?",
                "Hard": "Need responsive nav that works on mobile, tablet, desktop with different layouts for each",
                "Real": f"Review actual component from {REAL_SITES[hash(skill + 'build') % len(REAL_SITES)]} - suggest one improvement"
            },
            "skill-reviewer": {
                "Easy": "Review the last practice task - did it achieve the goal?",
                "Medium": "Proposed solution works but feels wrong - what's missing in the review?",
                "Hard": "Two solutions both work technically - how to choose the better architecture?",
                "Real": f"Review last real change to {REAL_SITES[hash(skill + 'review') % len(REAL_SITES)]} - would skill-reviewer have caught issues?"
            },
            "skill-checker": {
                "Easy": "Check mountainedgeplumbing.com homepage for mobile responsiveness",
                "Medium": "Site 'doesn't work right' on some phones - what to check first?",
                "Hard": "Accessibility audit shows issues but which ones actually matter for users?",
                "Real": f"Full accessibility + mobile check for {REAL_SITES[hash(skill + 'check') % len(REAL_SITES)]} - prioritize findings"
            }
        }

        skill_tasks = tasks.get(skill, {
            "Easy": f"Practice {skill} with clear requirements",
            "Medium": f"Practice {skill} with ambiguous context",
            "Hard": f"Practice {skill} with edge cases",
            "Real": f"Apply {skill} to real production site"
        })

        task = skill_tasks.get(difficulty, skill_tasks["Easy"])

        return f"[{difficulty}] {task}"

    async def execute_practice_task(self, skill: str, task: str) -> dict:
        """
        Execute practice task (sandbox mode - no side effects).
        This is a simulated execution for MVP.
        In production, this would call actual skill execution.
        """
        # Simulate work
        await asyncio.sleep(2)

        # For MVP, all tasks succeed (placeholder)
        # In production, this would execute real skill logic
        return {
            "success": True,
            "output": f"Completed practice task: {task}"
        }

    def log_practice(self, result: dict):
        """Log practice result to skill-X.practice.md"""
        skill = result["skill"]
        practice_file = self.practice_dir / f"{skill}.practice.md"

        # Create file with header if it doesn't exist
        if not practice_file.exists():
            with open(practice_file, 'w') as f:
                f.write(f"# Practice Log: {skill}\n\n")
                f.write("Autonomous practice sessions logged here.\n\n")
                f.write("---\n\n")

        # Append practice entry
        with open(practice_file, 'a') as f:
            timestamp = result["timestamp"]
            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
            duration = result["duration"]

            f.write(f"## {timestamp} - {status}\n\n")
            f.write(f"**Duration:** {duration}s\n\n")
            f.write(f"**Task:** {result['task']}\n\n")
            f.write(f"**Result:** {result['result']}\n\n")
            f.write("---\n\n")

    def check_consecutive_failures(self, skill: str) -> int:
        """Check how many consecutive failures this skill has"""
        practice_file = self.practice_dir / f"{skill}.practice.md"

        if not practice_file.exists():
            return 0

        try:
            with open(practice_file, 'r') as f:
                lines = f.readlines()

            # Count consecutive failures from end of file
            consecutive = 0
            for line in reversed(lines):
                if "❌ FAILED" in line:
                    consecutive += 1
                elif "✅ SUCCESS" in line:
                    break

            return consecutive
        except Exception:
            return 0

    async def run_continuous(self):
        """Main continuous practice loop"""

        print("🐝 CONTINUOUS PRACTICE LOOP STARTED")
        print("=" * 70)
        print(f"Practicing {len(self.skills)} skills in rotation")
        print("Checking for idle state every 60 seconds")
        print("Practice runs every 5 minutes when idle")
        print("=" * 70 + "\n")

        while True:
            try:
                # Check if idle
                if await self.is_idle():
                    # Get next skill
                    skill = self.get_next_skill()

                    # Check circuit breaker
                    if self.is_circuit_breaker_active(skill):
                        print(f"⏸️  {skill} paused (circuit breaker active)")
                        await asyncio.sleep(300)  # Wait 5 min
                        continue

                    # Run practice task
                    print(f"\n🔄 Practicing: {skill}")
                    result = await self.run_practice_task(skill, timeout=180)

                    # Log result
                    self.log_practice(result)

                    if result["success"]:
                        print(f"✅ {skill} practice completed ({result['duration']}s)")
                    else:
                        print(f"❌ {skill} practice failed: {result['result']}")

                        # Check for consecutive failures
                        consecutive = self.check_consecutive_failures(skill)
                        if consecutive >= 3:
                            self.activate_circuit_breaker(skill, duration=3600)

                    # Wait 5 minutes before next practice
                    print(f"⏸️  Waiting 5 minutes before next practice...")
                    await asyncio.sleep(300)

                else:
                    # Not idle, check again in 1 minute
                    await asyncio.sleep(60)

            except KeyboardInterrupt:
                print("\n\n🛑 Practice loop stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Error in practice loop: {e}")
                import traceback
                traceback.print_exc()
                print("\n⏸️  Waiting 5 minutes before retry...\n")
                await asyncio.sleep(300)

        print(f"\n{'='*70}")
        print("PRACTICE LOOP SHUTDOWN")
        print(f"{'='*70}\n")


async def main():
    """Run the continuous practice loop"""
    loop = ContinuousPracticeLoop()
    await loop.run_continuous()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("WORKER BEE CONTINUOUS PRACTICE SYSTEM")
    print("="*70)
    print("\nStarting 24/7 autonomous practice...")
    print("Press Ctrl+C to stop\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutdown complete.\n")
