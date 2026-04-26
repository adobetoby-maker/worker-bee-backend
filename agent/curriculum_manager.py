"""
Curriculum Manager — The Brain

Tracks 30-day learning progress across 6 domains.
Generates next session agenda from real failures + gaps.
Adapts Month 2 curriculum based on Month 1 results.

State-driven, not date-driven.
Pauses when Toby uses system.
Resumes exactly where it left off.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class CurriculumManager:
    """
    The brain of the learning system.
    Manages 30-day curriculum, tracks progress, adapts to gaps.
    """

    STATE_FILE = Path.home() / "worker-bee/manifests/practice/curriculum-state.json"
    PRACTICE_DIR = Path.home() / "worker-bee/manifests/practice"

    def __init__(self):
        self.state = self.load_state()
        from .curriculum_template import CURRICULUM_MONTH_1
        self.template = CURRICULUM_MONTH_1

    def load_state(self) -> dict:
        """Load curriculum state or initialize if first run"""
        if self.STATE_FILE.exists():
            with open(self.STATE_FILE, 'r') as f:
                return json.load(f)
        else:
            return self._initialize_state()

    def _initialize_state(self) -> dict:
        """Initialize fresh curriculum state for Month 1 Day 1"""
        return {
            "month": 1,
            "day": 1,
            "current_domain": "conversation_communication",
            "current_week": 1,
            "domains": {
                "conversation_communication": {
                    "week": 1,
                    "topic": "understanding_intent",
                    "sessions_completed": 0,
                    "teach_back_scores": [],
                    "avg_score": None,
                    "status": "in_progress",
                    "weakness_flagged": False
                },
                "visual_generative": {
                    "week": 0,
                    "topic": None,
                    "sessions_completed": 0,
                    "teach_back_scores": [],
                    "avg_score": None,
                    "status": "pending",
                    "weakness_flagged": False
                },
                "file_document": {
                    "week": 0,
                    "topic": None,
                    "sessions_completed": 0,
                    "teach_back_scores": [],
                    "avg_score": None,
                    "status": "pending",
                    "weakness_flagged": False
                },
                "code_repair": {
                    "week": 0,
                    "topic": None,
                    "sessions_completed": 0,
                    "teach_back_scores": [],
                    "avg_score": None,
                    "status": "pending",
                    "weakness_flagged": False
                },
                "decision_integrity": {
                    "week": 0,
                    "topic": None,
                    "sessions_completed": 0,
                    "teach_back_scores": [],
                    "avg_score": None,
                    "status": "pending",
                    "weakness_flagged": False
                },
                "integration_prompt_craft": {
                    "week": 0,
                    "topic": None,
                    "sessions_completed": 0,
                    "teach_back_scores": [],
                    "avg_score": None,
                    "status": "pending",
                    "weakness_flagged": False
                }
            },
            "session_history": [],
            "gap_tracking": {},
            "reasoning_gap_tracking": {},
            "implementation_failures": [],
            "monthly_assessment": {
                "month": 1,
                "scheduled_date": None,
                "status": "pending",
                "results": None
            },
            "curriculum_adaptations": []
        }

    def save_state(self):
        """Persist curriculum state to disk"""
        self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def get_next_session(self) -> Optional[dict]:
        """
        Determine what the next session should cover.
        Called by cron before each session.

        Returns session brief or None if curriculum paused.
        """
        # Calculate which session number this is today
        today = datetime.now().strftime("%Y-%m-%d")
        sessions_today = len([
            s for s in self.state["session_history"]
            if s["session_id"].startswith(today)
        ])

        # Max 6 sessions per day
        if sessions_today >= 6:
            return None

        # Get current domain and week
        domain_id = self.state["current_domain"]
        domain = self.state["domains"][domain_id]
        week_num = domain["week"]

        # Get week template
        week_template = self._get_week_template(domain_id, week_num)
        if not week_template:
            return None

        # Determine session type from daily schedule
        session_type = self.template["daily_schedule"][sessions_today]["session_type"]

        # Get previous session for accountability
        previous_session = self._get_previous_session()
        gap_file = self._get_gap_file(previous_session) if previous_session else None
        reasoning_gap_file = self._get_reasoning_gap_file(previous_session) if previous_session else None

        # Check for implementation failures from yesterday's Session 6
        implementation_failure = self._get_recent_implementation_failure()

        # Build agenda
        agenda = self._build_agenda(
            week_template,
            session_type,
            domain_id,
            gap_file,
            reasoning_gap_file,
            implementation_failure
        )

        # Generate session ID
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        session_id = timestamp

        return {
            "session_id": session_id,
            "domain": domain_id,
            "week": week_num,
            "topic": week_template["topic"],
            "session_type": session_type,
            "previous_session": previous_session,
            "gap_from_previous": gap_file,
            "reasoning_gap_from_previous": reasoning_gap_file,
            "implementation_failure": implementation_failure,
            "real_failures_source": week_template["real_failures_source"],
            "agenda": agenda
        }

    def record_session_complete(self, session_id: str, results: dict):
        """
        After session completes, update state.

        results = {
            "teach_back_score": {"accuracy": 8, "clarity": 7, "completeness": 9},
            "gap_detected": true,
            "gap_file": "2026-04-25-0900/gap-analysis.md",
            "reasoning_gap_detected": true,
            "reasoning_gap_file": "2026-04-25-0900/reasoning-gap-analysis.md",
            "implementation_success": false,  # only for session type "implement"
            "implementation_failure_details": "...",
            "reasoning_transferred": true
        }
        """
        domain_id = self.state["current_domain"]
        domain = self.state["domains"][domain_id]

        # Add to session history
        self.state["session_history"].append({
            "session_id": session_id,
            "day": self.state["day"],
            "domain": domain_id,
            "week": domain["week"],
            "topic": domain["topic"],
            "session_type": results.get("session_type"),
            "completed": True,
            "teach_back_score": results.get("teach_back_score"),
            "gap_detected": results.get("gap_detected"),
            "reasoning_gap_detected": results.get("reasoning_gap_detected"),
            "implementation_success": results.get("implementation_success")
        })

        # Track factual gaps
        if results.get("gap_detected"):
            if domain_id not in self.state["gap_tracking"]:
                self.state["gap_tracking"][domain_id] = []

            self.state["gap_tracking"][domain_id].append({
                "date": session_id[:10],
                "session": session_id,
                "gap_summary": results.get("gap_summary"),
                "gap_file": results["gap_file"]
            })

        # Track reasoning gaps separately
        if results.get("reasoning_gap_detected"):
            if domain_id not in self.state["reasoning_gap_tracking"]:
                self.state["reasoning_gap_tracking"][domain_id] = []

            self.state["reasoning_gap_tracking"][domain_id].append({
                "date": session_id[:10],
                "session": session_id,
                "reasoning_gap_summary": results.get("reasoning_gap_summary"),
                "reasoning_gap_file": results["reasoning_gap_file"]
            })

        # Track implementation failures (Session 6)
        if results.get("session_type") == "implement":
            if not results.get("implementation_success"):
                self.state["implementation_failures"].append({
                    "date": session_id[:10],
                    "session": session_id,
                    "domain": domain_id,
                    "topic": domain["topic"],
                    "failure_details": results.get("implementation_failure_details"),
                    "addressed": False
                })

        # Update teach-back scores
        if results.get("teach_back_score"):
            scores = results["teach_back_score"]
            avg_score = (scores["accuracy"] + scores["clarity"] + scores["completeness"]) / 3

            domain["teach_back_scores"].append(avg_score)
            domain["avg_score"] = sum(domain["teach_back_scores"]) / len(domain["teach_back_scores"])

            # Check weakness threshold: 3+ sessions below 7.0
            if len(domain["teach_back_scores"]) >= 3:
                recent_scores = domain["teach_back_scores"][-3:]
                if all(score < 7.0 for score in recent_scores):
                    if not domain["weakness_flagged"]:
                        domain["weakness_flagged"] = True
                        self._escalate_weakness(domain_id, domain["avg_score"])

        # Increment domain session count
        domain["sessions_completed"] += 1

        # Advance curriculum if needed
        # Each week = 6 sessions, 4 weeks per domain = 24 sessions
        if domain["sessions_completed"] > 0 and domain["sessions_completed"] % 6 == 0:
            # Completed a week
            week_completed = domain["sessions_completed"] // 6
            if week_completed < 4:
                # Advance to next week in this domain
                domain["week"] = week_completed + 1
                domain["topic"] = self._get_week_template(domain_id, domain["week"])["topic"]
            else:
                # Domain complete, move to next domain
                domain["status"] = "complete"
                self._advance_domain()

        # Check if day complete (6 sessions)
        sessions_today_count = len([
            s for s in self.state["session_history"]
            if s["session_id"][:10] == session_id[:10]
        ])
        if sessions_today_count >= 6:
            self.state["day"] += 1

        # Schedule monthly assessment on day 29
        if self.state["day"] == 29:
            self._schedule_monthly_assessment()

        # Generate Month 2 after assessment complete
        if self.state["day"] == 30 and self.state["monthly_assessment"]["status"] == "complete":
            self._generate_month_2_curriculum()

        self.save_state()

    def _get_week_template(self, domain_id: str, week_num: int) -> Optional[dict]:
        """Get week curriculum template for domain"""
        for domain in self.template["domains"]:
            if domain["id"] == domain_id:
                for week in domain["weeks"]:
                    if week["week"] == week_num:
                        return week
        return None

    def _get_previous_session(self) -> Optional[str]:
        """Get previous session ID"""
        if len(self.state["session_history"]) > 0:
            return self.state["session_history"][-1]["session_id"]
        return None

    def _get_gap_file(self, session_id: str) -> Optional[str]:
        """Get gap analysis file from previous session"""
        gap_dir = self.PRACTICE_DIR / "learning-sessions" / session_id
        gap_file = gap_dir / "gap-analysis.md"
        if gap_file.exists():
            return str(gap_file)
        return None

    def _get_reasoning_gap_file(self, session_id: str) -> Optional[str]:
        """Get reasoning gap analysis file from previous session"""
        gap_dir = self.PRACTICE_DIR / "learning-sessions" / session_id
        gap_file = gap_dir / "reasoning-gap-analysis.md"
        if gap_file.exists():
            return str(gap_file)
        return None

    def _get_recent_implementation_failure(self) -> Optional[dict]:
        """
        Get most recent unaddressed implementation failure.
        Session 6 failures feed Session 1 next day.
        """
        unaddressed = [f for f in self.state["implementation_failures"] if not f["addressed"]]
        if unaddressed:
            # Return most recent
            failure = unaddressed[-1]
            # Mark as addressed
            for f in self.state["implementation_failures"]:
                if f["session"] == failure["session"]:
                    f["addressed"] = True
            return failure
        return None

    def _build_agenda(self, week_template: dict, session_type: str,
                      domain_id: str, gap_file: Optional[str],
                      reasoning_gap_file: Optional[str],
                      implementation_failure: Optional[dict]) -> dict:
        """Build 20-minute session agenda"""

        # Open phase (2 min)
        open_content = "Starting session."
        if gap_file or reasoning_gap_file:
            open_content = (
                f"Upload bee-notes.md and claude-summary.md from previous session. "
                f"Gap analysis: {gap_file or 'none'}. "
                f"Reasoning gap: {reasoning_gap_file or 'none'}. "
                f"Test me on where I misunderstood last time."
            )

        # Accountability phase (5 min)
        accountability = self._build_accountability_test(
            session_type, gap_file, reasoning_gap_file, implementation_failure
        )

        # Lesson phase (8 min)
        lesson = self._build_lesson_plan(week_template, session_type)

        # Assignment phase (2 min)
        assignment = self._build_research_assignment(week_template)

        # Teach-back phase (2 min)
        teach_back = (
            f"Explain to phi4 (who has never seen this): {week_template['topic']}. "
            f"Make it clear enough that phi4 could apply it tomorrow. "
            f"Claude will score: Accuracy, Clarity, Completeness (1-10 each)."
        )

        # Close phase (1 min) - reasoning transfer
        reasoning_prompt = (
            f"Before writing summary, explain your reasoning:\n"
            f"- WHY you approach {week_template['topic']} this way\n"
            f"- WHAT would change your approach\n"
            f"- WHAT this connects to in other domains\n"
            f"Include cost-benefit analysis of this approach."
        )

        return {
            "open": open_content,
            "accountability": accountability,
            "lesson": lesson,
            "assignment": assignment,
            "teach_back": teach_back,
            "reasoning_prompt": reasoning_prompt
        }

    def _build_accountability_test(self, session_type: str, gap_file: Optional[str],
                                    reasoning_gap_file: Optional[str],
                                    implementation_failure: Optional[dict]) -> str:
        """Build accountability test from previous session"""

        if implementation_failure:
            return (
                f"Yesterday's implementation session failed. Here's what broke:\n"
                f"{implementation_failure['failure_details']}\n\n"
                f"Before we start today's lesson, explain:\n"
                f"1. What went wrong\n"
                f"2. What you should have done differently\n"
                f"3. How today's lesson will help prevent this"
            )

        if session_type == "test":
            return (
                f"Test from last session. Claude will present 3 scenarios "
                f"from the previous lesson. Apply what you learned."
            )

        if gap_file or reasoning_gap_file:
            return (
                f"We found gaps in your understanding last session. "
                f"Let's verify those gaps closed. Quick quiz on the gap topics."
            )

        return "Ready to learn. Let's begin."

    def _build_lesson_plan(self, week_template: dict, session_type: str) -> str:
        """Build lesson content for this session"""
        topic = week_template["topic"]
        focus = week_template["focus"]

        if session_type == "teach":
            return (
                f"Today's topic: {topic}\n"
                f"Focus: {focus}\n\n"
                f"Claude will teach this using real examples from practice logs. "
                f"Back-and-forth dialogue. Ask questions when unclear."
            )

        elif session_type == "test":
            return (
                f"Testing understanding of: {topic}\n"
                f"Claude presents 3 real scenarios. You apply the lesson."
            )

        elif session_type == "visual":
            return (
                f"Visual session: {topic}\n"
                f"Upload screenshots from real sites. "
                f"Claude guides visual analysis specific to {focus}."
            )

        elif session_type == "implement":
            return (
                f"Implementation: Apply today's learning to real task.\n"
                f"Topic: {topic}\n"
                f"Claude provides a real Worker Bee task. "
                f"You attempt it. Claude reviews your approach."
            )

        return f"Session on {topic}"

    def _build_research_assignment(self, week_template: dict) -> str:
        """Build specific research assignment"""
        topic = week_template["topic"]
        source = week_template["real_failures_source"]

        return (
            f"Research assignment before next session:\n"
            f"1. Find 5 examples in {source} related to {topic}\n"
            f"2. Identify the pattern across those examples\n"
            f"3. Write what you notice in bee-notes.md\n"
            f"Bring evidence to next session."
        )

    def _escalate_weakness(self, domain_id: str, avg_score: float):
        """Notify Toby of domain weakness via morning report + dashboard flag"""
        # Write to morning report log
        report_file = self.PRACTICE_DIR / "morning-report-flags.log"
        with open(report_file, 'a') as f:
            f.write(
                f"{datetime.now().isoformat()} | WEAKNESS | "
                f"Domain: {domain_id} | Avg Score: {avg_score:.1f}/10 | "
                f"3+ sessions below 7.0 threshold\n"
            )

        # Dashboard flag (read by dashboard component)
        dashboard_file = self.PRACTICE_DIR / "dashboard-flags.json"
        flags = []
        if dashboard_file.exists():
            with open(dashboard_file, 'r') as f:
                flags = json.load(f)

        flags.append({
            "type": "WEAKNESS",
            "domain": domain_id,
            "avg_score": avg_score,
            "message": f"{domain_id} failing 3+ sessions. May be capability limit.",
            "timestamp": datetime.now().isoformat()
        })

        with open(dashboard_file, 'w') as f:
            json.dump(flags, f, indent=2)

    def _advance_domain(self):
        """Move to next domain after completing current one"""
        domain_order = [
            "conversation_communication",
            "visual_generative",
            "file_document",
            "code_repair",
            "decision_integrity",
            "integration_prompt_craft"
        ]

        current_idx = domain_order.index(self.state["current_domain"])
        if current_idx < len(domain_order) - 1:
            next_domain = domain_order[current_idx + 1]
            self.state["current_domain"] = next_domain
            self.state["domains"][next_domain]["status"] = "in_progress"
            self.state["domains"][next_domain]["week"] = 1

            # Set topic from template
            week_template = self._get_week_template(next_domain, 1)
            if week_template:
                self.state["domains"][next_domain]["topic"] = week_template["topic"]

    def _schedule_monthly_assessment(self):
        """Schedule day 29 assessment"""
        self.state["monthly_assessment"]["scheduled_date"] = (
            datetime.now() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        self.state["monthly_assessment"]["status"] = "scheduled"

    def _generate_month_2_curriculum(self):
        """
        Generate Month 2 curriculum based on Month 1 results.
        Weakest 2 domains get double sessions.
        Strong domains get maintenance mode.
        """
        # Score each domain
        domain_scores = {}
        for domain_id, domain_data in self.state["domains"].items():
            if domain_data["avg_score"] is not None:
                domain_scores[domain_id] = domain_data["avg_score"]

        # Sort by score (lowest first = weakest)
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1])

        # Weakest 2 domains
        weak_domains = [d[0] for d in sorted_domains[:2]] if len(sorted_domains) >= 2 else []

        # Generate Month 2 adaptation
        adaptation = {
            "month": 2,
            "weak_domains": weak_domains,
            "double_sessions": weak_domains,
            "maintenance_domains": [d[0] for d in sorted_domains[2:]],
            "integration_weeks": [
                {"week": 3, "domains": ["conversation_communication", "code_repair"]},
                {"week": 4, "domains": ["visual_generative", "integration_prompt_craft"]}
            ],
            "reasoning": f"Weakest domains from Month 1: {weak_domains} with scores {[domain_scores[d] for d in weak_domains]}"
        }

        self.state["curriculum_adaptations"].append(adaptation)
        self.state["month"] = 2
        self.state["day"] = 1

        # Reset for Month 2
        for domain_id in weak_domains:
            self.state["domains"][domain_id]["week"] = 1
            self.state["domains"][domain_id]["status"] = "in_progress"

        self.save_state()

    def get_progress_summary(self) -> dict:
        """Get current progress summary for dashboard"""
        total_sessions = len(self.state["session_history"])
        today = datetime.now().strftime("%Y-%m-%d")
        sessions_today = len([
            s for s in self.state["session_history"]
            if s["session_id"].startswith(today)
        ])

        domain_summaries = {}
        for domain_id, domain_data in self.state["domains"].items():
            domain_summaries[domain_id] = {
                "status": domain_data["status"],
                "week": domain_data["week"],
                "topic": domain_data["topic"],
                "avg_score": domain_data["avg_score"],
                "sessions_completed": domain_data["sessions_completed"],
                "weakness_flagged": domain_data["weakness_flagged"]
            }

        return {
            "month": self.state["month"],
            "day": self.state["day"],
            "total_sessions": total_sessions,
            "sessions_today": sessions_today,
            "current_domain": self.state["current_domain"],
            "domains": domain_summaries,
            "pending_implementation_failures": len([
                f for f in self.state["implementation_failures"] if not f["addressed"]
            ])
        }
