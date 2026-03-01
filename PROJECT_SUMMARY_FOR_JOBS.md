# audio2text-translate — Project Summary for Job Applications (Python)

Use the text below on your resume, LinkedIn, or cover letter when applying for Python roles.

---

## One-line description

**Audio-to-Text & Translate** — Python backend that transcribes audio/video, translates text (multiple languages), and generates speech using ML models (Whisper, MarianMT, Coqui TTS).

---

## Short paragraph (cover letter / “About” section)

Built a **Python** backend service that turns audio and video into text, translates it between languages, and can speak the result. The API is built with **FastAPI** (async endpoints, file uploads, structured request/response with **Pydantic**). It uses **OpenAI Whisper** for speech-to-text, **Hugging Face MarianMT** for translation, **Coqui TTS** for text-to-speech, and **MoviePy**/ffmpeg for extracting audio from video. The app handles uploads, temp files, subprocess calls, and exposes REST endpoints for transcription, translation, subtitles (SRT/VTT), and billing/auth flows—demonstrating Python for APIs, ML integration, and media processing.

---

## Resume bullet points (pick 2–3)

- **Developed a Python/FastAPI backend** for an audio-to-text and translation service: speech-to-text (Whisper), multilingual translation (Hugging Face MarianMT), text-to-speech (Coqui TTS), and subtitle generation (SRT/VTT).
- **Integrated ML and media pipelines in Python**: Whisper for transcription, transformers for translation, subprocess/ffmpeg for audio extraction, and async file handling for uploads and temporary files.
- **Built REST APIs in Python** with FastAPI: async route handlers, Pydantic models, file uploads, CORS, static file serving, and modular routers for auth, billing, translation, and media processing.
- **Implemented media and text processing in Python**: video/audio handling (MoviePy, ffmpeg), timestamp formatting, subtitle generation, and error handling around external tools and ML inference.

---

## Keywords to include (for ATS and recruiters)

Python • FastAPI • REST API • Pydantic • async • Whisper • Hugging Face • Transformers • MarianMT • Coqui TTS • speech-to-text • machine learning • NLP • translation • subprocess • file I/O • MoviePy • ffmpeg • SRT/VTT • backend development

---

## If the job emphasizes…

| Job focus           | What to say |
|--------------------|-------------|
| **APIs / Backend** | FastAPI, async endpoints, Pydantic, file uploads, REST, modular routers. |
| **ML / NLP**       | Whisper (speech-to-text), Hugging Face MarianMT (translation), Coqui TTS (text-to-speech). |
| **Python quality** | Type hints, Pydantic models, structured error handling, separation of services and routers. |
| **Integrations**   | Subprocess (ffmpeg), file and temp file handling, external ML libraries and APIs. |

---

## Link to show the code

**GitHub:** https://github.com/ChayaRubin/audio2text-translate
