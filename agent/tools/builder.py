import httpx, json, os, asyncio, pathlib, re, subprocess
from datetime import datetime
from dotenv import dotenv_values

_env = dotenv_values(str(pathlib.Path.home() / "worker-bee" / ".env"))
OLLAMA = _env.get("OLLAMA_HOST", "http://localhost:11434")
PROJECTS = pathlib.Path.home() / "worker-bee" / "projects"
GITHUB_TOKEN = _env.get("GITHUB_TOKEN", "")
GITHUB_USERNAME = _env.get("GITHUB_USERNAME", "adobetoby-maker")

BASE_FILES_PROMPT = """
CRITICAL: Always output these base files if they don't exist:

=== src/main.tsx ===
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
createRoot(document.getElementById('root')!).render(
  <StrictMode><App /></StrictMode>
)
=== end ===

=== src/index.css ===
@tailwind base;
@tailwind components;
@tailwind utilities;
=== end ===

=== src/App.tsx ===
import Hero from './components/Hero'
function App() {
  return <div className="min-h-screen bg-[#0a0a0a]"><Hero /></div>
}
export default App
=== end ===

Then output your custom components.
"""

BUILDER_PROMPT = """You are Worker Bee Builder — an expert React/TypeScript/Tailwind developer.

When asked to build or modify UI always output COMPLETE files.

OUTPUT FORMAT — use this EXACT format for every file:
=== src/components/Hero.tsx ===
<complete file content here — never partial>
=== end ===

RULES:
1. ALWAYS output complete files — never snippets or diffs
2. NEVER use markdown backticks — output raw code only, no ```tsx or ``` markers ever
2. Use TypeScript always
3. Use Tailwind CSS for ALL styling — no inline styles
4. Mobile first — design for 375px then scale up
5. Clean modern design with generous whitespace
6. Smooth animations where appropriate
7. After outputting files list what changed:
   CHANGED: src/components/Hero.tsx

STACK:
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Lucide React for icons

DESIGN PRINCIPLES:
- Clean and modern
- Generous whitespace  
- Strong typography hierarchy
- Purposeful color use
- Delightful micro-interactions
- Professional feel
"""

def extract_files(response: str) -> dict:
    """Extract file changes from qwen response"""
    files = {}
    lines = response.split('\n')
    current_file = None
    current_content = []
    
    for line in lines:
        if (line.startswith('=== ') and 
            line.endswith(' ===') and 
            'end' not in line.lower()):
            current_file = line[4:-4].strip()
            current_content = []
        elif line.strip() == '=== end ===' and current_file:
            raw = '\n'.join(current_content)
            # Strip markdown code fences qwen sometimes adds
            lines = raw.split('\n')
            if lines and lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            files[current_file] = '\n'.join(lines)
            current_file = None
            current_content = []
        elif current_file is not None:
            current_content.append(line)
    
    return files

def extract_changed(response: str) -> list:
    """Extract list of changed files from response"""
    changed = []
    for line in response.split('\n'):
        if line.startswith('CHANGED:'):
            changed.append(line.replace('CHANGED:', '').strip())
    return changed

def scan_project_files(project_name: str) -> dict:
    """
    Scan project folder for existing code structure.
    Returns file list and key file contents for context.

    Strategy:
    - Include ALL .tsx, .ts, .jsx, .js files
    - Include package.json, tsconfig.json
    - Include .css files
    - Skip node_modules, .git, dist, build
    - Limit each file to first 150 lines to manage context size
    """
    project_path = PROJECTS / project_name
    if not project_path.exists():
        return {"file_list": [], "key_files": {}}

    file_list = []
    key_files = {}

    # Directories to skip
    skip_dirs = {'node_modules', '.git', 'dist', 'build', '.vite', 'coverage'}

    # File extensions to include
    code_extensions = {'.tsx', '.ts', '.jsx', '.js', '.css', '.json'}

    src_path = project_path / "src"
    if src_path.exists():
        for f in src_path.rglob("*"):
            # Skip directories we don't want
            if any(skip in f.parts for skip in skip_dirs):
                continue

            if f.is_file() and f.suffix in code_extensions:
                rel_path = str(f.relative_to(project_path))
                file_list.append(rel_path)

                # Read file content (first 150 lines)
                try:
                    lines = f.read_text().split('\n')[:150]
                    key_files[rel_path] = '\n'.join(lines)
                except Exception as e:
                    key_files[rel_path] = f"<error reading file: {e}>"

    # Always include package.json if it exists
    package_json = project_path / "package.json"
    if package_json.exists():
        try:
            key_files["package.json"] = package_json.read_text()
            file_list.append("package.json")
        except Exception:
            pass

    return {
        "file_list": file_list,
        "key_files": key_files
    }

