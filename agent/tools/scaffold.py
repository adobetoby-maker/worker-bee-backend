import asyncio, pathlib, os, json
from dotenv import dotenv_values

_env = dotenv_values(str(pathlib.Path.home() / "worker-bee" / ".env"))
PROJECTS = pathlib.Path.home() / "worker-bee" / "projects"

async def create_project(name: str, 
                          template: str = "react-ts") -> dict:
    """Create a new Vite + React + Tailwind project"""
    project_path = PROJECTS / name
    
    if project_path.exists():
        return {
            "success": False,
            "error": f"Project {name} already exists",
            "path": str(project_path)
        }
    
    PROJECTS.mkdir(parents=True, exist_ok=True)
    
    # Create Vite project
    # Ensure name is safe for shell
    safe_name = name.replace(" ", "-").replace("_", "-").lower()
    proc = await asyncio.create_subprocess_shell(
        f"cd {PROJECTS} && npm create vite@latest {safe_name} -- --template {template} --yes",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    out, err = await asyncio.wait_for(proc.communicate(), timeout=60)
    
    if proc.returncode != 0:
        return {
            "success": False,
            "error": err.decode()
        }
    
    # Install dependencies
    proc2 = await asyncio.create_subprocess_shell(
        f"cd {project_path} && npm install",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await asyncio.wait_for(proc2.communicate(), timeout=120)
    
    # Install Tailwind
    proc3 = await asyncio.create_subprocess_shell(
        f"cd {project_path} && npm install -D tailwindcss postcss autoprefixer && npx tailwindcss init -p",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await asyncio.wait_for(proc3.communicate(), timeout=60)
    
    # Add Tailwind to CSS
    css_path = project_path / "src" / "index.css"
    css_path.write_text("""@tailwind base;
@tailwind components;
@tailwind utilities;
""")
    
    # Update tailwind.config.js
    (project_path / "tailwind.config.js").write_text("""/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
""")
    
    # Write vite config with allowed hosts for tunnel preview
    (project_path / "vite.config.ts").write_text("""import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: [
      'localhost',
      'preview.tobyandertonmd.com'
    ]
  }
})
""")

    # Create project manifest
    manifest = {
        "name": name,
        "template": template,
        "created": __import__('datetime').datetime.now().isoformat(),
        "path": str(project_path),
        "port": 5173
    }
    (project_path / "wb-project.json").write_text(
        json.dumps(manifest, indent=2))
    
    return {
        "success": True,
        "name": name,
        "path": str(project_path),
        "message": f"Project {name} created with React + TypeScript + Tailwind"
    }

def list_projects() -> list:
    """List all Worker Bee projects"""
    projects = []
    for p in PROJECTS.iterdir():
        manifest = p / "wb-project.json"
        if manifest.exists():
            data = json.loads(manifest.read_text())
            projects.append(data)
        elif (p / "package.json").exists():
            projects.append({
                "name": p.name,
                "path": str(p)
            })
    return projects

def get_project_files(project_name: str) -> dict:
    """Get all source files from a project"""
    project_path = PROJECTS / project_name
    if not project_path.exists():
        return {"error": f"Project {project_name} not found"}
    
    files = {}
    src_path = project_path / "src"
    if src_path.exists():
        for f in src_path.rglob("*"):
            if f.is_file() and f.suffix in [
                '.tsx', '.ts', '.jsx', '.js', 
                '.css', '.html', '.json'
            ]:
                rel_path = f.relative_to(project_path)
                try:
                    files[str(rel_path)] = f.read_text()
                except Exception:
                    pass
    
    return files

def apply_changes(project_name: str, 
                   changes: dict) -> list:
    """Apply file changes to a project"""
    project_path = PROJECTS / project_name
    applied = []
    
    for filepath, content in changes.items():
        full_path = project_path / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        applied.append(filepath)
    
    return applied
