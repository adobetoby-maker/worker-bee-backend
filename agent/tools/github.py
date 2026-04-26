import httpx, os, base64, json

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

class GitHubTool:
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WorkerBee-Agent"
        }
        if GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {GITHUB_TOKEN}"

    async def get_file(self, owner: str, repo: str,
                       path: str) -> dict:
        """Fetch a single file from GitHub"""
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url, headers=self.headers)
            if r.status_code != 200:
                return {"error": f"HTTP {r.status_code}",
                        "success": False}
            data = r.json()
            content = base64.b64decode(
                data["content"]).decode("utf-8")
            return {
                "path": path,
                "content": content,
                "size": data["size"],
                "sha": data["sha"],
                "success": True
            }

    async def list_files(self, owner: str, repo: str,
                         path: str = "") -> dict:
        """List files in a directory"""
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url, headers=self.headers)
            if r.status_code != 200:
                return {"error": f"HTTP {r.status_code}",
                        "success": False}
            items = r.json()
            return {
                "path": path,
                "items": [{"name": i["name"],
                           "type": i["type"],
                           "path": i["path"],
                           "size": i.get("size", 0)}
                          for i in items],
                "success": True
            }

    async def get_repo_structure(self, owner: str,
                                  repo: str) -> dict:
        """Get full repo file tree"""
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url, headers=self.headers)
            if r.status_code != 200:
                return {"error": f"HTTP {r.status_code}",
                        "success": False}
            tree = r.json().get("tree", [])
            return {
                "files": [t["path"] for t in tree
                         if t["type"] == "blob"],
                "success": True
            }

    async def get_multiple_files(self, owner: str,
                                  repo: str,
                                  paths: list) -> dict:
        """Fetch multiple files at once"""
        results = {}
        for path in paths:
            result = await self.get_file(owner, repo, path)
            if result.get("success"):
                results[path] = result["content"]
            else:
                results[path] = f"ERROR: {result.get('error')}"
        return {"files": results, "success": True}

    async def push_file(self, owner: str, repo: str,
                        path: str, content: str,
                        message: str = "Worker Bee update",
                        sha: str = None) -> dict:
        """Push a file to GitHub"""
        if not GITHUB_TOKEN:
            return {"error": "No GITHUB_TOKEN set",
                    "success": False}
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        body = {
            "message": message,
            "content": base64.b64encode(
                content.encode()).decode()
        }
        if sha:
            body["sha"] = sha
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.put(url, headers=self.headers,
                           json=body)
            return {
                "success": r.status_code in [200, 201],
                "status": r.status_code,
                "path": path
            }
