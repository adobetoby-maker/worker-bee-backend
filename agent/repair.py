import httpx, json, os, asyncio, pathlib, sys

OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL  = os.getenv("DEFAULT_MODEL", "qwen2.5-coder:32b")
ROOT   = pathlib.Path.home() / "worker-bee"

WATCHED_FILES = [
    "main.py", "agent/runner.py",
    "agent/tools/browser.py",
    "agent/tools/filesystem.py",
    "agent/tools/shell.py",
    "agent/tools/memory.py",
    "agent/tools/planner.py",
    "agent/tools/github.py",
    "agent/tools/gmail.py",
    "agent/repair.py",
]

async def read_files() -> str:
    out = []
    for f in WATCHED_FILES:
        p = ROOT / f
        if p.exists():
            out.append(f"\n--- {f} ---\n{p.read_text()}")
    return "\n".join(out)

async def read_logs() -> str:
    log = pathlib.Path("/tmp/workerbee-error.log")
    if log.exists():
        return "\n".join(log.read_text().strip().split("\n")[-50:])
    return "No error log found"

async def ask_qwen(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(f"{OLLAMA}/api/chat", json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        })
        return r.json().get("message", {}).get("content", "")

async def apply_fix(filename: str, new_content: str):
    p = ROOT / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        (ROOT / f"{filename}.backup").write_text(p.read_text())
    p.write_text(new_content)
    print(f"Applied fix to {filename}")

async def extract_files_from_response(response: str) -> dict:
    fixes = {}
    lines = response.split("\n")
    current_file = None
    current_content = []
    for line in lines:
        if line.startswith("=== ") and line.endswith(" ===") and "end" not in line:
            current_file = line[4:-4].strip()
            current_content = []
        elif line == "=== end ===" and current_file:
            fixes[current_file] = "\n".join(current_content)
            current_file = None
            current_content = []
        elif current_file:
            current_content.append(line)
    return fixes

async def self_repair(error_description: str, ws=None):
    async def log(msg):
        print(msg)
        if ws:
            await ws.send_text(json.dumps({"type": "repair_log", "data": msg}))

    await log("SELF-REPAIR INITIATED")
    await log(f"Error: {error_description[:200]}")
    await log("Reading current agent files...")
    files = await read_files()
    await log("Reading error logs...")
    logs = await read_logs()

    prompt = f"""You are Worker Bee's self-repair system.
ERROR: {error_description}
LOGS: {logs}
FILES: {files}

Output ONLY files that need fixing in this format:
=== agent/tools/browser.py ===
<complete fixed file>
=== end ===

No explanation. Production ready Python only."""

    await log("Asking qwen to diagnose and fix...")
    response = await ask_qwen(prompt)
    await log(f"Got response ({len(response)} chars)")
    fixes = await extract_files_from_response(response)

    if not fixes:
        await log("No fixes found in response")
        return False

    await log(f"Fixing: {list(fixes.keys())}")
    for filename, content in fixes.items():
        if any(filename == f for f in WATCHED_FILES):
            await apply_fix(filename, content)
            await log(f"Fixed: {filename}")

    await log("Triggering reload...")
    (ROOT / "main.py").touch()
    await log("SELF-REPAIR COMPLETE — reconnecting in 3s")
    return True

if __name__ == "__main__":
    error = " ".join(sys.argv[1:]) or "General error"
    asyncio.run(self_repair(error))
