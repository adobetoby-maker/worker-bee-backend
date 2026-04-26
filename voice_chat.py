#!/usr/bin/env python3
"""
Worker Bee Voice Chat — Terminal Edition
Speak naturally, Worker Bee responds and remembers.
Press Enter to speak, Ctrl+C to exit.
"""
import asyncio, httpx, json, pathlib
from datetime import datetime
from dotenv import dotenv_values
from agent.tools.ears import listen
from agent.tools.mouth import speak
from agent.tools.memory import MemoryTool

_env = dotenv_values(str(pathlib.Path.home() / "worker-bee" / ".env"))
OLLAMA = _env.get("OLLAMA_HOST", "http://localhost:11434")

# Shared memory — same ChromaDB as the web UI
memory = MemoryTool(tab_id="voice-chat")

# Conversation history
history = []

SYSTEM = """You are Worker Bee, Toby's personal AI assistant.
You are speaking out loud so keep responses conversational,
concise and natural. No markdown, no bullet points — 
just natural speech. 2-4 sentences unless asked for more.

You have persistent memory of all past conversations.
When Toby shares ideas, plans, or insights — remember them.
When asked about something from before — recall it.

Toby is an orthopedic surgeon, web designer, and 
deep thinker building AI-powered apps including:
- Worker Bee (this agent)
- LinguaLens (language learning app)
- mountainedgeplumbing.com (his brother's business)
"""

async def think(text: str) -> str:
    """Think with llama3.3 using full memory context"""
    
    # Search memory for relevant context
    mem_context = memory.build_context(text)
    
    # Build messages with memory
    system = SYSTEM
    if mem_context:
        system = mem_context + "\n\n" + system
    
    messages = [{"role": "system", "content": system}]
    messages += history[-10:]  # Last 10 exchanges
    messages.append({"role": "user", "content": text})
    
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(f"{OLLAMA}/api/chat", json={
            "model": "llama3.3:70b",
            "messages": messages,
            "stream": False
        })
        return r.json().get("message", {}).get("content", "")

async def remember(user_text: str, bee_response: str):
    """Store conversation in ChromaDB"""
    memory.store_message("user", user_text, "voice")
    memory.store_message("assistant", bee_response, "llama3.3:70b")
    
    # Auto-extract and store ideas/insights
    if any(w in user_text.lower() for w in [
        "idea", "think", "want to", "what if", 
        "could we", "should we", "plan", "build",
        "remember", "note", "important"
    ]):
        memory.store_knowledge(
            topic=f"Voice idea — {datetime.now().strftime('%Y-%m-%d')}",
            content=f"Toby said: {user_text}",
            source="voice-chat"
        )
        print("  💾 Idea stored in memory")

async def voice_loop():
    print("\n🐝 Worker Bee Voice Chat")
    print("=" * 40)
    print("Press Enter → speak for 5 seconds")
    print("Type 'memory' → see what I remember")
    print("Type 'ideas' → list stored ideas")
    print("Type 'clear' → clear screen")
    print("Ctrl+C → exit")
    print("=" * 40)
    
    stats = memory.stats()
    total = stats['conversations'] + stats['knowledge']
    
    greeting = f"Worker Bee online. I have {total} memories stored. What's on your mind?"
    print(f"\nBee: {greeting}")
    await speak(greeting)
    
    while True:
        try:
            cmd = input("\n[Enter to speak / type command] ").strip().lower()
            
            if cmd == "memory":
                stats = memory.stats()
                print(f"\n📊 Memory: {stats['conversations']} conversations, "
                      f"{stats['knowledge']} knowledge entries")
                continue
                
            elif cmd == "ideas":
                results = memory.search_knowledge("idea plan build", n=5)
                if results:
                    print("\n💡 Recent ideas:")
                    for r in results:
                        print(f"  • {r['content'][:100]}")
                else:
                    print("No ideas stored yet")
                continue
                
            elif cmd == "clear":
                print("\033[2J\033[H")
                continue
                
            elif cmd and cmd != "":
                # Text input — send directly
                text = cmd
            else:
                # Voice input
                print("🎙 Listening...")
                heard = await listen(seconds=5, gain=15)
                
                if not heard.get("success") or not heard.get("text"):
                    print("Didn't catch that — try again")
                    continue
                    
                text = heard["text"]
            
            print(f"\nYou: {text}")
            print("🤔 Thinking...")
            
            response = await think(text)
            
            if not response:
                continue
            
            # Add to conversation history
            history.append({"role": "user", "content": text})
            history.append({"role": "assistant", "content": response})
            
            # Store in memory
            await remember(text, response)
            
            print(f"\nBee: {response}")
            await speak(response)
            
        except KeyboardInterrupt:
            print("\n\n🐝 Saving memories and shutting down...")
            stats = memory.stats()
            print(f"   Stored {stats['conversations']} conversations")
            print(f"   Stored {stats['knowledge']} ideas")
            goodbye = "Goodbye Toby. Your ideas are saved."
            print(f"\nBee: {goodbye}")
            await speak(goodbye)
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(voice_loop())
