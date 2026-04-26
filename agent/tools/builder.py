import httpx, json, os, asyncio, pathlib, re
from dotenv import dotenv_values

_env = dotenv_values(str(pathlib.Path.home() / "worker-bee" / ".env"))
OLLAMA = _env.get("OLLAMA_HOST", "http://localhost:11434")

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

    # Build context from current files
    context = ""
    if current_files:
        context = "\n\nCURRENT PROJECT FILES:\n"
        for filepath, content in list(
            current_files.items())[:10]:
            context += (f"\n--- {filepath} ---\n"
                       f"{content[:2000]}\n")

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
        
        # Get current project state
        current_files = get_project_files(project_name)
        
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
