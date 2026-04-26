import httpx, json, os, asyncio, pathlib
from datetime import datetime

OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ROOT   = pathlib.Path.home() / "worker-bee" / "projects"

class TaskPlanner:
    def __init__(self, runner=None):
        self.runner   = runner
        self.tasks    = []
        self.current  = 0
        self.running  = False
        self.paused   = False

    async def plan(self, goal: str) -> list:
        """
        Ask deepseek to break a goal into steps.
        Returns a list of actionable tasks.
        """
        prompt = f"""You are a task planner for Worker Bee, 
an AI agent with these tools:
  - browser: navigate, screenshot, scrape any URL
  - login: log into websites  
  - shell: run bash commands
  - file_read / file_write: manage project files
  - vision: analyze screenshots with llava
  - github: read/write GitHub repos
  - gmail: manage email inbox

GOAL: {goal}

Break this into 3-8 specific, executable steps.
Each step must be one of these action types:
  browser, login, shell, file_read, file_write, 
  vision, github, gmail, chat

Output ONLY valid JSON — no explanation:
{{
  "goal": "{goal}",
  "steps": [
    {{
      "id": 1,
      "action": "browser",
      "description": "Navigate to the target URL",
      "params": {{"url": "https://example.com"}},
      "depends_on": []
    }},
    {{
      "id": 2, 
      "action": "vision",
      "description": "Analyze the screenshot",
      "params": {{"question": "What do you see?"}},
      "depends_on": [1]
    }}
  ]
}}"""

        try:
            async with httpx.AsyncClient(timeout=60) as c:
                r = await c.post(
                    f"{OLLAMA}/api/chat",
                    json={
                        "model": "deepseek-r1:70b",
                        "messages": [{"role": "user",
                                      "content": prompt}],
                        "stream": False
                    }
                )
                content = r.json().get(
                    "message", {}).get("content", "")

                # Extract JSON from response
                # DeepSeek wraps in <think> blocks
                if "<think>" in content:
                    content = content.split(
                        "</think>")[-1].strip()

                # Find JSON block
                start = content.find("{")
                end   = content.rfind("}") + 1
                if start >= 0 and end > start:
                    data = json.loads(content[start:end])
                    self.tasks = data.get("steps", [])
                    return self.tasks

        except Exception as e:
            print(f"Plan error: {e}")

        return []

    async def execute(self, ws=None) -> dict:
        """
        Execute all planned tasks in order.
        Sends progress updates over WebSocket.
        """
        self.running = True
        self.current = 0
        results      = {}

        async def log(msg, level="info"):
            print(f"[PLANNER] {msg}")
            if ws:
                await ws.send_text(json.dumps({
                    "type": "plan_log",
                    "data": {"message": msg, "level": level}
                }))

        async def progress(step, status, result=None):
            if ws:
                await ws.send_text(json.dumps({
                    "type": "plan_progress",
                    "data": {
                        "step_id":   step["id"],
                        "status":    status,
                        "action":    step["action"],
                        "desc":      step["description"],
                        "result":    result,
                        "current":   self.current,
                        "total":     len(self.tasks)
                    }
                }))

        await log(f"Starting plan: {len(self.tasks)} steps")

        for step in self.tasks:
            if not self.running:
                await log("Plan stopped by user", "warn")
                break

            while self.paused:
                await asyncio.sleep(0.5)

            self.current = step["id"]
            await progress(step, "running")
            await log(
                f"Step {step['id']}/{len(self.tasks)}: "
                f"{step['description']}")

            result = None
            try:
                action = step["action"]
                params = step.get("params", {})

                # Inject results from previous steps
                for key, val in params.items():
                    if isinstance(val, str) and \
                       val.startswith("$step_"):
                        ref_id = int(val.replace("$step_",""))
                        params[key] = results.get(
                            ref_id, val)

                if action == "browser" and self.runner:
                    r = await self.runner.browser.navigate(
                        params.get("url", ""))
                    result = r

                elif action == "screenshot" and self.runner:
                    b64 = await self.runner.browser.screenshot(
                        params.get("url", ""))
                    result = {"screenshot_b64": b64}
                    if ws:
                        await ws.send_text(json.dumps({
                            "type": "screenshot",
                            "data": {
                                "url": params.get("url",""),
                                "screenshot_b64": b64
                            }
                        }))

                elif action == "vision" and self.runner:
                    b64 = params.get("screenshot_b64") or \
                          results.get(
                              step.get("depends_on",[None])[0],
                              {}).get("screenshot_b64","")
                    desc = await self.runner.vision_analyze(
                        b64,
                        params.get("question",
                                   "Describe what you see"))
                    result = {"description": desc}

                elif action == "shell" and self.runner:
                    r = await self.runner.shell.run(
                        params.get("command", ""))
                    result = r

                elif action == "file_write" and self.runner:
                    r = self.runner.fs.write(
                        params.get("path",""),
                        params.get("content",""))
                    result = {"written": r}

                elif action == "file_read" and self.runner:
                    content = self.runner.fs.read(
                        params.get("path",""))
                    result = {"content": content}

                elif action == "chat" and self.runner:
                    # Use the runner's chat capability
                    msg = {
                        "action": "chat",
                        "content": params.get("prompt",""),
                        "model": params.get(
                            "model", "qwen2.5-coder:32b")
                    }
                    # Capture the response
                    full = ""
                    saved_send = self.runner.send
                    async def capture_send(t, d):
                        nonlocal full
                        if t == "token":
                            full += d
                        elif t == "done":
                            pass
                        else:
                            await saved_send(t, d)
                    self.runner.send = capture_send
                    await self.runner.chat(msg)
                    self.runner.send = saved_send
                    result = {"response": full}

                elif action == "login" and self.runner:
                    r = await self.runner.browser.login(
                        url=params.get("url",""),
                        username=params.get("username",""),
                        password=params.get("password","")
                    )
                    result = r

                elif action == "gmail" and self.runner:
                    await self.runner.run_gmail({
                        "gmail_action": params.get(
                            "gmail_action","summary")
                    })
                    result = {"gmail": "done"}

                results[step["id"]] = result or {}
                await progress(step, "done", result)
                await log(
                    f"✅ Step {step['id']} complete", "ok")

            except Exception as e:
                await log(
                    f"❌ Step {step['id']} failed: {e}",
                    "error")
                await progress(step, "failed",
                               {"error": str(e)})
                results[step["id"]] = {"error": str(e)}

        self.running = False
        final = {
            "completed": len([r for r in results.values()
                              if "error" not in r]),
            "failed":    len([r for r in results.values()
                              if "error" in r]),
            "total":     len(self.tasks),
            "results":   results
        }
        await log(
            f"Plan complete: {final['completed']}"
            f"/{final['total']} steps succeeded")
        if ws:
            await ws.send_text(json.dumps({
                "type": "plan_complete",
                "data": final
            }))
        return final

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
