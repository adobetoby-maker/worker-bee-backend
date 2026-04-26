import asyncio, pathlib, json, os
from dotenv import dotenv_values

_env = dotenv_values(str(pathlib.Path.home() / "worker-bee" / ".env"))
PROJECTS = pathlib.Path.home() / "worker-bee" / "projects"

# Track running servers
_servers = {}

async def start(project_name: str, 
                port: int = 5173) -> dict:
    """Start Vite dev server for a project"""
    project_path = PROJECTS / project_name
    
    if not project_path.exists():
        return {"success": False, 
                "error": f"Project {project_name} not found"}
    
    if project_name in _servers:
        return {"success": True, 
                "message": "Already running",
                "url": f"http://localhost:{port}"}
    
    proc = await asyncio.create_subprocess_shell(
        f"cd {project_path} && npm run dev -- --port {port} --host",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    _servers[project_name] = {
        "proc": proc,
        "port": port,
        "path": str(project_path)
    }
    
    # Wait for server to start
    await asyncio.sleep(3)
    
    return {
        "success": True,
        "project": project_name,
        "url": f"http://localhost:{port}",
        "message": f"Dev server running at http://localhost:{port}"
    }

async def stop(project_name: str) -> dict:
    """Stop a project's dev server"""
    if project_name not in _servers:
        return {"success": False, 
                "error": "Server not running"}
    
    server = _servers.pop(project_name)
    server["proc"].terminate()
    await server["proc"].wait()
    
    return {"success": True, 
            "message": f"Stopped {project_name}"}

async def stop_all():
    """Stop all running servers"""
    for name in list(_servers.keys()):
        await stop(name)

def get_running() -> list:
    """Get list of running dev servers"""
    return [
        {"name": k, "url": f"http://localhost:{v['port']}"}
        for k, v in _servers.items()
    ]

def get_url(project_name: str) -> str:
    if project_name in _servers:
        return f"http://localhost:{_servers[project_name]['port']}"
    return ""
