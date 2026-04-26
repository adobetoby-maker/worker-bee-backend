"""
30-Day Curriculum Template — Month 1

UPDATED PATTERN:
- Odd sessions (1, 3, 5...): Deepen existing skills
- Even sessions (2, 4, 6...): Introduce NEW skills from ClawHub candidates

Six domains, four weeks each.
Each week has specific topic and focus.
Real failures from practice logs inform every lesson.
"""

CURRICULUM_MONTH_1 = {
    "month": 1,
    "session_pattern": {
        "odd_sessions": {
            "type": "deepen",
            "description": "Deepen understanding of existing Worker Bee skills",
            "source": "manifests/skill-*.md files",
            "approach": "Practice with real failures from .practice.md logs"
        },
        "even_sessions": {
            "type": "introduce",
            "description": "Introduce NEW skills from ClawHub candidates",
            "source": "clawhub_skill_candidates (below)",
            "approach": "Teach new capability, show example, practice immediately"
        }
    },
    "domains": [
        {
            "id": "conversation_communication",
            "name": "Conversation & Communication",
            "weeks": [
                {
                    "week": 1,
                    "topic": "understanding_intent",
                    "focus": "Distinguish explicit vs implicit requirements",
                    "real_failures_source": "skill-planner.practice.md"
                },
                {
                    "week": 2,
                    "topic": "clarifying_questions",
                    "focus": "When to ask, what to ask, how to ask",
                    "real_failures_source": "SESSIONS.md"
                },
                {
                    "week": 3,
                    "topic": "saying_i_dont_know",
                    "focus": "Escalation without hallucination",
                    "real_failures_source": "skill-reviewer.practice.md"
                },
                {
                    "week": 4,
                    "topic": "email_workflow",
                    "focus": "Draft, refine, approval gate protocol",
                    "real_failures_source": "skill-sender.practice.md"
                }
            ]
        },
        {
            "id": "visual_generative",
            "name": "Visual & Generative",
            "weeks": [
                {
                    "week": 1,
                    "topic": "image_analysis",
                    "focus": "What to look for first in screenshots",
                    "real_failures_source": "skill-checker.practice.md"
                },
                {
                    "week": 2,
                    "topic": "image_generation",
                    "focus": "Precise prompt writing for image tools",
                    "real_failures_source": "skill-image-gen.practice.md"
                },
                {
                    "week": 3,
                    "topic": "web_design_aesthetics",
                    "focus": "Modern UI/UX patterns and distinctive design",
                    "real_failures_source": "skill-web-architect.practice.md"
                },
                {
                    "week": 4,
                    "topic": "visual_self_review",
                    "focus": "Checking own visual output before shipping",
                    "real_failures_source": "skill-checker.practice.md"
                }
            ]
        },
        {
            "id": "file_document",
            "name": "File & Document Processing",
            "weeks": [
                {
                    "week": 1,
                    "topic": "structure_extraction",
                    "focus": "Finding patterns in unstructured documents",
                    "real_failures_source": "skill-memory.practice.md"
                },
                {
                    "week": 2,
                    "topic": "ocr_handling",
                    "focus": "ime-coach specific OCR patterns",
                    "real_failures_source": "SESSIONS.md"
                },
                {
                    "week": 3,
                    "topic": "medical_legal_documents",
                    "focus": "Recognizing document types and extracting key fields",
                    "real_failures_source": "skill-memory.practice.md"
                },
                {
                    "week": 4,
                    "topic": "clean_document_output",
                    "focus": "Formatting for professional delivery",
                    "real_failures_source": "skill-reporter.practice.md"
                }
            ]
        },
        {
            "id": "code_repair",
            "name": "Code & Repair",
            "weeks": [
                {
                    "week": 1,
                    "topic": "read_before_fixing",
                    "focus": "Never guess - always read the actual code first",
                    "real_failures_source": "skill-builder-fixer-deploy.practice.md"
                },
                {
                    "week": 2,
                    "topic": "root_cause_vs_symptom",
                    "focus": "Diagnosing the real problem, not just surface errors",
                    "real_failures_source": "skill-repair-pipeline.practice.md"
                },
                {
                    "week": 3,
                    "topic": "systematic_debugging",
                    "focus": "5-phase protocol: Context Recall → Investigation → Pattern → Hypothesis → Implementation",
                    "real_failures_source": "skill-repair-pipeline.practice.md"
                },
                {
                    "week": 4,
                    "topic": "regression_testing",
                    "focus": "Did fixing X break Y?",
                    "real_failures_source": "skill-checker.practice.md"
                }
            ]
        },
        {
            "id": "decision_integrity",
            "name": "Decision & Integrity",
            "weeks": [
                {
                    "week": 1,
                    "topic": "escalation_threshold",
                    "focus": "When to escalate vs when to attempt",
                    "real_failures_source": "JOURNAL.md"
                },
                {
                    "week": 2,
                    "topic": "hallucination_avoidance",
                    "focus": "What I can state as fact vs what I must verify",
                    "real_failures_source": "JOURNAL.md"
                },
                {
                    "week": 3,
                    "topic": "self_review_protocol",
                    "focus": "Two lenses: did it work + was it right",
                    "real_failures_source": "skill-reviewer.practice.md"
                },
                {
                    "week": 4,
                    "topic": "confidence_calibration",
                    "focus": "Knowing what you know vs what you think you know",
                    "real_failures_source": "PRACTICE.md"
                }
            ]
        },
        {
            "id": "integration_seo_automation",
            "name": "Integration, SEO & Automation",
            "weeks": [
                {
                    "week": 1,
                    "topic": "seo_optimization",
                    "focus": "Audit, fix, validate - systematic SEO workflow",
                    "real_failures_source": "skill-seo.practice.md"
                },
                {
                    "week": 2,
                    "topic": "browser_automation",
                    "focus": "Ref-based element selection and testing workflows",
                    "real_failures_source": "skill-navigator.practice.md"
                },
                {
                    "week": 3,
                    "topic": "full_pipeline",
                    "focus": "Conversation to delivery without gaps",
                    "real_failures_source": "SESSIONS.md"
                },
                {
                    "week": 4,
                    "topic": "teach_back_mastery",
                    "focus": "Explain everything simply enough to teach others",
                    "real_failures_source": "PRACTICE.md"
                }
            ]
        }
    ],
    "clawhub_skill_candidates": {
        "description": "New skills from ClawHub to introduce in EVEN sessions",
        "rotation_strategy": "Introduce one per even session, cycling through categories",
        "categories": [
            {
                "category": "seo_content",
                "skills": [
                    {
                        "slug": "copywriting",
                        "name": "Copywriting & Persuasive Writing",
                        "teach_priority": 1,
                        "why": "Essential for landing pages, email campaigns, marketing content",
                        "practice_task": "Write a landing page hero section with AIDA framework"
                    },
                    {
                        "slug": "content-strategy",
                        "name": "Content Strategy",
                        "teach_priority": 2,
                        "why": "Plan content calendars, topic selection, audience targeting",
                        "practice_task": "Create a 30-day content calendar for a business blog"
                    }
                ]
            },
            {
                "category": "debugging_advanced",
                "skills": [
                    {
                        "slug": "gstack-openclaw-investigate",
                        "name": "Garry Tan's Debugging Framework",
                        "teach_priority": 1,
                        "why": "Alternative systematic debugging from Y Combinator CEO",
                        "practice_task": "Debug a sample bug using gstack 4-phase protocol"
                    }
                ]
            },
            {
                "category": "browser_testing",
                "skills": [
                    {
                        "slug": "browser-automation",
                        "name": "Stagehand Browser Automation",
                        "teach_priority": 2,
                        "why": "Natural language browser automation (simpler than refs)",
                        "practice_task": "Write a natural language test for a contact form"
                    }
                ]
            },
            {
                "category": "email_marketing",
                "skills": [
                    {
                        "slug": "email-marketing",
                        "name": "Email Marketing & Deliverability",
                        "teach_priority": 1,
                        "why": "Advanced email strategy, A/B testing, segmentation",
                        "practice_task": "Design a 5-email welcome sequence with segmentation"
                    },
                    {
                        "slug": "cold-email-writer",
                        "name": "Cold Email Writing",
                        "teach_priority": 2,
                        "why": "4-line framework for cold outreach",
                        "practice_task": "Write a cold email for new client outreach"
                    }
                ]
            },
            {
                "category": "design_architecture",
                "skills": [
                    {
                        "slug": "frontend-design-3",
                        "name": "Distinctive Frontend Design",
                        "teach_priority": 1,
                        "why": "Avoid generic AI aesthetics, bold design choices",
                        "practice_task": "Design a landing page with distinctive aesthetic direction"
                    },
                    {
                        "slug": "architecture-patterns",
                        "name": "Backend Architecture Patterns",
                        "teach_priority": 2,
                        "why": "Clean Architecture, Hexagonal, DDD patterns",
                        "practice_task": "Design a repository pattern for user management"
                    }
                ]
            },
            {
                "category": "social_automation",
                "skills": [
                    {
                        "slug": "social-media-automation",
                        "name": "Social Media Automation",
                        "teach_priority": 3,
                        "why": "Multi-platform posting, scheduling, analytics",
                        "practice_task": "Plan a week of social media posts with scheduling"
                    }
                ]
            }
        ],
        "pending_upgrades": {
            "description": "Skills with better ClawHub versions (flagged after 50 practice sessions)",
            "check_after_sessions": 50,
            "upgrade_workflow": [
                "Search ClawHub for [skill-name] + variations",
                "Inspect top 3 results (clawhub inspect --file SKILL.md)",
                "Compare against current manifests/skill-X.md",
                "If ClawHub version better: save to pending/ with comparison notes",
                "Flag in morning report for Toby review"
            ],
            "skills_to_check": []
        }
    },
    "session_structure": {
        "duration_minutes": 20,
        "phases": [
            {"phase": "open", "minutes": 2, "content": "Upload previous notes, accountability"},
            {"phase": "accountability", "minutes": 5, "content": "Claude tests last session"},
            {"phase": "lesson", "minutes": 8, "content": "Today's topic, back-and-forth"},
            {"phase": "assignment", "minutes": 2, "content": "Specific research task"},
            {"phase": "teach_back", "minutes": 2, "content": "Bee explains to Claude"},
            {"phase": "close", "minutes": 1, "content": "Write notes, reasoning transfer"}
        ],
        "even_session_structure": {
            "description": "Modified structure for introducing NEW skills",
            "phases": [
                {"phase": "open", "minutes": 2, "content": "Upload previous notes, acknowledge pattern"},
                {"phase": "new_skill_intro", "minutes": 10, "content": "Claude teaches NEW skill from ClawHub"},
                {"phase": "immediate_practice", "minutes": 5, "content": "Bee practices the new skill"},
                {"phase": "teach_back", "minutes": 2, "content": "Bee explains new skill to Claude"},
                {"phase": "close", "minutes": 1, "content": "Write notes, add to rotation"}
            ]
        }
    },
    "daily_schedule": [
        {"time": "09:00", "session_type": "teach", "session_num": 1, "pattern": "odd"},
        {"time": "11:00", "session_type": "introduce", "session_num": 2, "pattern": "even"},
        {"time": "13:00", "session_type": "teach", "session_num": 3, "pattern": "odd"},
        {"time": "15:00", "session_type": "introduce", "session_num": 4, "pattern": "even"},
        {"time": "17:00", "session_type": "teach", "session_num": 5, "pattern": "odd"},
        {"time": "18:00", "session_type": "introduce", "session_num": 6, "pattern": "even"}
    ],
    "teach_back_rubric": {
        "accuracy": {
            "1-3": "Fundamentally wrong or missing key concepts",
            "4-6": "Partially correct but significant gaps",
            "7-8": "Mostly correct with minor errors",
            "9-10": "Perfectly accurate"
        },
        "clarity": {
            "1-3": "Confusing, phi4 couldn't follow",
            "4-6": "Understandable but requires effort",
            "7-8": "Clear and easy to follow",
            "9-10": "Crystal clear, could teach from this"
        },
        "completeness": {
            "1-3": "Missed most key points",
            "4-6": "Covered some but not all important points",
            "7-8": "Covered nearly everything important",
            "9-10": "Comprehensive, nothing missing"
        },
        "passing_threshold": 7.0
    }
}


