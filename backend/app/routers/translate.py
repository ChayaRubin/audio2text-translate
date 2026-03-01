from fastapi import APIRouter, UploadFile, File
from app.services.whisper_service import transcribe_audio
from app.services.video_service import extract_audio_from_video
import os

router = APIRouter()

@router.post("/")
async def generate_subtitles(file: UploadFile = File(...)):
    TEMP_DIR = "temp"
    os.makedirs(TEMP_DIR, exist_ok=True)

    file_path = os.path.join(TEMP_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # If video → extract audio
    if file.filename.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):
        audio_path = extract_audio_from_video(file_path)
    else:
        audio_path = file_path

    # Transcribe audio
    text = transcribe_audio(audio_path)

    return {
        "subtitles": text,
        "format": "plain"
    }
