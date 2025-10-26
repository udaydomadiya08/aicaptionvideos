import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = lambda: ssl_context

import argparse
import os
from transcribe import transcribe_video
from generate_srt import segments_to_srt
from rewrite_captions_gemini import rewrite_captions  # Updated multi-key Gemini
from overlay import overlay_captions

def main():
    parser = argparse.ArgumentParser(description="Automated Caption Generator")
    parser.add_argument("--video", required=True, help="Path to input video")
    parser.add_argument("--style", default="casual", help="Caption style: casual/formal/aesthetic")
    parser.add_argument("--lang", default="en", help="Language code for captions (e.g., en, hi)")
    parser.add_argument("--srt_output", default="output.srt", help="Path to save generated SRT file")
    parser.add_argument("--video_output", default="output.mp4", help="Path to save final video with captions")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"❌ Video file not found: {args.video}")
        return

    print("🔹 Transcribing video...")
    segments = transcribe_video(args.video)
    if not segments:
        print("❌ No transcription segments found.")
        return

    print("🔹 Rewriting captions via Gemini API...")
    for i, seg in enumerate(segments):
        print(f"   ↪ Processing segment {i+1}/{len(segments)}...")
        response = rewrite_captions(seg["text"], style=args.style, lang=args.lang)
        seg["text"] = response.text

    print(f"🔹 Generating SRT file → {args.srt_output}")
    segments_to_srt(segments, args.srt_output)

    print(f"🔹 Overlaying captions on video → {args.video_output}")
    overlay_captions(args.video, args.srt_output, args.video_output)

    print("✅ Done! Output saved as:", args.video_output)


if __name__ == "__main__":
    main()
