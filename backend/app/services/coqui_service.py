import os
import uuid
from pathlib import Path
from TTS.api import TTS

# Directory where generated audio files will be saved
OUTPUT_DIR = Path("generated_audio")
OUTPUT_DIR.mkdir(exist_ok=True)

# Load a simple Coqui TTS model (English)
# You can later switch to multilingual model if needed.
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)


def text_to_speech(text: str) -> str:
    """Generate speech audio from text. Returns path to WAV file."""

    filename = OUTPUT_DIR / f"{uuid.uuid4()}.wav"

    tts.tts_to_file(
        text=text,
        file_path=str(filename),
    )

    return str(filename)
