from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

from app.services.whisper_service import (
    generate_subtitles,
    generate_srt,
    generate_vtt
)

router = APIRouter(prefix="/subtitles", tags=["subtitles"])

@router.post("/generate")
async def subtitles_route(
    file: UploadFile = File(...),
    format: str = "srt"   # "srt" | "vtt" | "json"
):
    """
    Upload audio/video → return subtitles in segments + srt/vtt.
    """

    # Save uploaded file safely
    suffix = Path(file.filename).suffix or ".tmp"
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Generate Whisper segments
    segments = generate_subtitles(tmp_path)

    if not segments:
        raise HTTPException(status_code=400, detail="Could not generate subtitles")

    # Return JSON only
    if format == "json":
        return {"segments": segments}

    # Return VTT
    if format == "vtt":
        vtt_text = generate_vtt(segments)
        return {"segments": segments, "vtt": vtt_text}

    # Default: SRT
    srt_text = generate_srt(segments)
    return {"segments": segments, "srt": srt_text}
