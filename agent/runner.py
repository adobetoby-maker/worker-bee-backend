import httpx, json, os, base64
from .tools.browser import BrowserTool
from .tools.filesystem import FilesystemTool
from .tools.shell import ShellTool
from .tools.memory import MemoryTool
from .tools.planner import TaskPlanner

OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL  = os.getenv("DEFAULT_MODEL", "phi4:latest")

# Context window sizes for RAM management
MODEL_CONTEXT_SIZES = {
    "qwen2.5-coder:32b": 20480,  # 20k for code generation
    "deepseek-r1:14b": 8192,      # 8k for planning briefs
    "deepseek-r1:32b": 8192,      # 8k for planning briefs
    "llava:latest": 8192,         # 8k for vision
    "qwen2.5vl:7b": 8192,        # 8k for vision
    "phi4:latest": 8192,          # 8k for routing
}

def get_num_ctx(model: str) -> int:
    """Get context window size for model, default to 8k if not specified"""
    return MODEL_CONTEXT_SIZES.get(model, 8192)

class ManifestLoader:
    MANIFEST_DIR = os.path.expanduser("~/worker-bee/manifests")
    _cache: dict = {}

    @classmethod
    def load(cls, name: str) -> str:
        if name in cls._cache:
            return cls._cache[name]
        search_paths = [
            os.path.join(cls.MANIFEST_DIR, f"{name}.md"),
            os.path.join(cls.MANIFEST_DIR, "shared", f"{name}.md"),
            os.path.join(cls.MANIFEST_DIR, "pipelines", "builder", f"{name}.md"),
            os.path.join(cls.MANIFEST_DIR, "pipelines", "tester", f"{name}.md"),
            os.path.join(cls.MANIFEST_DIR, "pipelines", "email", f"{name}.md"),
            os.path.join(cls.MANIFEST_DIR, "pipelines", "repair", f"{name}.md"),
        ]
        for path in search_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        content = f.read()
                    cls._cache[name] = content
                    return content
                except Exception:
                    pass
        return ""

    @classmethod
    def load_for_model(cls, model: str) -> str:
        model_map = {
            "phi4:latest":       "identity-phi4",
            "deepseek-r1:14b":   "identity-deepseek",
            "deepseek-r1:32b":   "identity-deepseek",
            "qwen2.5-coder:32b": "identity-qwen",
            "qwen2.5vl:7b":      "identity-qwen2.5vl",
        }
        identity_name = model_map.get(model, "")
        return cls.load(identity_name) if identity_name else ""

    @classmethod
    def clear_cache(cls):
        cls._cache = {}

    @classmethod
    def manifests_loaded(cls) -> bool:
        return os.path.exists(
            os.path.join(cls.MANIFEST_DIR, "00-getting-started.md"))


def pick_model(message: str) -> str:
    msg = message.lower()
    if any(w in msg for w in [
        "screenshot", "see ", "look at", "image", "visual",
        "what does it look", "show me", "analyze the page",
        "what do you see", "check the screen", "vision"
    ]):
        return "qwen2.5vl:7b"
    if any(w in msg for w in [
        "code", "build", "write a", "fix the", "debug",
        "html", "css", "javascript", "python", "function",
        "class", "component", "script", "lovable prompt",
        "react", "typescript", "install", "deploy", "create a",
        "generate", "refactor", "landing page", "website",
        "webpage", "navbar", "footer", "button", "form",
        "style", "animation"
    ]):
        return "qwen2.5-coder:32b"
    if any(w in msg for w in [
        "why ", "explain", "analyze", "diagnose", "architect",
        "strategy", "should i", "best way", "review", "audit",
        "plan", "compare", "difference between", "pros and cons",
        "recommend", "what would", "how would", "reason",
        "think through", "help me decide", "is it possible",
        "what is the best", "disconnect", "websocket",
        "timeout", "protocol", "architecture", "how does",
        "what causes", "deep dive", "thorough", "detailed",
        "comprehensive"
    ]):
        return "deepseek-r1:14b"
    return "phi4:latest"


