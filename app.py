import streamlit as st
import uuid
from io import BytesIO
from modules.gpt import generate_image, transcribe_audio
from modules.upload import upload_file_to_s3
from modules.share import generate_download_link, generate_instagram_share_link

st.set_page_config(page_title="GPT-4o Image Wrapper", layout="centered")
st.title("🧠 GPT-4o: Whisper + Image + S3 + Share")

st.session_state.setdefault("user_id", str(uuid.uuid4()))
user_id = st.session_state["user_id"]

st.markdown(f"🔐 Your Session ID: `{user_id[:8]}`")

st.markdown("### Enter Prompt or Upload Audio File")
prompt = st.text_input("Prompt (or leave blank to use audio)")

audio_file = st.file_uploader("🎤 Upload audio (.mp3 or .wav)", type=["mp3", "wav"])
audio_text = ""

if audio_file:
    st.audio(audio_file)
    with st.spinner("Transcribing..."):
        audio_text = transcribe_audio(audio_file)
    st.success("Transcription complete!")
    st.markdown(f"📝 Transcribed: `{audio_text}`")

final_prompt = prompt or audio_text

if st.button("🎨 Generate Image") and final_prompt:
    with st.spinner("Generating and uploading..."):
        image_url = generate_image(final_prompt)
        image_data = BytesIO()
        image_data.write(image_url.encode())
        image_data.seek(0)

        file_id = f"{user_id}/images/{uuid.uuid4()}.txt"
        s3_url = upload_file_to_s3(image_data, file_id)

        st.image(image_url, caption="Generated Image", use_container_width=True)
        st.markdown(generate_download_link(image_url), unsafe_allow_html=True)
        st.markdown(f"[📸 Share on Instagram]({generate_instagram_share_link(image_url)})")
