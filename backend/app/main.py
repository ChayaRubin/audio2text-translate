from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.services.translate_service import translate_text

# Routers
from app.routers import (
    auth,
    translate,
    subtitles,
    audio_translate,
    video,
    billing,
    text_translate,
)

app = FastAPI(title="Octavia Backend")

# ------------------------------
# CORS
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Health check
# ------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ------------------------------
# Routers
# ------------------------------
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(translate.router, prefix="/translate", tags=["Translate"])
app.include_router(subtitles.router, prefix="/subtitles", tags=["Subtitles"])
app.include_router(audio_translate.router, prefix="/audio", tags=["Audio"])
app.include_router(video.router, prefix="/video", tags=["Video"])
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(text_translate.router, prefix="/translate-text", tags=["Text"])


# ------------------------------
# Serve TTS audio output
# ------------------------------
app.mount(
    "/static/audio",
    StaticFiles(directory="generated_audio"),
    name="generated-audio"
)
