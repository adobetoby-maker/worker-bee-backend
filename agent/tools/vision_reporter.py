import httpx, base64, os, json, pathlib
from datetime import datetime
from dotenv import dotenv_values as _dv

_env = _dv(str(pathlib.Path.home() / "worker-bee" / ".env"))
GITHUB_TOKEN      = _env.get("GITHUB_TOKEN", "")
VISION_REPO_OWNER = _env.get("VISION_REPO_OWNER", "adobetoby-maker")
VISION_REPO_NAME  = _env.get("VISION_REPO_NAME", "worker-bee-vision")

class VisionReporter:
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WorkerBee-Agent",
            "Authorization": f"token {GITHUB_TOKEN}"
        }

    async def push_screenshot(self, 
                               screenshot_b64: str,
                               label: str = "",
                               description: str = "") -> dict:
        """Push a screenshot to the vision repo"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_label = label.replace(" ", "_").replace("/", "_")[:30]
        filename = f"screenshots/{ts}_{safe_label}.png"
        
        # Push image
        url = (f"https://api.github.com/repos/"
               f"{VISION_REPO_OWNER}/{VISION_REPO_NAME}"
               f"/contents/{filename}")
        
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.put(url, headers=self.headers, json={
                "message": f"Worker Bee screenshot: {label}",
                "content": screenshot_b64
            })
            
        if r.status_code not in [200, 201]:
            return {"success": False, 
                    "error": f"HTTP {r.status_code}"}

        # Update the README with latest screenshot
        await self.update_readme(filename, label, 
                                  description, ts)
        
        raw_url = (f"https://raw.githubusercontent.com/"
                   f"{VISION_REPO_OWNER}/{VISION_REPO_NAME}"
                   f"/main/{filename}")
        
        return {
            "success": True,
            "filename": filename,
            "url": raw_url,
            "github_url": (f"https://github.com/"
                          f"{VISION_REPO_OWNER}/"
                          f"{VISION_REPO_NAME}/blob/main/"
                          f"{filename}")
        }

    async def update_readme(self, filename: str,
                             label: str,
                             description: str,
                             ts: str):
        """Update README with latest screenshot"""
        readme_url = (f"https://api.github.com/repos/"
                      f"{VISION_REPO_OWNER}/{VISION_REPO_NAME}"
                      f"/contents/README.md")
        
        # Get current README sha
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(readme_url, headers=self.headers)
            sha = r.json().get("sha", "") if r.status_code == 200 else ""
        
        raw_url = (f"https://raw.githubusercontent.com/"
                   f"{VISION_REPO_OWNER}/{VISION_REPO_NAME}"
                   f"/main/{filename}")
        
        content = f"""# Worker Bee Vision Log

Latest screenshot taken at {ts}

## {label}
{description}

![Latest Screenshot]({raw_url})

## How To Use
Claude can see these screenshots directly.
Paste the raw URL into Claude for analysis.

## History
See /screenshots folder for all captures.
"""
        
        body = {
            "message": f"Update vision log: {label}",
            "content": base64.b64encode(
                content.encode()).decode()
        }
        if sha:
            body["sha"] = sha
            
        async with httpx.AsyncClient(timeout=15) as c:
            await c.put(readme_url, 
                        headers=self.headers, 
                        json=body)

    async def push_multiple(self, 
                             screenshots: list) -> list:
        """Push multiple screenshots at once"""
        results = []
        for s in screenshots:
            result = await self.push_screenshot(
                s["screenshot_b64"],
                s.get("label", "screenshot"),
                s.get("description", "")
            )
            results.append(result)
        return results

    async def get_latest_url(self) -> str:
        """Get the raw URL of the latest screenshot"""
        url = (f"https://api.github.com/repos/"
               f"{VISION_REPO_OWNER}/{VISION_REPO_NAME}"
               f"/contents/screenshots")
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url, headers=self.headers)
            if r.status_code != 200:
                return ""
            files = r.json()
            if not files:
                return ""
            latest = sorted(
                files, 
                key=lambda x: x["name"],
                reverse=True
            )[0]
            return (f"https://raw.githubusercontent.com/"
                    f"{VISION_REPO_OWNER}/{VISION_REPO_NAME}"
                    f"/main/{latest['path']}")
