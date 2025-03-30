import streamlit as st
import uuid
from io import BytesIO
from modules.gpt import generate_image
from modules.upload import upload_file_to_s3
from modules.share import generate_instagram_share_link, generate_download_link

st.set_page_config(page_title="GPT-4o Image Wrapper", layout="centered")
st.title("🧠 GPT-4o: Generate + Upload + Share")

st.markdown("### Enter Prompt or Upload Audio File")

prompt = st.text_input("Prompt (or leave blank to use audio)")

audio_file = st.file_uploader("🎤 Upload audio (.mp3 or .wav)", type=["mp3", "wav"])
audio_text = ""

if audio_file:
    st.audio(audio_file)
    st.info("Note: Transcription backend is pending. Using filename as placeholder.")
    audio_text = audio_file.name.split(".")[0]  # Temporary placeholder for demo

final_prompt = prompt or audio_text

if st.button("🎨 Generate Image") and final_prompt:
    with st.spinner("Generating and uploading..."):
        image_url = generate_image(final_prompt)
        image_data = BytesIO()
        image_data.write(image_url.encode())
        image_data.seek(0)

        file_id = f"images/{uuid.uuid4()}.txt"
        s3_url = upload_file_to_s3(image_data, file_id)

        st.image(image_url, caption="Generated Image", use_container_width=True)
        st.markdown(generate_download_link(image_url), unsafe_allow_html=True)
        st.markdown(f"[📸 Share on Instagram]({generate_instagram_share_link(image_url)})")
