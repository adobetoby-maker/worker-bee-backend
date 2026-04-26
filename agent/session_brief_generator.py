"""
Session Brief Generator

Builds 20-minute session agenda from:
- Curriculum plan
- Recent failures from practice logs
- Gaps from previous session
- Implementation failures
- Real examples

Outputs specific brief ready for Claude conversation.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class SessionBriefGenerator:
    """
    Generates specific session briefs with real failure examples.
    """

    PRACTICE_DIR = Path.home() / "worker-bee/manifests/practice"
    MANIFESTS_DIR = Path.home() / "worker-bee/manifests"

    def generate_brief(self, session_info: dict) -> dict:
        """
        Generate complete session brief from curriculum manager's session info.

        session_info from curriculum_manager.get_next_session()
        Returns detailed brief ready for browser automation.
        """
        # Extract real failures from source
        failures = self._get_real_failures(
            session_info["real_failures_source"],
            session_info["topic"]
        )

        # Build session brief
        brief = {
            "session_id": session_info["session_id"],
            "domain": session_info["domain"],
            "week": session_info["week"],
            "topic": session_info["topic"],
            "session_type": session_info["session_type"],
            "timestamp": datetime.now().isoformat(),

            # Files to upload at session start
            "upload_files": self._get_upload_files(session_info),

            # Agenda phases
            "agenda": session_info["agenda"],

            # Real failures with examples
            "real_failures": failures,

            # Teach-back prompt
            "teach_back_prompt": self._build_teach_back_prompt(session_info),

            # Reasoning transfer prompt
            "reasoning_prompt": session_info["agenda"]["reasoning_prompt"],

            # Expected outputs
            "expected_outputs": {
                "bee_notes": f"{session_info['session_id']}/bee-notes.md",
                "claude_summary": f"{session_info['session_id']}/claude-summary.md",
                "gap_analysis": f"{session_info['session_id']}/gap-analysis.md",
                "reasoning_gap_analysis": f"{session_info['session_id']}/reasoning-gap-analysis.md",
                "scores": f"{session_info['session_id']}/scores.md",
                "transcript": f"{session_info['session_id']}/transcript.md"
            }
        }

        # Save brief to disk
        self._save_brief(brief)

        return brief

    def _get_real_failures(self, source_file: str, topic: str) -> List[Dict]:
        """
        Extract real failures from practice log or session log.
        Last 7 days, top 5 by frequency/recency.
        """
        failures = []

        # Determine source type
        if source_file == "SESSIONS.md":
            failures = self._extract_from_sessions(topic)
        elif source_file == "JOURNAL.md":
            failures = self._extract_from_journal(topic)
        elif source_file == "PRACTICE.md":
            failures = self._extract_from_practice_log(topic)
        elif source_file.endswith(".practice.md"):
            failures = self._extract_from_skill_practice(source_file, topic)

        # Limit to top 5 most recent/relevant
        return failures[:5]

    def _extract_from_skill_practice(self, filename: str, topic: str) -> List[Dict]:
        """Extract failures from skill-*.practice.md files"""
        failures = []

        # Search in pipelines directories
        search_paths = [
            self.MANIFESTS_DIR / "pipelines" / "builder" / filename,
            self.MANIFESTS_DIR / "pipelines" / "tester" / filename,
            self.MANIFESTS_DIR / "pipelines" / "email" / filename,
            self.MANIFESTS_DIR / "pipelines" / "repair" / filename,
        ]

        for path in search_paths:
            if path.exists():
                content = path.read_text()

                # Parse practice runs
                # Looking for pattern: ### Practice Run #N — YYYY-MM-DD HH:MM
                pattern = r'### Practice Run #(\d+) — (\d{4}-\d{2}-\d{2} \d{2}:\d{2})'
                matches = re.finditer(pattern, content)

                for match in matches:
                    iteration = match.group(1)
                    date_str = match.group(2)

                    # Get content after this header until next header
                    start = match.end()
                    next_match = re.search(r'###', content[start:])
                    end = start + next_match.start() if next_match else len(content)
                    run_content = content[start:end]

                    # Check if this run was a failure and relevant to topic
                    if '❌ FAILURE' in run_content or '👎 REJECTED' in run_content:
                        # Extract failure points
                        failure_match = re.search(r'\*\*Failure Points:\*\* (.+)', run_content)
                        if failure_match:
                            failure_desc = failure_match.group(1)

                            # Check relevance to topic (simple keyword match)
                            topic_keywords = topic.replace('_', ' ').split()
                            if any(kw.lower() in run_content.lower() for kw in topic_keywords):
                                failures.append({
                                    "iteration": iteration,
                                    "date": date_str,
                                    "description": failure_desc,
                                    "source": filename
                                })

                break  # Found the file, stop searching

        return failures

    def _extract_from_sessions(self, topic: str) -> List[Dict]:
        """Extract relevant examples from SESSIONS.md"""
        sessions_file = Path.home() / "worker-bee/SESSIONS.md"
        if not sessions_file.exists():
            return []

        content = sessions_file.read_text()
        failures = []

        # Look for session entries with issues related to topic
        # This is a simplified version - would need more sophisticated parsing
        lines = content.split('\n')
        topic_keywords = topic.replace('_', ' ').split()

        for i, line in enumerate(lines):
            if any(kw.lower() in line.lower() for kw in topic_keywords):
                # Found relevant line, extract context
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 3)
                context = '\n'.join(lines[context_start:context_end])

                failures.append({
                    "iteration": "N/A",
                    "date": "recent",
                    "description": line.strip(),
                    "context": context,
                    "source": "SESSIONS.md"
                })

        return failures

    def _extract_from_journal(self, topic: str) -> List[Dict]:
        """Extract learning examples from JOURNAL.md"""
        journal_file = Path.home() / "worker-bee/JOURNAL.md"
        if not journal_file.exists():
            return []

        content = journal_file.read_text()
        failures = []

        # Look for journal entries related to topic
        topic_keywords = topic.replace('_', ' ').split()

        # Find sections that match topic
        sections = re.split(r'## Journal Entry:', content)
        for section in sections[1:]:  # Skip intro
            if any(kw.lower() in section.lower() for kw in topic_keywords):
                # Extract date and summary
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', section)
                date = date_match.group(1) if date_match else "recent"

                # Get first paragraph as description
                paragraphs = section.split('\n\n')
                description = paragraphs[0] if paragraphs else section[:200]

                failures.append({
                    "iteration": "N/A",
                    "date": date,
                    "description": description.strip(),
                    "source": "JOURNAL.md"
                })

        return failures

    def _extract_from_practice_log(self, topic: str) -> List[Dict]:
        """Extract from Claude's PRACTICE.md"""
        practice_file = Path.home() / "worker-bee/PRACTICE.md"
        if not practice_file.exists():
            return []

        content = practice_file.read_text()
        failures = []

        # Similar extraction to journal
        topic_keywords = topic.replace('_', ' ').split()

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if any(kw.lower() in line.lower() for kw in topic_keywords):
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 3)
                context = '\n'.join(lines[context_start:context_end])

                failures.append({
                    "iteration": "N/A",
                    "date": "recent",
                    "description": line.strip(),
                    "context": context,
                    "source": "PRACTICE.md"
                })

        return failures

    def _get_upload_files(self, session_info: dict) -> List[str]:
        """Get files to upload at session start (from previous session)"""
        files = []

        if session_info.get("previous_session"):
            prev_id = session_info["previous_session"]
            session_dir = self.PRACTICE_DIR / "learning-sessions" / prev_id

            # bee-notes.md from previous session
            bee_notes = session_dir / "bee-notes.md"
            if bee_notes.exists():
                files.append(str(bee_notes))

            # claude-summary.md from previous session
            claude_summary = session_dir / "claude-summary.md"
            if claude_summary.exists():
                files.append(str(claude_summary))

        return files

    def _build_teach_back_prompt(self, session_info: dict) -> str:
        """Build specific teach-back prompt for this session"""
        topic = session_info["topic"].replace('_', ' ')

        return (
            f"Now teach this back to me.\n\n"
            f"Imagine you're explaining '{topic}' to phi4, who has never seen this before. "
            f"phi4 needs to be able to apply this tomorrow on a real task.\n\n"
            f"I'll score you on three dimensions (1-10 each):\n"
            f"- Accuracy: Is it correct?\n"
            f"- Clarity: Could phi4 follow this?\n"
            f"- Completeness: Did you cover all key points?\n\n"
            f"Go ahead."
        )

    def _save_brief(self, brief: dict):
        """Save session brief to disk for debugging/logging"""
        import json

        brief_dir = self.PRACTICE_DIR / "session-briefs"
        brief_dir.mkdir(parents=True, exist_ok=True)

        brief_file = brief_dir / f"{brief['session_id']}.json"
        with open(brief_file, 'w') as f:
            json.dump(brief, f, indent=2)

    def format_for_claude(self, brief: dict) -> str:
        """
        Format brief as initial message to Claude.
        This is what gets pasted into claude.ai chat.
        """
        failures_text = ""
        if brief["real_failures"]:
            failures_text = "\n\n**Recent failures on this topic:**\n"
            for i, failure in enumerate(brief["real_failures"], 1):
                failures_text += (
                    f"{i}. [{failure['date']}] {failure['description']}\n"
                )

        implementation_failure_text = ""
        impl_failure = brief.get("implementation_failure")
        if impl_failure:
            implementation_failure_text = (
                f"\n\n**Implementation failure from yesterday's Session 6:**\n"
                f"{impl_failure['failure_details']}\n"
                f"This needs to be addressed in today's accountability phase.\n"
            )

        message = f"""# Learning Session {brief['session_id']}

**Domain:** {brief['domain']}
**Week:** {brief['week']}
**Topic:** {brief['topic']}
**Session Type:** {brief['session_type']}

---

## SESSION STRUCTURE (20 minutes)

**Minutes 0-2: OPEN**
{brief['agenda']['open']}

**Minutes 2-7: ACCOUNTABILITY**
{brief['agenda']['accountability']}
{implementation_failure_text}

**Minutes 7-15: LESSON**
{brief['agenda']['lesson']}
{failures_text}

**Minutes 15-17: READING/RESEARCH ASSIGNMENT**
{brief['agenda']['assignment']}

**Minutes 17-19: TEACH BACK**
{brief['teach_back_prompt']}

**Minutes 19-20: CLOSE**
{brief['reasoning_prompt']}

Write claude-summary.md with:
1. What we covered
2. Key insights
3. Your reasoning (WHY section)
4. What bee should practice before next session

I will write bee-notes.md with my understanding.

---

Ready to begin.
"""

        return message