def should_escalate_to_claude(message: str) -> bool:
    msg = message.lower()
    hard_triggers = [
        "teach worker bee", "add the ability to",
        "write a skill", "new skill file",
        "site architecture", "add to the system",
        "strategic", "going live", "clients will see",
    ]
    if any(t in msg for t in hard_triggers):
        return True
    score = 0
    for s in ["across all", "multiple sites", "architectural",
              "failed before", "keeps breaking", "restructure"]:
        if s in msg:
            score += 1
    for s in ["important", "jay needs", "client",
              "production", "urgent"]:
        if s in msg:
            score += 1
    for s in ["never done", "new kind", "different from",
              "haven't seen", "first time"]:
        if s in msg:
            score += 1
    return score >= 3


class AgentRunner:
    def __init__(self, tab_id: str, ws):
        self.tab_id      = tab_id
        self.ws          = ws
        self.model       = MODEL
        self.history     = []
        self.browser     = BrowserTool()
        self.fs          = FilesystemTool()
        self.shell       = ShellTool()
        self.memory      = MemoryTool(tab_id=tab_id)
        self.planner     = TaskPlanner(runner=self)
        self.error_count = 0
        self.MAX_ERRORS  = 3

    async def handle(self, msg: dict):
        a = msg.get("action")
        if   a == "chat":             await self.chat(msg)
        elif a == "browser":          await self.run_browser(msg)
        elif a == "shell":            await self.run_shell(msg)
        elif a == "vision":           await self.run_vision(msg)
        elif a == "login":            await self.run_login(msg)
        elif a == "gmail":            await self.run_gmail(msg)
        elif a == "get_tags":         await self.run_get_tags()
        elif a == "get_ps":           await self.run_get_ps()
        elif a == "github":           await self.run_github(msg)
        elif a == "self_repair":      await self.run_self_repair(msg)
        elif a == "file_read":
            try:
                await self.send("file_content", {
                    "path": msg["path"],
                    "content": self.fs.read(msg["path"])
                })
            except Exception as e:
                await self.send("error", str(e))
        elif a == "file_write":
            try:
                await self.send("file_written", {
                    "result": self.fs.write(msg["path"], msg["content"])
                })
            except Exception as e:
                await self.send("error", str(e))
        elif a == "plan":             await self.run_plan(msg)
        elif a == "plan_stop":        self.planner.stop()
        elif a == "plan_pause":       self.planner.pause()
        elif a == "plan_resume":      self.planner.resume()
        elif a == "memory_search":    await self.run_memory_search(msg)
        elif a == "memory_store":     await self.run_memory_store(msg)
        elif a == "memory_stats":     await self.run_memory_stats()
        elif a == "vision_report":    await self.run_vision_report(msg)
        elif a == "save_cookies":     await self.run_save_cookies(msg)
        elif a == "learn_now":        await self.run_learn_now(msg)
        elif a == "speak":            await self.run_speak(msg)
        elif a == "voice_input":      await self.run_voice_input(msg)
        elif a == "voice_transcribe": await self.run_voice_transcribe(msg)
        elif a == "index_site":       await self.run_index_site(msg)
        elif a == "build":            await self.run_build(msg)
        elif a == "build_start":      await self.run_build_start(msg)
        elif a == "dev_server_start": await self.run_dev_server(msg)
        elif a == "dev_server_stop":  await self.run_dev_server_stop(msg)
        elif a == "scaffold":         await self.run_scaffold(msg)
        elif a == "list_projects":    await self.run_list_projects()
        elif a == "reload_manifests":
            ManifestLoader.clear_cache()
            await self.send("status", "Manifests reloaded")
        elif a == "ping":
            await self.send("pong", {"tab_id": self.tab_id})

    async def emit_status(self, model: str, step: str, message: str):
        status_line = f"[{model.upper()}:{step.upper()}] {message}"
        await self.send("narrator_status", {
            "line":    status_line,
            "model":   model,
            "step":    step,
            "message": message
        })

    async def run_get_tags(self):
        try:
            base = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(f"{base}/api/tags")
                data = r.json()
                models = [m["name"] for m in data.get("models", [])]
                await self.send("tags_result", {
                    "models": models, "count": len(models)})
        except Exception as e:
            await self.send("tags_error", str(e))

    async def run_get_ps(self):
        try:
            base = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(f"{base}/api/ps")
                await self.send("ps_result", r.json())
        except Exception as e:
            await self.send("ps_error", str(e))

    async def run_browser(self, msg: dict):
        await self.emit_status("WEBUSER", "NAVIGATE",
            f"going to {msg.get('url', '')}")
        result = await self.browser.navigate(msg["url"])
        if result.get("success") and result.get("screenshot_b64"):
            await self.send("screenshot", {
                "url": result["url"],
                "screenshot_b64": result["screenshot_b64"]
            })
            await self.emit_status("CHECKER", "SCAN",
                "analyzing screenshot with qwen2.5vl")
            vision = await self.vision_analyze(
                result["screenshot_b64"],
                "You are analyzing a web app screenshot. Describe: "
                "1) The main purpose of the app "
                "2) Color scheme and design style "
                "3) Key UI components visible "
                "4) Any issues or improvements needed"
            )
            result["vision_description"] = vision
        await self.send("browser_result", result)

    async def run_shell(self, msg: dict):
        await self.emit_status("SHELL", "RUN", "executing command")
        result = await self.shell.run(msg["command"])
        await self.send("shell_result", result)

    async def run_vision(self, msg: dict):
        await self.emit_status("CHECKER", "VISION",
            "qwen2.5vl analyzing image")
        description = await self.vision_analyze(
            msg.get("screenshot_b64", ""),
            msg.get("question", "What do you see?")
        )
        await self.send("vision_result", {"description": description})

    async def run_login(self, msg: dict):
        await self.emit_status("WEBUSER", "LOGIN",
            f"attempting login to {msg.get('url', '')}")
        await self.send("login_log",
            f"Attempting login to {msg.get('url')}...")
        result = await self.browser.login(
            url=msg.get("url", ""),
            username=msg.get("username", ""),
            password=msg.get("password", ""),
            max_attempts=msg.get("max_attempts", 5)
        )
        if result.get("success"):
            await self.emit_status("WEBUSER", "LOGIN",
                f"logged in after {result.get('attempts', 1)} attempt(s)")
            await self.send("login_log",
                f"Logged in after {result.get('attempts', 1)} attempt(s)")
            if result.get("screenshot_b64"):
                await self.send("screenshot", {
                    "url": result["url"],
                    "screenshot_b64": result["screenshot_b64"]
                })
        else:
            await self.emit_status("WEBUSER", "ERROR",
                f"login failed: {result.get('error')}")
            await self.send("login_log",
                f"Login failed: {result.get('error')}")
        await self.send("login_result", result)

    async def run_gmail(self, msg: dict):
        await self.emit_status("SENDER", "GMAIL", "accessing gmail")
        try:
            from .tools.gmail import GmailTool
            gmail  = GmailTool()
            action = msg.get("gmail_action")
            if action == "summary":
                await self.send("gmail_summary",
                    gmail.get_inbox_summary())
            elif action == "top_senders":
                await self.send("gmail_senders",
                    gmail.get_top_senders())
            elif action == "preview":
                await self.send("gmail_preview",
                    gmail.get_emails(msg.get("query", "in:inbox")))
            elif action == "archive":
                result = gmail.archive_emails(msg.get("query", ""))
                await self.send("gmail_done",
                    {"action": "archive", **result})
            elif action == "delete":
                result = gmail.delete_emails(msg.get("query", ""))
                await self.send("gmail_done",
                    {"action": "delete", **result})
            elif action == "unsubscribe":
                result = gmail.unsubscribe_sender(
                    msg.get("sender", ""))
                await self.send("gmail_done",
                    {"action": "unsubscribe", **result})
            else:
                await self.send("gmail_error",
                    {"message": f"Unknown gmail_action: {action}"})
        except Exception as e:
            await self.send("gmail_error", {"message": str(e)})

    async def run_github(self, msg: dict):
        from .tools.github import GitHubTool
        gh     = GitHubTool()
        action = msg.get("github_action")
        owner  = msg.get("owner",
            os.getenv("GITHUB_REPO_OWNER", ""))
        repo   = msg.get("repo",
            os.getenv("GITHUB_REPO_NAME", ""))
        if action == "get_file":
            result = await gh.get_file(
                owner, repo, msg.get("path", ""))
            await self.send("github_file", result)
        elif action == "list_files":
            result = await gh.list_files(
                owner, repo, msg.get("path", ""))
            await self.send("github_files", result)
        elif action == "get_structure":
            result = await gh.get_repo_structure(owner, repo)
            await self.send("github_structure", result)
        elif action == "get_multiple":
            result = await gh.get_multiple_files(
                owner, repo, msg.get("paths", []))
            await self.send("github_files_batch", result)
        elif action == "push_file":
            result = await gh.push_file(
                owner, repo,
                msg.get("path", ""),
                msg.get("content", ""),
                msg.get("message", "Worker Bee update"),
                msg.get("sha", None)
            )
            await self.send("github_push_result", result)

    async def run_self_repair(self, msg: dict):
        from .repair import self_repair
        await self.emit_status("REPAIR", "START",
            "beginning self-repair sequence")
        await self.send("repair_started", {
            "error": msg.get("error", "Manual repair requested")})
        success = await self_repair(
            msg.get("error", "Manual repair requested"),
            ws=self.ws)
        await self.send("repair_complete", {"success": success})

    async def vision_analyze(self, screenshot_b64: str,
                              question: str) -> str:
        # Using qwen2.5vl:7b for better vision analysis than llava
        try:
            model = "qwen2.5vl:7b"
            async with httpx.AsyncClient(timeout=60) as c:
                r = await c.post(
                    f"{OLLAMA}/api/generate",
                    json={
                        "model": model,
                        "prompt": question,
                        "images": [screenshot_b64],
                        "stream": False,
                        "options": {"num_ctx": get_num_ctx(model)}
                    }
                )
                return r.json().get("response", "Vision unavailable")
        except Exception as e:
            return f"Vision unavailable: {e}"

    async def chat(self, msg: dict):
        user_content = msg["content"]
        self.model   = msg.get("model") or pick_model(user_content)

        force_claude = msg.get("force_claude", False)
        use_claude_api = (
            force_claude or
            msg.get("use_claude", False) or
            (os.getenv("USE_CLAUDE", "false").lower() == "true"
             and should_escalate_to_claude(user_content))
        )

        self.history.append({"role": "user", "content": user_content})
        self.memory.store_message("user", user_content, self.model)
        mem_context = self.memory.build_context(user_content)

        await self.emit_status("QUEEN", "ROUTING",
            f"routing to {self.model}" +
            (" via Claude escalation" if use_claude_api else ""))

        await self.send("status", "streaming")
        full = ""
        import asyncio

        async def heartbeat():
            count = 0
            while True:
                await asyncio.sleep(30)
                count += 1
                try:
                    await self.ws.send_text(
                        '{"type":"heartbeat","data":"ping"}')
                    if count % 4 == 0:
                        await self.emit_status(
                            self.model.split(":")[0].upper(),
                            "ALIVE", "still working...")
                except Exception:
                    break

        hb_task = asyncio.create_task(heartbeat())

        try:
            if use_claude_api:
                full = await self._chat_claude(
                    user_content, mem_context)

                # If force_claude flag was set, write this as a learning example
                if force_claude:
                    await self._write_claude_example(user_content, full)

                for word in full.split():
                    await self.send("token", word + " ")
                    await asyncio.sleep(0.01)
            else:
                system_prompt = self._build_system_prompt(self.model)
                non_streaming = ["deepseek-r1:14b", "deepseek-r1:32b"]

                if self.model in non_streaming:
                    await self.send("token", "🤔 ")
                    async def thinking_updates():
                        while True:
                            await asyncio.sleep(10)
                            await self.send("token", ".")
                    think_task = asyncio.create_task(thinking_updates())
                    try:
                        async with httpx.AsyncClient(timeout=600) as c:
                            r = await c.post(
                                f"{OLLAMA}/api/chat",
                                json={
                                    "model": self.model,
                                    "messages": self._with_memory_context(
                                        mem_context, system_prompt),
                                    "stream": False,
                                    "options": {"num_ctx": get_num_ctx(self.model)}
                                }
                            )
                            raw = r.json().get(
                                "message", {}).get("content", "")
                    finally:
                        think_task.cancel()
                    await self.send("clear_thinking", {})
                    await asyncio.sleep(0.1)
                    words = raw.split()
                    full  = ""
                    for i, word in enumerate(words):
                        chunk = ("" if i == 0 else " ") + word
                        full += chunk
                        await self.send("token", chunk)
                        if i % 5 == 0:
                            await asyncio.sleep(0.01)
                else:
                    async with httpx.AsyncClient(timeout=300) as c:
                        async with c.stream(
                            "POST", f"{OLLAMA}/api/chat",
                            json={
                                "model": self.model,
                                "messages": self._with_memory_context(
                                    mem_context, system_prompt),
                                "stream": True,
                                "options": {"num_ctx": get_num_ctx(self.model)}
                            }
                        ) as r:
                            async for line in r.aiter_lines():
                                if not line.strip():
                                    continue
                                try:
                                    token = json.loads(line).get(
                                        "message", {}).get("content", "")
                                    if token:
                                        full += token
                                        await self.send("token", token)
                                except json.JSONDecodeError:
                                    continue

            self.history.append(
                {"role": "assistant", "content": full})
            hb_task.cancel()
            self.error_count = 0
            self.memory.store_message("assistant", full, self.model)
            await self.send("done", {
                "content": full, "chars": len(full)})

        except Exception as e:
            hb_task.cancel()
            self.error_count += 1
            await self.emit_status("QUEEN", "ERROR",
                f"chat error: {str(e)[:100]}")
            await self.send("error", str(e))
            if self.error_count >= self.MAX_ERRORS:
                await self.send("repair_started", {
                    "error": f"Auto-repair after {self.MAX_ERRORS} errors: {e}"
                })
                from .repair import self_repair
                await self_repair(f"Chat failing: {e}", ws=self.ws)
                self.error_count = 0

    async def _chat_claude(self, user_content: str,
                            mem_context: str) -> str:
        import anthropic

        # Initialize client with extended mode for MCP support
        client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY", ""))

        system = self._build_system_prompt("claude")
        await self.emit_status("QUEEN", "CLAUDE",
            "escalating to Claude API with full MCP connectivity")

        try:
            # Enable extended mode for MCP access
            # Available MCPs: Gmail, Google Drive, ICD-10, Supabase, Vercel, WordPress.com
            # Requested: Stripe, Calendly, Slack, Ahrefs, Supermetrics, Google Calendar
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=system,
                messages=[{"role": "user", "content": user_content}],
                # Extended mode enables MCP server connections when available
                betas=["extended-thinking-2025-01-28"]
            )
            return response.content[0].text
        except Exception as e:
            await self.emit_status("QUEEN", "ERROR",
                f"Claude API failed: {e}")
            self.model = "phi4:latest"
            return f"[Claude unavailable: {e}] Falling back to phi4..."

    async def _write_claude_example(self, task: str, response: str):
        """
        Auto-write Claude's approach to practice log as learning material
        for local models. Called when force_claude flag is used.
        """
        from datetime import datetime
        import pathlib

        practice_dir = pathlib.Path(
            os.path.expanduser("~/worker-bee/manifests/practice"))
        practice_dir.mkdir(parents=True, exist_ok=True)

        examples_file = practice_dir / "claude-examples.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract key decisions from response (first 200 chars of reasoning)
        # Look for sections that might contain reasoning
        key_decisions = "See full response above"
        if len(response) > 500:
            # Try to find reasoning/decision patterns
            for marker in ["because", "decided to", "approach:", "reasoning:"]:
                if marker in response.lower():
                    idx = response.lower().find(marker)
                    snippet = response[idx:idx+200].split('\n')[0]
                    key_decisions = snippet
                    break

        example_entry = f"""
## Example: {timestamp}
Task: {task[:200]}{'...' if len(task) > 200 else ''}

Claude's approach: {response}

Key decisions: {key_decisions}

---
"""

        try:
            # Append to file (create if doesn't exist)
            with open(examples_file, "a") as f:
                f.write(example_entry)

            await self.emit_status("MEMORY", "LOGGED",
                f"saved Claude example to practice log")
        except Exception as e:
            await self.emit_status("MEMORY", "ERROR",
                f"failed to log example: {e}")

    async def send(self, t: str, d):
        try:
            await self.ws.send_text(
                json.dumps({"type": t, "data": d}))
        except Exception:
            pass

    async def cleanup(self):
        await self.browser.close()

    def _build_system_prompt(self, model: str = None) -> str:
        target_model    = model or self.model
        getting_started = ManifestLoader.load("00-getting-started")
        model_identity  = ManifestLoader.load_for_model(target_model)
        system_overview = ManifestLoader.load("ref-system-overview")
        voice           = ManifestLoader.load("voice")
        narrator        = ManifestLoader.load("runner-narrator")

        feedback = self.memory.search(
            "positive response pattern", n=3)
        avoid    = self.memory.search(
            "negative response pattern", n=3)
        feedback_context = ""
        if feedback:
            good = [r["content"][:100] for r in feedback[:2]]
            feedback_context += (
                "RESPONSE STYLES USER LIKES:\n" +
                "\n".join(f"• {g}" for g in good) + "\n\n")
        if avoid:
            bad = [r["content"][:100] for r in avoid[:2]]
            feedback_context += (
                "RESPONSE STYLES USER DISLIKES:\n" +
                "\n".join(f"• {b}" for b in bad) + "\n\n")

        base_prompt = """You are Worker Bee, an autonomous AI agent running on Toby Anderton's Mac Studio M1 Ultra in Idaho.

MODELS IN THIS SYSTEM:
- phi4:latest — Queen/Controller, fast routing and orchestration
- deepseek-r1:14b — Planner, deep reasoning and technical briefs
- qwen2.5-coder:32b — Builder, code generation and fixes
- qwen2.5vl:7b — Checker, vision and visual verification

PRODUCTION SITES:
- mountainedgeplumbing.com
- ime-coach.com (MedLegal Nexus)
- growyournumber.com
- language-lens-elite.lovable.app

CAPABILITIES: Browser, Shell, Vision, Memory (ChromaDB),
GitHub, Gmail, Voice, Builder pipeline, Tester pipeline.

Be direct. Be specific. Use voice.md tone.
Emit status at every step: [MODEL:STEP] what you are doing."""

        parts = [p for p in [
            getting_started, model_identity, system_overview,
            voice, narrator, feedback_context, base_prompt
        ] if p]

        return "\n\n---\n\n".join(parts)

    def _with_memory_context(self, mem_context: str,
                              system_prompt: str = None) -> list:
        messages = list(self.history)
        system   = system_prompt or self._build_system_prompt()
        if mem_context:
            system = mem_context + "\n\n" + system
        if messages and messages[0]["role"] == "system":
            messages[0]["content"] = system
        else:
            messages.insert(0, {"role": "system", "content": system})
        return messages

    async def run_memory_search(self, msg: dict):
        results = self.memory.search(
            msg.get("query", ""), n=msg.get("n", 5))
        await self.send("memory_results", {
            "query": msg.get("query"), "results": results})

    async def run_memory_store(self, msg: dict):
        doc_id = self.memory.store_knowledge(
            msg.get("topic", ""),
            msg.get("content", ""),
            msg.get("source", ""))
        await self.send("memory_stored", {
            "id": doc_id, "topic": msg.get("topic")})

    async def run_memory_stats(self):
        await self.send("memory_stats", self.memory.stats())

    async def run_plan(self, msg: dict):
        goal = msg.get("goal", "")
        if not goal:
            await self.send("plan_error",
                {"message": "No goal provided"})
            return
        await self.emit_status("QUEEN", "PLAN",
            f"planning: {goal[:50]}")
        await self.send("plan_started", {"goal": goal})
        tasks = await self.planner.plan(goal)
        if not tasks:
            await self.send("plan_error",
                {"message": "Could not generate a plan"})
            return
        await self.send("plan_ready", {
            "goal": goal, "tasks": tasks, "count": len(tasks)})
        result = await self.planner.execute(ws=self.ws)
        await self.send("plan_complete", result)

    async def run_vision_report(self, msg: dict):
        from .tools.vision_reporter import VisionReporter
        vr    = VisionReporter()
        url   = msg.get("url", "https://worker-bee.lovable.app")
        label = msg.get("label", "worker-bee-ui")
        await self.emit_status("CHECKER", "VISION_REPORT",
            f"taking screenshot of {url}")
        result = await self.browser.navigate(url)
        if not result.get("success"):
            await self.send("error",
                f"Screenshot failed: {result.get('error')}")
            return
        screenshot_b64 = result.get("screenshot_b64", "")
        await self.emit_status("CHECKER", "QWEN2.5VL",
            "analyzing with qwen2.5vl")
        vision = await self.vision_analyze(
            screenshot_b64,
            "Analyze the Worker Bee AI agent UI in detail.")
        await self.emit_status("DEPLOY", "GITHUB",
            "pushing screenshot to github")
        push_result = await vr.push_screenshot(
            screenshot_b64, label=label, description=vision)
        if push_result.get("success"):
            await self.send("screenshot", {
                "url": url, "screenshot_b64": screenshot_b64})
            await self.send("vision_result", {"description": vision})
            await self.send("vision_report_done", {
                "github_url": push_result["github_url"],
                "raw_url":    push_result["url"],
                "label":      label,
                "analysis":   vision
            })
        else:
            await self.send("error",
                f"Push failed: {push_result.get('error')}")

    async def run_learn_now(self, msg: dict):
        from .tools.learner import learn_session
        await self.emit_status("MEMORY", "LEARN",
            "starting learning session")
        async def log_fn(m):
            await self.send("token", f"\n{m}")
        count = await learn_session(
            memory=self.memory, log_fn=log_fn)
        await self.send("done", {
            "content": f"\n✅ Learning complete — {count} sources processed.",
            "chars": 50
        })

    async def run_voice_input(self, msg: dict):
        import main as app_main
        await self.send("status", "listening")
        if app_main.voice_daemon_ws:
            await app_main.voice_daemon_ws.send_text(
                json.dumps({
                    "type": "voice_request",
                    "seconds": msg.get("seconds", 5)
                })
            )
        else:
            from .tools.ears import listen
            result = await listen(
                seconds=msg.get("seconds", 5), gain=15)
            if result.get("success") and result.get("text"):
                await self.send("voice_transcription",
                    {"text": result["text"]})
            else:
                await self.send("voice_error",
                    {"message": "No speech detected"})

    async def run_scaffold(self, msg: dict):
        from .tools.scaffold import create_project
        name     = msg.get("name", "")
        template = msg.get("template", "react-ts")
        if not name:
            await self.send("error", "Project name required")
            return
        await self.emit_status("BUILDER", "SCAFFOLD",
            f"creating project: {name}")
        result = await create_project(name, template)
        await self.send("scaffold_result", result)

    async def run_list_projects(self):
        from .tools.scaffold import list_projects
        projects = list_projects()
        await self.send("projects_list", {"projects": projects})

    async def run_dev_server(self, msg: dict):
        from .tools.devserver import start
        name = msg.get("project", "")
        port = msg.get("port", 5173)
        await self.emit_status("DEPLOY", "DEV_SERVER",
            f"starting dev server for {name}")
        result = await start(name, port)
        await self.send("dev_server_result", result)

    async def run_dev_server_stop(self, msg: dict):
        from .tools.devserver import stop
        result = await stop(msg.get("project", ""))
        await self.send("dev_server_stopped", result)

    async def run_build(self, msg: dict):
        import asyncio
        from .tools.builder import build
        from .tools.scaffold import get_project_files, apply_changes
        prompt  = msg.get("prompt", "")
        project = msg.get("project", "")
        if not prompt or not project:
            await self.send("error", "prompt and project required")
            return
        await self.emit_status("QUEEN", "ROUTING",
            f"builder pipeline starting for {project}")
        await self.send("build_started", {
            "prompt": prompt, "project": project})
        current_files = get_project_files(project)
        await self.emit_status("PLANNER", "BRIEF",
            "deepseek writing technical brief")
        result = await build(
            prompt, project, current_files, self.ws,
            use_architect=msg.get("use_architect", True),
            use_claude=msg.get("use_claude", False))
        if result.get("success"):
            await self.emit_status("BUILDER", "APPLY",
                "applying files to project")
            applied = apply_changes(project, result["files"])
            await self.send("build_applied", {
                "files": applied, "project": project})
            from .tools.devserver import get_url
            url = get_url(project)
            if url:
                await asyncio.sleep(2)
                await self.emit_status("CHECKER", "SCREENSHOT",
                    "taking screenshot for qwen2.5vl")
                shot = await self.browser.navigate(url)
                if shot.get("success"):
                    await self.send("screenshot", {
                        "url": url,
                        "screenshot_b64": shot["screenshot_b64"]
                    })
                    await self.emit_status("CHECKER", "SCAN",
                        "qwen2.5vl checking output")
                    vision = await self.vision_analyze(
                        shot["screenshot_b64"],
                        f"Does this match: '{prompt}'? "
                        f"Reply YES or describe issues.")
                    await self.send("build_vision", {
                        "vision": vision, "prompt": prompt})
        else:
            await self.emit_status("BUILDER", "ERROR",
                "build failed")
            await self.send("build_error", result)

    async def run_build_start(self, msg: dict):
        from .tools.builder import build_loop
        result = await build_loop(
            prompt=msg.get("prompt", ""),
            project_name=msg.get("project", ""),
            runner=self,
            ws=self.ws,
            max_iterations=msg.get("iterations", 3)
        )
        await self.send("build_complete", result)

    async def run_save_cookies(self, msg: dict):
        try:
            from .tools.cookies import save_cookies
            domain  = msg.get("domain", "")
            cookies = msg.get("cookies", [])
            path    = save_cookies(domain, cookies)
            await self.send("cookies_saved", {
                "domain": domain,
                "count": len(cookies),
                "path": path})
        except Exception as e:
            await self.send("error", str(e))

    async def run_speak(self, msg: dict):
        import asyncio, re
        text = msg.get("text", "")
        if not text:
            return
        text = re.sub(r'\*\*|__|\*|_|#{1,6} |`', '', text)
        text = text[:500]
        proc = await asyncio.create_subprocess_shell(
            f'say "{text}"',
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await proc.wait()
        await self.send("speak_done", {"success": True})

    async def run_voice_transcribe(self, msg: dict):
        import base64, pathlib, asyncio
        audio_b64 = msg.get("audio_b64", "")
        fmt       = msg.get("format", "webm")
        if not audio_b64:
            await self.send("voice_error",
                {"message": "No audio received"})
            return
        raw_path = pathlib.Path(f"/tmp/wb_voice.{fmt}")
        wav_path = pathlib.Path("/tmp/wb_voice.wav")
        raw_path.write_bytes(base64.b64decode(audio_b64))
        proc = await asyncio.create_subprocess_shell(
            f"ffmpeg -y -i {raw_path} -ar 16000 -ac 1 {wav_path}",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await proc.wait()
        from .tools.ears import get_model
        model  = get_model()
        result = model.transcribe(
            str(wav_path), language="en", fp16=False)
        text = result["text"].strip()
        if text:
            await self.send("voice_transcription", {"text": text})
        else:
            await self.send("voice_error",
                {"message": "No speech detected"})

    async def run_index_site(self, msg: dict):
        from .tools.site_indexer import index_site
        url = msg.get("url", "")
        if not url:
            await self.send("error", "URL required")
            return
        await self.emit_status("NAVIGATOR", "INDEX",
            f"indexing {url}")
        await self.send("index_started", {"url": url})
        async def log_fn(message):
            await self.send("index_log", {"message": message})
        result = await index_site(
            url=url,
            browser=self.browser,
            vision_analyze_fn=self.vision_analyze,
            log_fn=log_fn)
        if result.get("success"):
            await self.send("index_complete", result)
            await self.send("done", {
                "content": f"✅ Index complete — {result['pages']} pages",
                "chars": 60
            })
        else:
            await self.send("error",
                f"Index failed: {result.get('error')}")