def git_init_project(project_name: str) -> dict:
    """
    Initialize git repository in project if not already initialized.
    Returns success status and path to .git folder.
    """
    project_path = PROJECTS / project_name
    git_dir = project_path / ".git"

    if git_dir.exists():
        return {
            "success": True,
            "already_initialized": True,
            "path": str(git_dir)
        }

    try:
        # Initialize git repo
        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            capture_output=True,
            check=True
        )

        # Create .gitignore if it doesn't exist
        gitignore = project_path / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text("""# Dependencies
node_modules/
.pnp
.pnp.js

# Build
dist/
build/
.vite/

# Env
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Logs
*.log
npm-debug.log*
""")

        return {
            "success": True,
            "already_initialized": False,
            "path": str(git_dir)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def create_github_repo(project_name: str) -> dict:
    """
    Create GitHub repository for project if it doesn't exist.
    Repo name: worker-bee-{project_name}

    Returns: {"success": bool, "repo_url": str, "exists": bool}
    """
    if not GITHUB_TOKEN:
        return {
            "success": False,
            "error": "GITHUB_TOKEN not set in .env"
        }

    repo_name = f"worker-bee-{project_name}"

    try:
        # Check if repo exists
        async with httpx.AsyncClient(timeout=30) as client:
            check_response = await client.get(
                f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}",
                headers={
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )

            if check_response.status_code == 200:
                repo_url = check_response.json()["html_url"]
                return {
                    "success": True,
                    "repo_url": repo_url,
                    "exists": True
                }

            # Create repo
            create_response = await client.post(
                "https://api.github.com/user/repos",
                headers={
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json"
                },
                json={
                    "name": repo_name,
                    "description": f"Worker Bee project: {project_name}",
                    "private": False,
                    "auto_init": False
                }
            )

            if create_response.status_code == 201:
                repo_url = create_response.json()["html_url"]
                return {
                    "success": True,
                    "repo_url": repo_url,
                    "exists": False
                }
            else:
                return {
                    "success": False,
                    "error": f"GitHub API error: {create_response.status_code}"
                }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def push_to_github(project_name: str) -> dict:
    """
    Push local commits to GitHub repository.
    Creates remote and pushes if first time.

    Returns: {"success": bool, "pushed": bool, "repo_url": str}
    """
    if not GITHUB_TOKEN:
        return {
            "success": True,
            "pushed": False,
            "reason": "GITHUB_TOKEN not configured (skipping push)"
        }

    project_path = PROJECTS / project_name
    repo_name = f"worker-bee-{project_name}"

    # Ensure GitHub repo exists
    repo_result = await create_github_repo(project_name)
    if not repo_result.get("success"):
        return {
            "success": False,
            "error": f"Failed to create GitHub repo: {repo_result.get('error')}"
        }

    repo_url = repo_result["repo_url"]
    git_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git"

    try:
        # Check if remote exists
        remote_check = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_path,
            capture_output=True,
            text=True
        )

        if remote_check.returncode != 0:
            # Add remote
            subprocess.run(
                ["git", "remote", "add", "origin", git_url],
                cwd=project_path,
                capture_output=True,
                check=True
            )

        # Push to GitHub
        push_result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=project_path,
            capture_output=True,
            text=True
        )

        if push_result.returncode != 0:
            # Try master branch if main doesn't exist
            subprocess.run(
                ["git", "branch", "-M", "main"],
                cwd=project_path,
                capture_output=True
            )
            push_result = subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=project_path,
                capture_output=True,
                text=True
            )

        if push_result.returncode == 0:
            return {
                "success": True,
                "pushed": True,
                "repo_url": repo_url
            }
        else:
            return {
                "success": False,
                "error": f"Git push failed: {push_result.stderr}"
            }

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"Git command failed: {e.stderr.decode() if e.stderr else str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def git_commit_build(
    project_name: str,
    prompt: str,
    job_id: str,
    files: list,
    model: str = "qwen2.5-coder:32b"
) -> dict:
    """
    Commit build changes with metadata.

    Commit message format:
    Build: <first 50 chars of prompt> (job_id)

    Prompt: "<full prompt>"
    Model: qwen2.5-coder:32b
    Files: src/components/Hero.tsx, src/App.tsx
    Timestamp: 2026-04-26T11:30:00
    """
    project_path = PROJECTS / project_name

    # Ensure git is initialized
    init_result = git_init_project(project_name)
    if not init_result["success"]:
        return {"success": False, "error": f"Git init failed: {init_result.get('error')}"}

    try:
        # Stage all changes
        subprocess.run(
            ["git", "add", "."],
            cwd=project_path,
            capture_output=True,
            check=True
        )

        # Check if there are changes to commit
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True
        )

        if not status.stdout.strip():
            return {
                "success": True,
                "no_changes": True,
                "message": "No changes to commit"
            }

        # Build commit message
        prompt_short = prompt[:50] + "..." if len(prompt) > 50 else prompt
        timestamp = datetime.now().isoformat()
        files_str = ", ".join(files[:5])  # First 5 files
        if len(files) > 5:
            files_str += f" (+{len(files) - 5} more)"

        commit_message = f"""Build: {prompt_short} ({job_id})

Prompt: "{prompt}"
Model: {model}
Files: {files_str}
Timestamp: {timestamp}"""

        # Create commit
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=project_path,
            capture_output=True,
            check=True
        )

        # Get commit hash
        commit_hash = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        return {
            "success": True,
            "commit_hash": commit_hash,
            "message": commit_message,
            "files_count": len(files)
        }

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"Git commit failed: {e.stderr.decode() if e.stderr else str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def build(
    prompt: str,
    project_name: str,
    current_files: dict = None,
    ws=None,
    use_architect: bool = True,
    use_claude: bool = False
) -> dict:
    """
    Send prompt to qwen and get file changes back.
    If use_architect=True, deepseek first creates
    a detailed brief then qwen executes it.
    """
    async def log(msg):
        print(f"[BUILDER] {msg}")
        if ws:
            await ws.send_text(json.dumps({
                "type": "build_log",
                "data": {"message": msg}
            }))

    await log(f"Building: {prompt[:80]}...")

    # Build rich context from current files
    context = ""
    if current_files:
        file_list = list(current_files.keys())
        context = f"\n\nEXISTING PROJECT STRUCTURE ({len(file_list)} files):\n"
        context += "Files: " + ", ".join(file_list) + "\n\n"

        # Include key file contents (prioritize components and App.tsx)
        priority_files = [f for f in file_list if 'App.tsx' in f or 'component' in f.lower()]
        other_files = [f for f in file_list if f not in priority_files]

        context += "KEY FILES:\n"
        for filepath in (priority_files[:8] + other_files[:7]):  # Top 15 files max
            content = current_files[filepath]
            context += f"\n--- {filepath} ---\n{content}\n"

        context += "\n⚠️ IMPORTANT: Your changes must INTEGRATE with this existing code, not replace it.\n"
        context += "Reference existing components and patterns. Maintain consistency.\n"

    # Step 1 — Architect creates brief
    if use_architect:
        await log("🏗 Architect thinking...")
        if ws:
            await ws.send_text(json.dumps({
                "type": "build_phase",
                "data": {
                    "phase": "architect",
                    "message": "deepseek designing..."
                }
            }))
        
        from .architect import architect
        brief, token_stats = await architect(
            request=prompt,
            context=context,
            use_claude=use_claude,
            fast=False
        )

        await log(f"📋 Brief ready ({len(brief)} chars)")
        if token_stats:
            await log(f"💰 Claude tokens: {token_stats.get('input_tokens', 0)} in, {token_stats.get('output_tokens', 0)} out, ${token_stats.get('cost_usd', 0)}")
        
        if ws:
            await ws.send_text(json.dumps({
                "type": "build_brief",
                "data": {"brief": brief[:500] + "..."}
            }))
        
        # qwen gets the brief not the raw request
        full_prompt = f"""Execute this technical brief exactly.
Output complete files in === filename === format.

{BASE_FILES_PROMPT}

BRIEF:
{brief}

ORIGINAL REQUEST: {prompt}
{context}"""
        
        await log("⚡ qwen building from brief...")
        if ws:
            await ws.send_text(json.dumps({
                "type": "build_phase",
                "data": {
                    "phase": "builder",
                    "message": "qwen coding..."
                }
            }))
    else:
        full_prompt = f"{prompt}{context}"

    try:
        async with httpx.AsyncClient(timeout=300) as c:
            r = await c.post(
                f"{OLLAMA}/api/chat",
                json={
                    "model": "qwen2.5-coder:32b",
                    "messages": [
                        {
                            "role": "system",
                            "content": BUILDER_PROMPT
                        },
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ],
                    "stream": False,
                    "options": {"num_predict": 8192}
                }
            )
            response = r.json().get(
                "message", {}).get("content", "")
    except Exception as e:
        return {"success": False, "error": str(e)}

    await log(f"Got response ({len(response)} chars)")

    files = extract_files(response)
    changed = extract_changed(response)

    if not files:
        await log("No file changes found in response")
        return {
            "success": False,
            "error": "No files generated",
            "response": response
        }

    await log(f"Generated {len(files)} files: {list(files.keys())}")

    return {
        "success": True,
        "files": files,
        "changed": changed,
        "response": response,
        "file_count": len(files)
    }

