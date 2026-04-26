import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from agent.runner import AgentRunner

load_dotenv(os.path.expanduser("~/worker-bee/.env"))

app = FastAPI(title="Worker Bee Agent")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"])

runners: Dict[str, AgentRunner] = {}
jobs: Dict[str, Dict[str, Any]] = {}
voice_daemon_ws = None

def get_active_build_for_project(project: str) -> str | None:
    """Check if a project has an active build job. Returns job_id or None."""
    for job_id, job in jobs.items():
        if job["status"] in ("queued", "running"):
            if job["action"] in ("build", "build_start"):
                if job["payload"].get("project") == project:
                    return job_id
    return None

def cancel_job(job_id: str, reason: str = "Cancelled"):
    """Cancel a running or queued job."""
    if job_id in jobs:
        update_job(job_id, "cancelled", f"Cancelled: {reason}")

def create_job(tab_id: str, action: str, payload: dict) -> str:
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    jobs[job_id] = {
        "id": job_id,
        "tab_id": tab_id,
        "action": action,
        "payload": payload,
        "status": "queued",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "progress": [],
        "result": None,
        "error": None
    }
    return job_id

def update_job(job_id: str, status: str, progress_msg: str = None, result=None, error=None):
    if job_id not in jobs:
        return
    jobs[job_id]["status"] = status
    jobs[job_id]["updated_at"] = datetime.now().isoformat()
    if progress_msg:
        jobs[job_id]["progress"].append({
            "time": datetime.now().isoformat(),
            "message": progress_msg
        })
    if result is not None:
        jobs[job_id]["result"] = result
    if error is not None:
        jobs[job_id]["error"] = error

async def run_background_job(job_id: str, tab_id: str, msg: dict):
    update_job(job_id, "running", "Job started")

    class JobWebSocket:
        async def send_text(self, data: str):
            try:
                parsed = json.loads(data)
                msg_type = parsed.get("type", "")
                msg_data = parsed.get("data", "")
                update_job(job_id, "running", f"{msg_type}: {str(msg_data)[:200]}")
                if tab_id in runners:
                    try:
                        await runners[tab_id].ws.send_text(data)
                    except Exception:
                        pass
            except Exception:
                pass

    job_ws = JobWebSocket()
    try:
        runner = AgentRunner(tab_id, job_ws)
        await runner.handle(msg)
        update_job(job_id, "complete", "Job finished successfully")
    except Exception as e:
        update_job(job_id, "failed", f"Job failed: {str(e)}", error=str(e))

BACKGROUND_ACTIONS = {
    "build", "build_start", "browser", "login",
    "index_site", "plan", "learn_now", "vision_report"
}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "worker-bee-agent",
        "version": "3.2.0",
        "active_runners": len(runners),
        "active_jobs": len([j for j in jobs.values() if j["status"] == "running"])
    }

@app.get("/api/projects")
async def get_projects():
    from agent.tools.scaffold import list_projects
    return {"projects": list_projects()}

@app.get("/api/tags")
async def tags():
    import httpx
    base = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(f"{base}/api/tags")
        return r.json()

@app.get("/api/ps")
async def ps():
    import httpx
    base = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(f"{base}/api/ps")
        return r.json()

@app.get("/api/jobs")
async def get_jobs():
    return {"jobs": list(jobs.values())}

@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    if job_id not in jobs:
        return {"error": "Job not found"}
    return jobs[job_id]

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    if job_id in jobs:
        del jobs[job_id]
    return {"status": "deleted"}

@app.post("/api/morning-report")
async def receive_morning_report(report_data: dict):
    """
    Receive morning report from morning_report.py script.
    Broadcast to all connected WebSocket clients.
    """
    # Broadcast to all active runner WebSockets
    for tab_id, runner in runners.items():
        try:
            await runner.send("morning_report", report_data)
        except Exception:
            pass  # Client might be disconnected

    return {"status": "ok", "broadcasted_to": len(runners)}

@app.get("/api/morning-report")
async def get_morning_report():
    """
    Get latest morning report from JSON file.
    Frontend can poll this or receive via WebSocket.
    """
    import pathlib
    report_file = pathlib.Path.home() / "worker-bee" / "morning-report.json"

    if not report_file.exists():
        return {"error": "No morning report available yet"}

    try:
        with open(report_file, 'r') as f:
            import json
            return json.load(f)
    except Exception as e:
        return {"error": f"Error reading report: {str(e)}"}

@app.websocket("/ws/voice-daemon")
async def voice_daemon_endpoint(ws: WebSocket):
    global voice_daemon_ws
    await ws.accept()
    voice_daemon_ws = ws
    print("[VOICE DAEMON] Connected")
    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "voice_transcription":
                for runner in runners.values():
                    await runner.send("voice_transcription", msg.get("data", {}))
                    break
    except Exception:
        voice_daemon_ws = None
        print("[VOICE DAEMON] Disconnected")

@app.websocket("/ws/{tab_id}")
async def ws_endpoint(ws: WebSocket, tab_id: str):
    await ws.accept()
    runner = AgentRunner(tab_id, ws)
    runners[tab_id] = runner

    pending = [j for j in jobs.values()
               if j["tab_id"] == tab_id
               and j["status"] == "complete"
               and j.get("result")]
    for job in pending:
        try:
            await ws.send_text(json.dumps({
                "type": "job_complete",
                "data": {
                    "job_id": job["id"],
                    "action": job["action"],
                    "result": job["result"],
                    "progress": job["progress"]
                }
            }))
        except Exception:
            pass

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            action = msg.get("action", "")

            if action in BACKGROUND_ACTIONS:
                # Per-project build locking: prevent multiple builds on same project
                if action in ("build", "build_start"):
                    project = msg.get("project", "")
                    if project:
                        existing_job_id = get_active_build_for_project(project)
                        if existing_job_id:
                            cancel_job(existing_job_id, f"Replaced by new build request")
                            await ws.send_text(json.dumps({
                                "type": "build_replaced",
                                "data": {
                                    "old_job_id": existing_job_id,
                                    "project": project,
                                    "message": f"Cancelled previous build for {project}"
                                }
                            }))

                job_id = create_job(tab_id, action, msg)
                await ws.send_text(json.dumps({
                    "type": "job_started",
                    "data": {
                        "job_id": job_id,
                        "action": action,
                        "message": f"Running in background — job {job_id}"
                    }
                }))
                asyncio.create_task(
                    run_background_job(job_id, tab_id, msg)
                )
            else:
                asyncio.create_task(runner.handle(msg))

    except WebSocketDisconnect:
        runners.pop(tab_id, None)
        await runner.cleanup()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
