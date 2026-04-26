#!/usr/bin/env python3
"""
Worker Bee Voice Daemon
Runs in background, watches for voice requests,
records and transcribes, sends results back.
"""
import asyncio, pathlib, json, ssl
import websockets
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav_io

TRIGGER = pathlib.Path("/tmp/wb_voice_trigger")
WAV_PATH = pathlib.Path("/tmp/wb_voice_daemon.wav")
WS_URL   = "wss://localhost:8000/ws/voice-daemon"
SAMPLE_RATE = 16000
SECONDS     = 5
GAIN        = 15

print("🎙 Worker Bee Voice Daemon starting...")
model = whisper.load_model("base")
print("✅ Whisper loaded")

async def record_and_transcribe() -> str:
    print("🎙 Recording...")
    recording = sd.rec(
        int(SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )
    sd.wait()
    recording = np.clip(
        recording * GAIN,
        -32768, 32767
    ).astype(np.int16)
    wav_io.write(str(WAV_PATH), SAMPLE_RATE, recording)
    print("📝 Transcribing...")
    result = model.transcribe(
        str(WAV_PATH),
        language="en",
        fp16=False
    )
    text = result["text"].strip()
    print(f"✅ Heard: {text}")
    return text

async def daemon():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    print(f"🔌 Connecting to {WS_URL}...")

    async with websockets.connect(
        WS_URL, ssl=ssl_ctx
    ) as ws:
        print("✅ Voice daemon connected")

        async def send(t, d):
            await ws.send(json.dumps(
                {"type": t, "data": d}))

        while True:
            try:
                # Wait for voice request from agent
                msg = await asyncio.wait_for(
                    ws.recv(), timeout=30)
                data = json.loads(msg)

                if data.get("type") == "voice_request":
                    text = await record_and_transcribe()
                    if text:
                        await send("voice_transcription",
                            {"text": text})
                    else:
                        await send("voice_error",
                            {"message": "No speech detected"})

                elif data.get("type") == "ping":
                    await send("pong", {})

            except asyncio.TimeoutError:
                # Send keepalive
                await send("daemon_alive", {})
            except Exception as e:
                print(f"Daemon error: {e}")
                await asyncio.sleep(2)
                break

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(daemon())
        except KeyboardInterrupt:
            print("\n🐝 Voice daemon stopped")
            break
        except Exception as e:
            print(f"Reconnecting: {e}")
            asyncio.sleep(3)
