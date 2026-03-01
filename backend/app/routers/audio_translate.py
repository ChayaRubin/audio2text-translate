from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

from app.services.whisper_service import safe_transcribe
from app.services.translate_service import translate_text
from app.services.coqui_service import text_to_speech

router = APIRouter(prefix="/audio", tags=["audio"])


@router.post("/translate")
async def audio_translate(
    file: UploadFile = File(...),
    source_lang: str = Form("en"),
    target_lang: str = Form("he"),
):
    """
    Upload audio → Whisper → Helsinki → Coqui TTS
    Returns: translated text + path to synthesized audio.
    """

    # Save file temporarily
    suffix = Path(file.filename or "").suffix or ".tmp"
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Step 1 — Transcribe using Whisper
    whisper_result = safe_transcribe(tmp_path)
    if "error" in whisper_result:
        raise HTTPException(status_code=400, detail=whisper_result["error"])

    original_text = whisper_result.get("text", "").strip()

    # Step 2 — Translate using Helsinki
    translated_text = translate_text(
        original_text,
        source_lang=source_lang,
        target_lang=target_lang,
    )

    # Step 3 — Generate speech using Coqui TTS
    generated_audio_path = text_to_speech(translated_text)

    # URL for frontend (FastAPI will serve static folder)
    audio_filename = Path(generated_audio_path).name
    audio_url = f"/static/audio/{audio_filename}"

    return {
        "originalText": original_text,
        "translatedText": translated_text,
        "targetLang": target_lang,
        "audioUrl": audio_url
    }
