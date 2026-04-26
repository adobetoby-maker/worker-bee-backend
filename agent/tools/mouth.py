import asyncio, pathlib, subprocess, base64
import numpy as np

_kokoro = None

def get_kokoro():
    global _kokoro
    if _kokoro is None:
        try:
            from kokoro import KPipeline
            _kokoro = KPipeline(lang_code="a")
            print("[MOUTH] Kokoro ready")
        except Exception as e:
            print(f"[MOUTH] Kokoro unavailable: {e}")
            return None
    return _kokoro

async def speak(text: str, 
                voice: str = "af_sky",
                speed: float = 1.0,
                play: bool = True) -> dict:
    """
    Convert text to speech and optionally play it.
    Returns base64 audio for streaming to browser.
    """
    try:
        import scipy.io.wavfile as wav
        import io

        kokoro = get_kokoro()
        if not kokoro:
            # Fallback to macOS say command
            proc = await asyncio.create_subprocess_shell(
                f'say "{text}"',
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await proc.wait()
            return {"success": True, "text": text, 
                    "method": "macos_say"}

        # Generate audio with Kokoro
        samples, rate = kokoro.create(
            text, voice=voice, speed=speed, lang="en-us")
        
        # Save to wav
        wav_path = pathlib.Path("/tmp/workerbee_speech.wav")
        wav.write(str(wav_path), rate, 
                  samples.astype(np.float32))
        
        # Play it
        if play:
            proc = await asyncio.create_subprocess_shell(
                f"afplay {wav_path}",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await proc.wait()
        
        # Return base64 for browser playback
        audio_b64 = base64.b64encode(
            wav_path.read_bytes()).decode()
        
        return {
            "success": True,
            "text": text,
            "audio_b64": audio_b64,
            "rate": rate,
            "method": "kokoro"
        }
        
    except Exception as e:
        # Final fallback — macOS say
        try:
            proc = await asyncio.create_subprocess_shell(
                f'say "{text}"',
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await proc.wait()
            return {"success": True, "text": text,
                    "method": "macos_say_fallback"}
        except:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    async def test():
        print("Testing voice...")
        result = await speak(
            "Hello Toby. Worker Bee is online and ready.",
            voice="af_sky"
        )
        print(f"Result: {result}")
    asyncio.run(test())
