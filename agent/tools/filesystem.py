import pathlib

SAFE = pathlib.Path.home() / "worker-bee" / "projects"

class FilesystemTool:
    def __init__(self):
        SAFE.mkdir(parents=True, exist_ok=True)

    def _safe(self, path: str) -> pathlib.Path:
        p = (SAFE / path).resolve()
        if not str(p).startswith(str(SAFE)):
            raise PermissionError(f"Path outside safe root: {path}")
        return p

    def read(self, path: str) -> str:
        return self._safe(path).read_text(encoding="utf-8")

    def write(self, path: str, content: str) -> str:
        p = self._safe(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Written {len(content)} chars to {path}"

    def list_dir(self, path: str = "") -> list:
        return [str(f.relative_to(SAFE))
                for f in self._safe(path).iterdir()]

    def delete(self, path: str) -> str:
        self._safe(path).unlink()
        return f"Deleted {path}"

    def exists(self, path: str) -> bool:
        return self._safe(path).exists()
