#!/usr/bin/env python3
"""
Morning Report - Daily Worker Bee Status Summary

Runs daily at 9am, collects system health data, and emails a report.

Checks:
- System health (ports, processes)
- Practice loop status and failures
- Site health (all 4 production sites)
- Deployment status (Blueprint, FastAPI)
- Recent git activity
- Urgent emails (if Gmail configured)

Sends formatted report to adobetoby@gmail.com
"""

import asyncio
import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import httpx


class MorningReport:
    def __init__(self):
        self.report_time = datetime.now()
        self.base_dir = Path.home() / "worker-bee"
        self.practice_dir = self.base_dir / "manifests/practice"

        # Production sites from site registry
        self.sites = [
            "mountainedgeplumbing.com",
            "ime-coach.com",
            "growyournumber.com",
            "language-lens-elite.lovable.app"
        ]

    async def check_system_health(self) -> Dict[str, Any]:
        """Check if key services are running"""
        health = {
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }

        # Check FastAPI backend (port 8001)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get("http://localhost:8001/health")
                health["services"]["fastapi"] = {
                    "status": "✅ Running" if r.status_code == 200 else "⚠️ Unhealthy",
                    "port": 8001,
                    "data": r.json() if r.status_code == 200 else None
                }
        except Exception as e:
            health["services"]["fastapi"] = {
                "status": "❌ Down",
                "port": 8001,
                "error": str(e)
            }

        # Check Blueprint server (port 8002)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get("http://localhost:8002/health")
                health["services"]["blueprint"] = {
                    "status": "✅ Running" if r.status_code == 200 else "⚠️ Unhealthy",
                    "port": 8002,
                    "data": r.json() if r.status_code == 200 else None
                }
        except Exception as e:
            health["services"]["blueprint"] = {
                "status": "❌ Down",
                "port": 8002,
                "error": str(e)
            }

        # Check Ollama
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get("http://localhost:11434/api/ps")
                if r.status_code == 200:
                    models = r.json().get("models", [])
                    health["services"]["ollama"] = {
                        "status": "✅ Running",
                        "port": 11434,
                        "loaded_models": len(models)
                    }
                else:
                    health["services"]["ollama"] = {
                        "status": "⚠️ Unhealthy",
                        "port": 11434
                    }
        except Exception as e:
            health["services"]["ollama"] = {
                "status": "❌ Down",
                "port": 11434,
                "error": str(e)
            }

        # Check Cloudflare tunnel
        try:
            result = subprocess.run(["pgrep", "-f", "cloudflared"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                health["services"]["cloudflare_tunnel"] = {
                    "status": "✅ Running",
                    "pid": result.stdout.strip()
                }
            else:
                health["services"]["cloudflare_tunnel"] = {
                    "status": "❌ Down"
                }
        except Exception as e:
            health["services"]["cloudflare_tunnel"] = {
                "status": "❌ Error",
                "error": str(e)
            }

        return health

    def check_practice_failures(self) -> Dict[str, Any]:
        """Check for recent practice loop failures"""
        failures = {
            "total_failures_24h": 0,
            "skills_with_failures": [],
            "circuit_breakers": []
        }

        # Check practice state for circuit breakers
        state_file = self.practice_dir / "practice-state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    circuit_breakers = state.get("circuit_breakers", {})

                    for skill, breaker in circuit_breakers.items():
                        expires_at = datetime.fromisoformat(breaker["expires_at"])
                        if datetime.now() < expires_at:
                            failures["circuit_breakers"].append({
                                "skill": skill,
                                "expires_at": expires_at.strftime("%H:%M"),
                                "reason": breaker.get("reason", "Unknown")
                            })
            except Exception as e:
                print(f"Error reading practice state: {e}")

        # Check practice logs for recent failures (last 24 hours)
        yesterday = datetime.now() - timedelta(hours=24)

        for practice_file in self.practice_dir.glob("skill-*.practice.md"):
            skill_name = practice_file.stem  # e.g., "skill-seo.practice"

            try:
                with open(practice_file, 'r') as f:
                    content = f.read()

                    # Count recent failures
                    recent_failures = 0
                    for line in content.split('\n'):
                        if "❌ FAILED" in line and "##" in line:
                            # Try to parse timestamp
                            try:
                                timestamp_str = line.split("##")[1].split("-")[0].strip()
                                timestamp = datetime.fromisoformat(timestamp_str)
                                if timestamp > yesterday:
                                    recent_failures += 1
                            except:
                                pass

                    if recent_failures > 0:
                        failures["total_failures_24h"] += recent_failures
                        failures["skills_with_failures"].append({
                            "skill": skill_name,
                            "failures": recent_failures
                        })
            except Exception as e:
                print(f"Error reading {practice_file}: {e}")

        return failures

    async def check_site_health(self) -> List[Dict[str, Any]]:
        """Quick health check on all 4 production sites"""
        results = []

        for site in self.sites:
            url = f"https://{site}"
            try:
                async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                    start = datetime.now()
                    r = await client.get(url)
                    duration = (datetime.now() - start).total_seconds()

                    results.append({
                        "site": site,
                        "status": "✅ Up" if r.status_code == 200 else f"⚠️ {r.status_code}",
                        "response_time": f"{duration:.2f}s",
                        "healthy": r.status_code == 200 and duration < 5.0
                    })
            except Exception as e:
                results.append({
                    "site": site,
                    "status": "❌ Down",
                    "error": str(e)[:100],
                    "healthy": False
                })

        return results

    def check_git_activity(self) -> Dict[str, Any]:
        """Check recent git activity in backend repo"""
        git_info = {
            "branch": "unknown",
            "last_commit": "unknown",
            "uncommitted_changes": False
        }

        try:
            os.chdir(self.base_dir)

            # Get current branch
            result = subprocess.run(["git", "branch", "--show-current"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                git_info["branch"] = result.stdout.strip()

            # Get last commit
            result = subprocess.run(["git", "log", "-1", "--pretty=format:%h - %s (%ar)"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                git_info["last_commit"] = result.stdout.strip()

            # Check for uncommitted changes
            result = subprocess.run(["git", "status", "--porcelain"],
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                git_info["uncommitted_changes"] = True
                git_info["changed_files"] = len(result.stdout.strip().split('\n'))

        except Exception as e:
            git_info["error"] = str(e)

        return git_info

    def format_report(self, health: Dict, practice: Dict, sites: List, git: Dict) -> str:
        """Format all data into readable email report"""

        report = f"""☀️ WORKER BEE MORNING REPORT
{self.report_time.strftime('%A, %B %d, %Y at %I:%M %p')}

{'='*70}
🔧 SYSTEM HEALTH
{'='*70}

"""

        # System services
        for service, info in health["services"].items():
            report += f"{service.upper().replace('_', ' ')}: {info['status']}\n"
            if "port" in info:
                report += f"  Port: {info['port']}\n"
            if "error" in info:
                report += f"  Error: {info['error']}\n"
            if service == "ollama" and "loaded_models" in info:
                report += f"  Models loaded: {info['loaded_models']}\n"

        report += f"\n{'='*70}\n🎓 PRACTICE LOOP STATUS\n{'='*70}\n\n"

        # Practice failures
        if practice["total_failures_24h"] > 0:
            report += f"⚠️ {practice['total_failures_24h']} failures in last 24 hours\n\n"
            for skill_fail in practice["skills_with_failures"]:
                report += f"  • {skill_fail['skill']}: {skill_fail['failures']} failures\n"
        else:
            report += "✅ No failures in last 24 hours\n"

        # Circuit breakers
        if practice["circuit_breakers"]:
            report += f"\n🔴 Active circuit breakers:\n"
            for cb in practice["circuit_breakers"]:
                report += f"  • {cb['skill']} - expires at {cb['expires_at']}\n"
                report += f"    Reason: {cb['reason']}\n"
        else:
            report += "\n✅ No active circuit breakers\n"

        report += f"\n{'='*70}\n🌐 PRODUCTION SITES\n{'='*70}\n\n"

        # Site health
        all_healthy = all(site.get("healthy", False) for site in sites)
        if all_healthy:
            report += "✅ All sites healthy\n\n"
        else:
            report += "⚠️ Some sites need attention:\n\n"

        for site_info in sites:
            report += f"{site_info['status']} {site_info['site']}\n"
            if "response_time" in site_info:
                report += f"  Response time: {site_info['response_time']}\n"
            if "error" in site_info:
                report += f"  Error: {site_info['error']}\n"

        report += f"\n{'='*70}\n📊 GIT STATUS\n{'='*70}\n\n"

        # Git info
        report += f"Branch: {git.get('branch', 'unknown')}\n"
        report += f"Last commit: {git.get('last_commit', 'unknown')}\n"

        if git.get("uncommitted_changes"):
            report += f"\n⚠️ {git.get('changed_files', 0)} uncommitted changes\n"
        else:
            report += f"\n✅ Working tree clean\n"

        report += f"\n{'='*70}\n🔗 QUICK LINKS\n{'='*70}\n\n"

        report += "• Worker Bee Frontend: https://worker-bee.lovable.app\n"
        report += "• Backend Config: https://bee.tobyandertonmd.com\n"
        report += "• Blueprint: https://blueprint.worker-bee.app\n"
        report += "• Backend Repo: https://github.com/adobetoby-maker/worker-bee-backend\n"
        report += "• Frontend Repo: https://github.com/adobetoby-maker/worker-bee\n"

        report += f"\n{'='*70}\n"
        report += "🐝 Always buzzing, never sleeping.\n"
        report += f"{'='*70}\n"

        return report

    async def push_to_frontend(self, report: str, health: Dict, practice: Dict, sites: List, git: Dict):
        """Save report to JSON file that frontend can fetch"""

        # Save full JSON data for frontend API
        report_data = {
            "generated_at": self.report_time.isoformat(),
            "report_text": report,
            "health": health,
            "practice": practice,
            "sites": sites,
            "git": git,
            "summary": {
                "all_services_up": all(
                    svc.get("status", "").startswith("✅")
                    for svc in health["services"].values()
                ),
                "all_sites_healthy": all(site.get("healthy", False) for site in sites),
                "has_failures": practice["total_failures_24h"] > 0,
                "has_circuit_breakers": len(practice["circuit_breakers"]) > 0
            }
        }

        # Save to JSON file
        report_file = self.base_dir / "morning-report.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"✅ Morning report saved to {report_file}")

        # Also save text version for quick reading
        text_file = self.base_dir / f"morning-report-{self.report_time.strftime('%Y%m%d')}.txt"
        with open(text_file, 'w') as f:
            f.write(report)

        print(f"📄 Text report saved to {text_file}")

        # Send WebSocket notification to frontend (if backend is running)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # POST to backend to trigger WebSocket push
                await client.post(
                    "http://localhost:8001/api/morning-report",
                    json=report_data,
                    timeout=5.0
                )
                print("✅ Pushed report to frontend via WebSocket")
        except Exception as e:
            print(f"⚠️  Could not push to WebSocket (backend may not be running): {e}")

        return True

    async def generate_and_send(self):
        """Main method - generate report and push to frontend"""
        print(f"\n🌅 Generating morning report at {self.report_time.strftime('%I:%M %p')}")

        # Collect all data
        health = await self.check_system_health()
        practice = self.check_practice_failures()
        sites = await self.check_site_health()
        git = self.check_git_activity()

        # Format report
        report = self.format_report(health, practice, sites, git)

        # Print to console for debugging
        print("\n" + "="*70)
        print(report)
        print("="*70 + "\n")

        # Push to frontend
        await self.push_to_frontend(report, health, practice, sites, git)


async def main():
    """Run morning report"""
    reporter = MorningReport()
    await reporter.generate_and_send()


if __name__ == "__main__":
    asyncio.run(main())
