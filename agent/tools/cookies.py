import json, pathlib

COOKIE_DIR = pathlib.Path.home() / "worker-bee" / ".cookies"
COOKIE_DIR.mkdir(exist_ok=True)

def save_cookies(domain: str, cookies: list) -> str:
    path = COOKIE_DIR / f"{domain.replace('.', '_')}.json"
    path.write_text(json.dumps(cookies, indent=2))
    return str(path)

def load_cookies(domain: str) -> list:
    path = COOKIE_DIR / f"{domain.replace('.', '_')}.json"
    if not path.exists():
        return []
    return json.loads(path.read_text())

def list_saved() -> list:
    return [f.stem.replace('_', '.') 
            for f in COOKIE_DIR.glob("*.json")]
