import moviepy.editor as mp
import os

def extract_audio_from_video(video_path: str) -> str:
    audio_path = video_path + ".wav"

    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    return audio_path
