import asyncio, pathlib, os

BLOCKED = [
    "rm -rf /", "sudo rm -rf", "mkfs", "dd if=",
    ":(){:|:&};:", "chmod 777 /", "curl | bash", "wget | bash"
]

VENV = str(pathlib.Path.home() / "worker-bee" / ".venv" / "bin")

class ShellTool:
    async def run(self, command: str, timeout: int = 120) -> dict:
        for b in BLOCKED:
            if b in command:
                return {"error": f"Blocked: {b}", "success": False}
        env = os.environ.copy()
        env["PATH"] = f"{VENV}:{env.get('PATH', '')}"
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(pathlib.Path.home() / "worker-bee"),
                env=env
            )
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return {
                "stdout": out.decode(),
                "returncode": proc.returncode,
                "success": proc.returncode == 0
            }
        except asyncio.TimeoutError:
            return {"error": "Timed out", "success": False}
