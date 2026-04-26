"""
Blueprint Tool - Claude API integration for path recommendations

Generates 3 structured implementation paths for user ideas.
Returns JSON with recommended path, pros/cons, tech approach, complexity.
"""

import os
import json
from typing import Dict, List, Any
import anthropic


async def generate_blueprint_paths(idea: str, features: List[str]) -> Dict[str, Any]:
    """
    Generate 3 implementation path recommendations for a given idea.

    Args:
        idea: Core idea description from user
        features: List of must-have feature bullet points

    Returns:
        {
            "ok": bool,
            "data": {
                "recommended": int,  # 0, 1, or 2 - which path is recommended
                "paths": [
                    {
                        "id": int,
                        "name": str,
                        "tagline": str,
                        "why_recommended": str,
                        "pros": List[str],
                        "cons": List[str],
                        "tech_approach": str,
                        "time_estimate": str,
                        "complexity": str  # "Simple", "Moderate", or "Complex"
                    }
                ],
                "bee_note": str  # Personal note from Worker Bee
            },
            "error": str  # Only present if ok=False
        }
    """

    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {
            "ok": False,
            "error": "ANTHROPIC_API_KEY not found in environment"
        }

    try:
        client = anthropic.Anthropic(api_key=api_key)

        # Format features as bullet list
        features_list = "\n".join([f"- {f}" for f in features]) if features else "No specific features listed"

        # System prompt forces JSON-only response with strict schema
        system_prompt = """You are Worker Bee's path recommendation engine.

Given a user's core idea and must-have features, generate exactly 3 implementation paths.

CRITICAL RULES:
1. Return ONLY valid JSON - no markdown, no explanations, just the JSON object
2. Exactly 3 paths, ordered from simplest to most complex
3. One path MUST be recommended (set recommended: 0, 1, or 2)
4. Complexity must be exactly "Simple", "Moderate", or "Complex"
5. Time estimates realistic (hours/days/weeks format)
6. Pros and cons must be specific, not generic
7. Tech approach describes the stack and architecture briefly

JSON SCHEMA (return this exact structure):
{
  "recommended": 0,
  "paths": [
    {
      "id": 0,
      "name": "Quick & Minimal",
      "tagline": "Get it working fast with essential features only",
      "why_recommended": "Why this path makes sense for this specific idea",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "tech_approach": "Brief description of stack and architecture",
      "time_estimate": "1-2 days",
      "complexity": "Simple"
    },
    {
      "id": 1,
      "name": "Balanced Build",
      "tagline": "Solid foundation with room to grow",
      "why_recommended": "Why this path makes sense for this specific idea",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "tech_approach": "Brief description of stack and architecture",
      "time_estimate": "3-5 days",
      "complexity": "Moderate"
    },
    {
      "id": 2,
      "name": "Production-Ready",
      "tagline": "Enterprise-grade with all the features",
      "why_recommended": "Why this path makes sense for this specific idea",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "tech_approach": "Brief description of stack and architecture",
      "time_estimate": "1-2 weeks",
      "complexity": "Complex"
    }
  ],
  "bee_note": "Personal note from Worker Bee about this idea (1-2 sentences, warm colleague tone)"
}

REMEMBER: Return ONLY the JSON object. No markdown code blocks, no explanations."""

        user_prompt = f"""Core Idea:
{idea}

Must-Have Features:
{features_list}

Generate 3 implementation paths for this idea. Return only the JSON object."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        # Extract JSON from response
        response_text = response.content[0].text.strip()

        # Remove markdown code blocks if present (Claude sometimes adds them despite instructions)
        if response_text.startswith("```"):
            # Find the actual JSON content between code blocks
            lines = response_text.split("\n")
            json_lines = []
            in_code_block = False
            for line in lines:
                if line.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block or not line.startswith("```"):
                    json_lines.append(line)
            response_text = "\n".join(json_lines).strip()

        # Parse JSON response
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            return {
                "ok": False,
                "error": f"Claude returned invalid JSON: {str(e)}\nResponse: {response_text[:200]}"
            }

        # Validate schema
        if "paths" not in data or "recommended" not in data:
            return {
                "ok": False,
                "error": "Claude response missing required fields (paths, recommended)"
            }

        if len(data["paths"]) != 3:
            return {
                "ok": False,
                "error": f"Expected 3 paths, got {len(data['paths'])}"
            }

        # Validate each path has required fields
        required_fields = ["id", "name", "tagline", "why_recommended", "pros", "cons", "tech_approach", "time_estimate", "complexity"]
        for i, path in enumerate(data["paths"]):
            for field in required_fields:
                if field not in path:
                    return {
                        "ok": False,
                        "error": f"Path {i} missing required field: {field}"
                    }

            # Validate complexity is one of the allowed values
            if path["complexity"] not in ["Simple", "Moderate", "Complex"]:
                return {
                    "ok": False,
                    "error": f"Path {i} has invalid complexity: {path['complexity']} (must be Simple, Moderate, or Complex)"
                }

        # Validate recommended index
        if not isinstance(data["recommended"], int) or data["recommended"] not in [0, 1, 2]:
            return {
                "ok": False,
                "error": f"Invalid recommended index: {data['recommended']} (must be 0, 1, or 2)"
            }

        return {
            "ok": True,
            "data": data
        }

    except anthropic.APIError as e:
        return {
            "ok": False,
            "error": f"Anthropic API error: {str(e)}"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": f"Unexpected error: {str(e)}"
        }
