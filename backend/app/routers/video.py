from fastapi import APIRouter, UploadFile, File, Query
import os

from app.services.video_service import extract_audio_from_video
from app.services.whisper_service import transcribe_audio
from app.services.translate_service import translate_text

router = APIRouter()

@router.post("/translate")
async def translate_video(
    file: UploadFile = File(...),
    target_lang: str = Query("he")
):
    TEMP_DIR = "temp"
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Save uploaded video
    video_path = os.path.join(TEMP_DIR, file.filename)
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # Extract audio
    audio_path = extract_audio_from_video(video_path)

    # Transcribe
    original = transcribe_audio(audio_path)

    if not original.strip():
        return {"error": "No speech detected in video"}

    # Translate
    translated = translate_text(original, "en", target_lang)

    return {
        "originalText": original,
        "translatedText": translated,
        "targetLang": target_lang
    }
