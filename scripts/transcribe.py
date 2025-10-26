import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = lambda: ssl_context

import whisper

def transcribe_video(video_path):
    model = whisper.load_model("medium")
    result = model.transcribe(video_path)
    return result['segments']  # List of segments with start, end, text