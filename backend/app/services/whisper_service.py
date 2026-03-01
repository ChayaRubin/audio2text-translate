# import whisper

# model = whisper.load_model("medium")

# def transcribe_audio(file_path: str):
#     """Returns plain text transcription."""
#     result = model.transcribe(file_path)
#     return result["text"]

# def generate_subtitles(file_path: str):
#     """Returns timestamped segments for subtitles."""
#     result = model.transcribe(file_path)

#     subtitles = []
#     for seg in result.get("segments", []):
#         subtitles.append({
#             "start": float(seg["start"]),
#             "end": float(seg["end"]),
#             "text": seg["text"].strip()
#         })

#     return subtitles
import os
import subprocess
import whisper


model = whisper.load_model("medium")


def extract_audio(input_path: str, output_path: str):
    """
    Extracts audio using ffmpeg (more reliable than MoviePy).
    Always outputs 16kHz mono WAV.
    """
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vn",                   # no video
        "-acodec", "pcm_s16le",  # WAV raw
        "-ar", "16000",          # 16 kHz
        "-ac", "1",              # mono
        output_path,
        "-y"                     # overwrite
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def safe_transcribe(audio_path: str):
    """
    Wrapper around Whisper to catch errors and ensure non-empty audio.
    """
    # Check file exists
    if not os.path.exists(audio_path):
        return {"error": f"Audio file not found: {audio_path}"}

    # Check audio is not empty
    if os.path.getsize(audio_path) < 500:
        return {"error": "Audio file is empty or contains silence."}

    # Whisper transcription
    try:
        result = model.transcribe(audio_path)
        return result
    except Exception as e:
        return {"error": str(e)}


def transcribe_audio(file_path: str):
    """
    Transcribes audio or extracts audio from video first.
    Returns plain text.
    """

    # If file is video → extract audio
    if file_path.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):
        audio_path = file_path + ".wav"
        extract_audio(file_path, audio_path)
    else:
        audio_path = file_path

    # Whisper transcription
    result = safe_transcribe(audio_path)

    # Handle errors
    if "error" in result:
        return result["error"]

    return result.get("text", "").strip()


def generate_subtitles(file_path: str):
    """
    Generates timestamped subtitle segments from audio/video.
    """

    # If file is video → extract audio
    if file_path.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):
        audio_path = file_path + ".wav"
        extract_audio(file_path, audio_path)
    else:
        audio_path = file_path

    # Whisper transcription
    result = safe_transcribe(audio_path)

    if "error" in result:
        return []

    segments = result.get("segments", [])
    subtitles = []

    for seg in segments:
        subtitles.append({
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": seg["text"].strip()
        })

    return subtitles

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def generate_srt(subtitle_segments):
    """Convert Whisper segments into SRT file content."""
    srt_lines = []
    for i, seg in enumerate(subtitle_segments, start=1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"]

        srt_lines.append(f"{i}")
        srt_lines.append(f"{start} --> {end}")
        srt_lines.append(text)
        srt_lines.append("")  # empty line after each block

    return "\n".join(srt_lines)

def generate_vtt(subtitle_segments):
    """Convert Whisper segments into WebVTT format."""
    vtt_lines = ["WEBVTT\n"]

    for seg in subtitle_segments:
        start = format_timestamp(seg["start"]).replace(",", ".")
        end = format_timestamp(seg["end"]).replace(",", ".")
        text = seg["text"]

        vtt_lines.append(f"{start} --> {end}")
        vtt_lines.append(text)
        vtt_lines.append("")  # empty line

    return "\n".join(vtt_lines)
