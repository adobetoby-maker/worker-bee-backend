/**
 * Blueprint Path Generator - Claude API Integration
 *
 * Generates 3 distinct implementation paths for user ideas.
 * Uses Claude Sonnet 4 to analyze idea + features and recommend approaches.
 */

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || ""
});

export interface BlueprintPath {
  id: string;
  name: string;
  tagline: string;
  why_recommended: string;
  pros: string[];
  cons: string[];
  tech_approach: string;
  time_estimate: string;
  complexity: "Simple" | "Moderate" | "Complex";
}

export interface BlueprintData {
  recommended: string;
  paths: BlueprintPath[];
  bee_note: string;
}

export interface BlueprintResult {
  ok: boolean;
  data?: BlueprintData;
  error?: string;
}

const SYSTEM_PROMPT = `You are Blueprint, Worker Bee's strategic planning mode.

Your job: Read the user's core idea and must-have features, then generate exactly 3 distinct implementation paths.

CRITICAL RULES:
1. Respond ONLY with valid JSON — no markdown, no preamble, no explanation, nothing outside the JSON object
2. Exactly 3 paths, ordered from simplest to most complex
3. Paths must be genuinely different approaches, not just variations in scope
4. One path MUST be recommended (set "recommended" to 0, 1, or 2)
5. Be specific to THIS idea — no generic advice
6. Complexity must be exactly "Simple", "Moderate", or "Complex"
7. Time estimates must be realistic (format: "2-3 hours", "1-2 days", "1 week", etc.)
8. Pros and cons must be specific to the idea, not generic platitudes

JSON SCHEMA (return exactly this structure):
{
  "recommended": "0",
  "paths": [
    {
      "id": "0",
      "name": "Quick & Minimal",
      "tagline": "One sentence describing this approach",
      "why_recommended": "2-3 sentences explaining why this path makes sense FOR THIS SPECIFIC IDEA",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "tech_approach": "2-3 sentences describing the tech stack and architecture",
      "time_estimate": "2-3 hours",
      "complexity": "Simple"
    },
    {
      "id": "1",
      "name": "Balanced Build",
      "tagline": "One sentence describing this approach",
      "why_recommended": "2-3 sentences explaining why this path makes sense FOR THIS SPECIFIC IDEA",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "tech_approach": "2-3 sentences describing the tech stack and architecture",
      "time_estimate": "1-2 days",
      "complexity": "Moderate"
    },
    {
      "id": "2",
      "name": "Production-Ready",
      "tagline": "One sentence describing this approach",
      "why_recommended": "2-3 sentences explaining why this path makes sense FOR THIS SPECIFIC IDEA",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "tech_approach": "2-3 sentences describing the tech stack and architecture",
      "time_estimate": "1-2 weeks",
      "complexity": "Complex"
    }
  ],
  "bee_note": "One honest sentence from Worker Bee about the most important thing to get right with this idea"
}

TONE: You're a warm, experienced colleague who's built things before. Be honest about tradeoffs. Don't oversell or undersell. Help them pick the right path for their context.

REMEMBER: Return ONLY the JSON object. No markdown code blocks. No explanations. Just pure JSON.`;

