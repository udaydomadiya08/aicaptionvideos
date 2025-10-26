import sys, os


import streamlit as st
from transcribe import transcribe_video
from generate_srt import segments_to_srt
from rewrite_captions_gemini import rewrite_captions
from overlay import overlay_captions

st.set_page_config(page_title="AI Caption Generator", layout="wide")
st.title("🎬 AI Video Caption Generator")

# Upload video
video_file = st.file_uploader("Upload your video", type=["mp4", "mov"])
style = st.selectbox("Caption Style", ["casual", "formal", "aesthetic"])
lang = st.selectbox("Language", ["en", "hi", "es", "fr", "de", "ja", "ko", "zh"])

if st.button("Generate Captions"):
    if video_file is None:
        st.error("❌ Please upload a video first!")
    else:
        temp_video_path = f"temp_{video_file.name}"
        with open(temp_video_path, "wb") as f:
            f.write(video_file.read())

        st.info("🔹 Transcribing video...")
        segments = transcribe_video(temp_video_path)

        if not segments:
            st.error("❌ No transcription found.")
        else:
            st.info("🔹 Rewriting captions via Gemini API...")
            for i, seg in enumerate(segments):
                seg["text"] = rewrite_captions(seg["text"], style=style, lang=lang).text
                st.text(f"Segment {i+1}: {seg['text']}")

            srt_path = "output.srt"
            st.info("🔹 Generating SRT file...")
            segments_to_srt(segments, srt_path)

            output_video_path = "output.mp4"
            st.info("🔹 Overlaying captions...")
            overlay_captions(temp_video_path, srt_path, output_video_path)

            st.success(f"✅ Done! Video saved as {output_video_path}")
            st.video(output_video_path)
            st.download_button(
                "💾 Download Video",
                data=open(output_video_path, "rb").read(),
                file_name="output_captions.mp4"
            )

        # Cleanup
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