def get_session_type(session_number: int) -> dict:
    """
    Determine session type based on session number.

    Odd sessions: Deepen existing skills
    Even sessions: Introduce new skills from ClawHub
    """
    is_even = session_number % 2 == 0

    if is_even:
        return {
            "type": "introduce",
            "structure": CURRICULUM_MONTH_1["session_structure"]["even_session_structure"],
            "skill_source": "clawhub_skill_candidates",
            "goal": "Learn one new skill from ClawHub, practice immediately"
        }
    else:
        return {
            "type": "deepen",
            "structure": CURRICULUM_MONTH_1["session_structure"],
            "skill_source": "existing Worker Bee skills",
            "goal": "Deepen understanding through real failure analysis"
        }


def get_next_clawhub_skill(session_number: int) -> dict:
    """
    Get the next ClawHub skill to introduce.
    Cycles through categories, prioritizing by teach_priority.
    """
    categories = CURRICULUM_MONTH_1["clawhub_skill_candidates"]["categories"]

    # Count even sessions to determine which skill to teach
    even_session_count = (session_number // 2)

    # Flatten all skills with priorities
    all_skills = []
    for category in categories:
        for skill in category["skills"]:
            all_skills.append({
                **skill,
                "category": category["category"]
            })

    # Sort by priority
    all_skills.sort(key=lambda x: x["teach_priority"])

    # Get skill for this session (cycle if we run out)
    skill_index = (even_session_count - 1) % len(all_skills)
    return all_skills[skill_index]
