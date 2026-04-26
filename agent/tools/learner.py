import httpx, asyncio, pathlib, json, os, re
from datetime import datetime
from dotenv import dotenv_values

_env = dotenv_values(str(pathlib.Path.home() / "worker-bee" / ".env"))
OLLAMA = _env.get("OLLAMA_HOST", "http://localhost:11434")

SOURCES = [
    # 3D and immersive web
    {"url": "https://threejs.org/examples/", "topic": "Three.js 3D web experiences"},
    {"url": "https://tympanus.net/codrops/", "topic": "creative 3D web design and animations"},
    {"url": "https://www.awwwards.com/websites/three-js/", "topic": "award winning 3D websites"},
    {"url": "https://gsap.com/blog/", "topic": "GSAP animation and scroll effects"},
    {"url": "https://css-tricks.com/", "topic": "advanced CSS effects and 3D transforms"},
    {"url": "https://tympanus.net/codrops/category/tutorials/", "topic": "WebGL and 3D tutorials"},
    {"url": "https://www.smashingmagazine.com/", "topic": "web design best practices"},
    # App building
    {"url": "https://www.joshwcomeau.com/", "topic": "React and CSS advanced techniques"},
    {"url": "https://ui.dev/", "topic": "modern JavaScript and React patterns"},
    {"url": "https://kentcdodds.com/blog", "topic": "React best practices and testing"},
    {"url": "https://supabase.com/blog", "topic": "Supabase and backend patterns"},
    # Business and conversion
    {"url": "https://getjobber.com/academy/", "topic": "field service business"},
    {"url": "https://wptavern.com/", "topic": "WordPress best practices"},
    {"url": "https://simonwillison.net/", "topic": "AI agents and LLMs"},
]

async def fetch_page(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 WorkerBee-Learner"}) as c:
            r = await c.get(url)
            if r.status_code != 200:
                return ""
            text = re.sub(r'<script[^>]*>.*?</script>', '', r.text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:8000]
    except Exception as e:
        print(f"Fetch error {url}: {e}")
        return ""

async def extract_insights(text: str, topic: str, url: str) -> str:
    prompt = f"""Extract the 3-5 most valuable actionable insights from this content about {topic}.
URL: {url}
CONTENT: {text[:4000]}
Format as bullet points. Be specific and practical.
Focus on insights that help build better websites or improve customer experience."""
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{OLLAMA}/api/chat", json={
                "model": "qwen2.5-coder:32b",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            })
            return r.json().get("message", {}).get("content", "")
    except Exception as e:
        return f"Extract error: {e}"

async def learn_session(memory=None, log_fn=None):
    async def log(msg):
        print(f"[LEARNER] {msg}")
        if log_fn:
            await log_fn(msg)

    await log(f"Learning session started — {len(SOURCES)} sources")
    learned = 0

    for source in SOURCES:
        try:
            await log(f"Reading: {source['url']}")
            text = await fetch_page(source["url"])
            if not text:
                continue
            insights = await extract_insights(text, source["topic"], source["url"])
            if memory and insights and len(insights) > 50:
                memory.store_knowledge(
                    topic=f"Auto-learned: {source['topic']}",
                    content=insights,
                    source=f"{source['url']} — {datetime.now().strftime('%Y-%m-%d')}"
                )
                await log(f"Stored insights from {source['url']}")
            learned += 1
            await asyncio.sleep(5)
        except Exception as e:
            await log(f"Error with {source['url']}: {e}")

    await log(f"Complete — {learned}/{len(SOURCES)} sources processed")
    return learned

if __name__ == "__main__":
    asyncio.run(learn_session())
