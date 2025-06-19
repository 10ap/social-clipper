import streamlit as st
import yt_dlp
import whisper
import os

st.set_page_config(page_title="AI Clip Transcriber", layout="centered")
st.title("🎥 YouTube Video Transcriber")
st.write("Paste a YouTube URL and get a timestamped transcript using Whisper AI.")

# Input for YouTube URL
video_url = st.text_input("Enter YouTube video URL:")

if video_url:
    filename = "downloaded_video.mp4"

    with st.spinner("⬇️ Downloading video..."):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': filename,
            'merge_output_format': 'mp4',
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            st.error(f"❌ Download failed: {e}")
            st.stop()

        if not os.path.exists(filename) or os.path.getsize(filename) < 100000:
            st.error("❌ Downloaded file is missing or too small.")
            st.stop()

    st.success("✅ Video downloaded successfully!")

    with st.spinner("🧠 Transcribing with Whisper..."):
        try:
            model = whisper.load_model("base")
            result = model.transcribe(filename)
        except Exception as e:
            st.error(f"❌ Transcription failed: {e}")
            st.stop()

    st.success("✅ Transcription complete!")

    # Display transcript
    st.subheader("📝 Transcript with Timestamps")
    for segment in result["segments"]:
        start = round(segment["start"], 2)
        end = round(segment["end"], 2)
        text = segment["text"]
        st.markdown(f"**[{start} - {end}]** {text}")
