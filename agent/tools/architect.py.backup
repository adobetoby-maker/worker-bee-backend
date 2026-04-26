import httpx
import pathlib
from datetime import datetime
from dotenv import dotenv_values

_env = dotenv_values(str(pathlib.Path.home() / "worker-bee" / ".env"))
OLLAMA        = _env.get("OLLAMA_HOST", "http://localhost:11434")
ANTHROPIC_KEY = _env.get("ANTHROPIC_API_KEY", "")

# ── Token tracking ────────────────────────────────────────
session_tokens = {
    "input": 0,
    "output": 0,
    "calls": 0,
    "cost_usd": 0.0,
    "history": []
}

CLAUDE_INPUT_COST  = 3.00 / 1_000_000   # $3 per million input tokens
CLAUDE_OUTPUT_COST = 15.00 / 1_000_000  # $15 per million output tokens

def record_usage(input_tokens: int, output_tokens: int, prompt_preview: str = ""):
    cost = (input_tokens * CLAUDE_INPUT_COST) + (output_tokens * CLAUDE_OUTPUT_COST)
    session_tokens["input"]    += input_tokens
    session_tokens["output"]   += output_tokens
    session_tokens["calls"]    += 1
    session_tokens["cost_usd"] += cost
    session_tokens["history"].append({
        "time":           datetime.now().isoformat(),
        "input_tokens":   input_tokens,
        "output_tokens":  output_tokens,
        "cost_usd":       round(cost, 6),
        "prompt_preview": prompt_preview[:80]
    })
    return {
        "input_tokens":   input_tokens,
        "output_tokens":  output_tokens,
        "cost_usd":       round(cost, 6),
        "session_total":  round(session_tokens["cost_usd"], 4),
        "session_calls":  session_tokens["calls"]
    }

def get_session_stats() -> dict:
    return {
        "input_tokens":  session_tokens["input"],
        "output_tokens": session_tokens["output"],
        "total_tokens":  session_tokens["input"] + session_tokens["output"],
        "calls":         session_tokens["calls"],
        "cost_usd":      round(session_tokens["cost_usd"], 4),
        "history":       session_tokens["history"]
    }

def reset_session():
    session_tokens["input"]    = 0
    session_tokens["output"]   = 0
    session_tokens["calls"]    = 0
    session_tokens["cost_usd"] = 0.0
    session_tokens["history"]  = []

# ── System prompts ────────────────────────────────────────
ARCHITECT_PROMPT = """You are the Worker Bee Architect — world-class UI/UX designer and frontend engineer.

Your job is to write a precise technical brief for qwen2.5-coder to execute.
qwen is excellent at following specs but has NO design sense on its own.

Output a TECHNICAL BRIEF with:
## COMPONENT STRUCTURE — every component needed
## DESIGN SYSTEM — exact colors, typography, spacing, shadows
## MXUX ELEMENTS — gradient mesh, glass cards, animations, 3D effects
## RESPONSIVE BEHAVIOR — exact breakpoints
## COMPONENT SPECS — exact implementation for each component
## TAILWIND CLASSES — key classes to use
## FILE STRUCTURE — exact files to create

Be extremely specific. Leave nothing to interpretation."""

ARCHITECT_PROMPT_FAST = """Write a precise technical UI brief for qwen to execute.
Be specific about colors, spacing, animations, and component structure.
Output only the brief, no explanation."""

# ── Local architect (deepseek or phi4) ───────────────────
async def architect_local(request: str, context: str = "", fast: bool = False) -> str:
    model  = "phi4:latest" if fast else "deepseek-r1:14b"
    system = ARCHITECT_PROMPT_FAST if fast else ARCHITECT_PROMPT
    prompt = request
    if context:
        prompt += f"\n\nCONTEXT:\n{context}"
    async with httpx.AsyncClient(timeout=300) as c:
        r = await c.post(f"{OLLAMA}/api/chat", json={
            "model":    model,
            "messages": [
                {"role": "system",  "content": system},
                {"role": "user",    "content": prompt}
            ],
            "stream": False
        })
        content = r.json().get("message", {}).get("content", "")
        if "<think>" in content:
            content = content.split("</think>")[-1].strip()
        return content

# ── Claude architect ──────────────────────────────────────
async def architect_claude(request: str, context: str = "") -> tuple[str, dict]:
    if not ANTHROPIC_KEY:
        result = await architect_local(request, context)
        return result, {}

    prompt = request
    if context:
        prompt += f"\n\nCONTEXT:\n{context}"

    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key":         ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type":      "application/json"
            },
            json={
                "model":      "claude-sonnet-4-5",
                "max_tokens": 4000,
                "system":     ARCHITECT_PROMPT,
                "messages":   [{"role": "user", "content": prompt}]
            }
        )
        data = r.json()

        if "content" not in data:
            # API error — fall back to local
            result = await architect_local(request, context)
            return result, {}

        text = data["content"][0].get("text", "")

        # Record token usage
        usage = data.get("usage", {})
        input_tokens  = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        token_stats   = record_usage(input_tokens, output_tokens, request)

        return text, token_stats

# ── Main entry point ──────────────────────────────────────
async def architect(
    request:    str,
    context:    str  = "",
    use_claude: bool = False,
    fast:       bool = False
) -> tuple[str, dict]:
    if use_claude and ANTHROPIC_KEY:
        return await architect_claude(request, context)
    result = await architect_local(request, context, fast)
    return result, {}
