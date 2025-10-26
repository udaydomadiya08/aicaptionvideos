from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt

def overlay_captions(video_path, srt_path, output_path="output.mp4"):
    video = VideoFileClip(video_path)
    subs = pysrt.open(srt_path)
    
    txt_clips = []
    max_height_ratio = 0.25  # max 25% of video height

    for sub in subs:
        fontsize = 40
        txt = TextClip(
            sub.text,
            fontsize=fontsize,
            color='white',
            bg_color='rgba(0,0,0,0.6)',
            method='caption',
            size=(video.w - 20, int(video.h * max_height_ratio))
        )

        while txt.h > video.h * max_height_ratio and fontsize > 10:
            fontsize -= 2
            txt = TextClip(
                sub.text,
                fontsize=fontsize,
                color='white',
                bg_color='rgba(0,0,0,0.6)',
                method='caption',
                size=(video.w - 20, int(video.h * max_height_ratio))
            )

        txt = txt.set_start(sub.start.seconds).set_end(sub.end.seconds).set_position(('center', 'bottom'))
        txt_clips.append(txt)

    # Composite the video and text clips
    final = CompositeVideoClip([video, *txt_clips])
    
    # Add back the original audio
    final = final.set_audio(video.audio)

    final.write_videofile(output_path, codec='libx264', fps=video.fps, audio_codec='aac')
