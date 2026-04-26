import asyncio, pathlib, subprocess, tempfile
import whisper
import torch

# Load model once at startup
_model = None

def get_model():
    global _model
    if _model is None:
        device = "cpu"  # whisper small works fine on cpu
        _model = whisper.load_model("small", device=device)
    return _model

async def listen(seconds: int = 5, 
                 gain: int = 15) -> dict:
    """
    Record from microphone and transcribe with Whisper.
    Returns transcribed text.
    """
    wav_path = pathlib.Path("/tmp/workerbee_listen.wav")
    
    try:
        # Record using sounddevice (works without terminal)
        import sounddevice as sd
        import scipy.io.wavfile as wav_io
        import numpy as np
        
        sample_rate = 16000
        recording = sd.rec(
            int(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()  # Wait for recording to finish
        
        # Apply gain
        recording = np.clip(
            recording * (gain / 5), 
            -32768, 32767
        ).astype(np.int16)
        
        wav_io.write(str(wav_path), sample_rate, recording)
        
        if not wav_path.exists():
            return {"success": False, "error": "Recording failed"}
        
        # Transcribe
        model = get_model()
        result = model.transcribe(
            str(wav_path), 
            language="en",
            fp16=False
        )
        
        text = result["text"].strip()
        
        return {
            "success": True,
            "text": text,
            "language": result.get("language", "en")
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

async def listen_continuous(callback, 
                             stop_event=None,
                             seconds_per_chunk: int = 5):
    """
    Continuous listening loop.
    Calls callback(text) for each transcribed chunk.
    Stop by setting stop_event.
    """
    while not (stop_event and stop_event.is_set()):
        result = await listen(seconds=seconds_per_chunk)
        if result.get("success") and result.get("text"):
            await callback(result["text"])
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    async def test():
        print("Listening for 5 seconds... speak now!")
        result = await listen(5)
        print(f"Heard: {result}")
    asyncio.run(test())