export async function generateBlueprintPaths(
  idea: string,
  features: string[]
): Promise<BlueprintResult> {
  // Validate API key
  if (!process.env.ANTHROPIC_API_KEY) {
    return {
      ok: false,
      error: "ANTHROPIC_API_KEY not configured. Add it to ~/worker-bee/.env"
    };
  }

  // Validate inputs
  if (!idea || idea.trim().length === 0) {
    return {
      ok: false,
      error: "Core idea cannot be empty"
    };
  }

  try {
    // Format features as bullet list
    const featuresText =
      features && features.length > 0
        ? features.map((f) => `- ${f.trim()}`).join("\n")
        : "- No specific features listed";

    const userPrompt = `Project Idea:
${idea.trim()}

Must-Have Features:
${featuresText}

Generate 3 distinct implementation paths for this idea. Return only the JSON object.`;

    // Call Claude API
    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 4096,
      system: SYSTEM_PROMPT,
      messages: [
        {
          role: "user",
          content: userPrompt
        }
      ]
    });

    // Extract response text
    const firstBlock = response.content[0];
    if (firstBlock.type !== "text") {
      return {
        ok: false,
        error: "Claude returned non-text response"
      };
    }
    const responseText = firstBlock.text.trim();

    // Remove markdown code blocks if present (Claude sometimes adds them despite instructions)
    let cleanedResponse = responseText;
    if (responseText.startsWith("```")) {
      const lines = responseText.split("\n");
      const jsonLines: string[] = [];
      let inCodeBlock = false;

      for (const line of lines) {
        if (line.startsWith("```")) {
          inCodeBlock = !inCodeBlock;
          continue;
        }
        if (inCodeBlock || !line.startsWith("```")) {
          jsonLines.push(line);
        }
      }
      cleanedResponse = jsonLines.join("\n").trim();
    }

    // Parse JSON response
    let data: any;
    try {
      data = JSON.parse(cleanedResponse);
    } catch (parseError) {
      return {
        ok: false,
        error: `Claude returned invalid JSON. Parse error: ${parseError instanceof Error ? parseError.message : String(parseError)}\n\nResponse preview: ${cleanedResponse.substring(0, 200)}...`
      };
    }

    // Validate schema
    if (typeof data !== "object" || data === null) {
      return {
        ok: false,
        error: "Claude response is not a valid JSON object"
      };
    }

    if (!("paths" in data)) {
      return {
        ok: false,
        error: "Claude response missing 'paths' field"
      };
    }

    if (!("recommended" in data)) {
      return {
        ok: false,
        error: "Claude response missing 'recommended' field"
      };
    }

    if (!Array.isArray(data.paths)) {
      return {
        ok: false,
        error: "'paths' field must be an array"
      };
    }

    if (data.paths.length !== 3) {
      return {
        ok: false,
        error: `Expected exactly 3 paths, got ${data.paths.length}`
      };
    }

    // Validate recommended index
    if (
      typeof data.recommended !== "string" ||
      !["0", "1", "2"].includes(data.recommended)
    ) {
      return {
        ok: false,
        error: `Invalid 'recommended' value: ${data.recommended} (must be "0", "1", or "2")`
      };
    }

    // Validate each path has required fields
    const requiredFields = [
      "id",
      "name",
      "tagline",
      "why_recommended",
      "pros",
      "cons",
      "tech_approach",
      "time_estimate",
      "complexity"
    ];

    for (let i = 0; i < data.paths.length; i++) {
      const path = data.paths[i];

      for (const field of requiredFields) {
        if (!(field in path)) {
          return {
            ok: false,
            error: `Path ${i} missing required field: '${field}'`
          };
        }
      }

      // Validate complexity is one of the allowed values
      if (!["Simple", "Moderate", "Complex"].includes(path.complexity)) {
        return {
          ok: false,
          error: `Path ${i} has invalid complexity: '${path.complexity}' (must be 'Simple', 'Moderate', or 'Complex')`
        };
      }

      // Validate pros and cons are arrays
      if (!Array.isArray(path.pros)) {
        return {
          ok: false,
          error: `Path ${i} 'pros' must be an array`
        };
      }

      if (!Array.isArray(path.cons)) {
        return {
          ok: false,
          error: `Path ${i} 'cons' must be an array`
        };
      }

      // Validate id matches index (as string)
      if (path.id !== String(i)) {
        return {
          ok: false,
          error: `Path ${i} has mismatched id: ${path.id} (should be "${i}")`
        };
      }
    }

    // Validate bee_note exists
    if (!("bee_note" in data) || typeof data.bee_note !== "string") {
      return {
        ok: false,
        error: "Missing or invalid 'bee_note' field"
      };
    }

    // All validation passed - return successful result
    return {
      ok: true,
      data: data as BlueprintData
    };

  } catch (error) {
    // Handle API errors
    if (error instanceof Anthropic.APIError) {
      return {
        ok: false,
        error: `Claude API error: ${error.message}`
      };
    }

    // Handle unexpected errors
    return {
      ok: false,
      error: `Unexpected error: ${error instanceof Error ? error.message : String(error)}`
    };
  }
}