async def build_loop(
    prompt: str,
    project_name: str,
    runner=None,
    ws=None,
    max_iterations: int = 3
) -> dict:
    """
    Full autonomous build loop:
    1. Get current files
    2. Ask qwen to build/fix
    3. Apply changes
    4. Screenshot result
    5. llava checks quality
    6. Iterate if needed
    """
    from .scaffold import get_project_files, apply_changes
    from .devserver import get_url
    
    async def log(msg):
        print(f"[BUILD LOOP] {msg}")
        if ws:
            await ws.send_text(json.dumps({
                "type": "build_log",
                "data": {"message": msg}
            }))

    results = []
    
    for iteration in range(1, max_iterations + 1):
        await log(f"Iteration {iteration}/{max_iterations}")

        if ws:
            await ws.send_text(json.dumps({
                "type": "build_iteration",
                "data": {
                    "iteration": iteration,
                    "total": max_iterations,
                    "prompt": prompt
                }
            }))

        # Get current project state with full file scanning
        project_context = scan_project_files(project_name)
        current_files = project_context.get("key_files", {})

        await log(f"📁 Scanned {len(project_context.get('file_list', []))} files from project")
        
        # Generate changes
        result = await build(
            prompt, project_name, current_files, ws)
        
        if not result.get("success"):
            await log(f"Build failed: {result.get('error')}")
            break
        
        # Apply changes
        applied = apply_changes(
            project_name, result["files"])
        await log(f"Applied: {applied}")

        if ws:
            await ws.send_text(json.dumps({
                "type": "build_applied",
                "data": {
                    "files": applied,
                    "iteration": iteration
                }
            }))

        # Git commit the changes
        # Extract job_id from context if available, otherwise use iteration number
        job_id = f"iter_{iteration}"
        commit_result = git_commit_build(
            project_name=project_name,
            prompt=prompt,
            job_id=job_id,
            files=applied,
            model="qwen2.5-coder:32b"
        )

        commit_hash = None
        if commit_result.get("success"):
            if commit_result.get("no_changes"):
                await log("📝 No changes to commit")
            else:
                commit_hash = commit_result.get("commit_hash", "")
                commit_hash_short = commit_hash[:8] if commit_hash else "unknown"
                await log(f"✅ Git commit: {commit_hash_short}")
                if ws:
                    await ws.send_text(json.dumps({
                        "type": "build_committed",
                        "data": {
                            "commit_hash": commit_hash,
                            "files_count": len(applied)
                        }
                    }))
        else:
            await log(f"⚠️ Git commit failed: {commit_result.get('error', 'Unknown error')}")

        # Push to GitHub (if token configured)
        if commit_hash and GITHUB_TOKEN:
            await log("📤 Pushing to GitHub...")
            push_result = await push_to_github(project_name)

            if push_result.get("success") and push_result.get("pushed"):
                repo_url = push_result.get("repo_url", "")
                await log(f"✅ Pushed to {repo_url}")
                if ws:
                    await ws.send_text(json.dumps({
                        "type": "github_pushed",
                        "data": {
                            "repo_url": repo_url,
                            "commit_hash": commit_hash
                        }
                    }))
            elif push_result.get("pushed") == False:
                # Token not configured - silent skip
                pass
            else:
                await log(f"⚠️ GitHub push failed: {push_result.get('error', 'Unknown error')}")

        # Send build preview to frontend
        # Get preview URL
        url = get_url(project_name)
        if url and ws:
            # Create summary from prompt (first sentence or up to 100 chars)
            summary = prompt.split('.')[0][:100]
            if len(prompt) > 100:
                summary += "..."

            await ws.send_text(json.dumps({
                "type": "build_preview",
                "data": {
                    "url": url,
                    "commit_hash": commit_hash or "no-commit",
                    "files_changed": applied[:10],  # Max 10 files to show
                    "summary": summary,
                    "project": project_name,
                    "iteration": iteration
                }
            }))
        
        # Screenshot result if dev server running
        url = get_url(project_name)
        if url and runner:
            await log("Screenshotting result...")
            await asyncio.sleep(2)  # Wait for hot reload
            
            screenshot = await runner.browser.navigate(url)
            
            if screenshot.get("success"):
                if ws:
                    await ws.send_text(json.dumps({
                        "type": "screenshot",
                        "data": {
                            "url": url,
                            "screenshot_b64": screenshot["screenshot_b64"]
                        }
                    }))
                
                # llava quality check
                vision = await runner.vision_analyze(
                    screenshot["screenshot_b64"],
                    f"Does this React app match this request: '{prompt}'? "
                    f"Reply YES if it looks good, or describe specifically "
                    f"what needs to be fixed."
                )
                
                await log(f"Vision check: {vision[:100]}")
                
                results.append({
                    "iteration": iteration,
                    "files": applied,
                    "vision": vision
                })
                
                # If llava says it looks good — done
                if "YES" in vision.upper():
                    await log("✅ Build looks good!")
                    break
                    
                # Otherwise iterate with vision feedback
                if iteration < max_iterations:
                    prompt = (f"Fix these issues: {vision}\n\n"
                             f"Original request: {prompt}")
                    await log(f"Iterating: {vision[:80]}")
        else:
            results.append({
                "iteration": iteration,
                "files": applied
            })
            break
    
    await log("Build complete")
    
    if ws:
        await ws.send_text(json.dumps({
            "type": "build_complete",
            "data": {
                "project": project_name,
                "iterations": len(results),
                "results": results
            }
        }))
    
    return {
        "success": True,
        "project": project_name,
        "iterations": len(results),
        "results": results
    }
