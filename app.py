import streamlit as st
import uuid
from modules.image_gen import generate_image
from modules.share_utils import generate_download_link, generate_instagram_link
import boto3
from PIL import Image
from io import BytesIO
import os

st.set_page_config(page_title="GPT-4o Image Portal", layout="centered")
st.title("🧠✨ Prompt or Upload → Ghibli-style Image")

# Authenticated user check (mocked fallback)
user_email = st.secrets.get("USER_EMAIL", "demo_user@example.com")
s3 = boto3.client("s3", region_name=st.secrets["AWS_REGION"])

# Input options
prompt = st.text_input("Describe your scene")
uploaded_file = st.file_uploader("Or upload an image", type=["jpg", "jpeg", "png"])
final_prompt = prompt.strip() if prompt else "user-uploaded image"

if st.button("🎨 Generate Image"):
    with st.spinner("Processing..."):
        try:
            if uploaded_file:
                img = Image.open(uploaded_file)
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                key = f"user_uploads/{user_email}/{uuid.uuid4()}.png"
                s3.upload_fileobj(buffer, st.secrets["S3_BUCKET"], key)
                st.success(f"Image uploaded to S3!")
                st.image(img, caption="Uploaded Image", use_container_width=True)

            if prompt:
                image_url = generate_image(final_prompt)
                s3_key = f"generated/{user_email}/{uuid.uuid4()}.png"
                st.image(image_url, caption="Generated Image", use_container_width=True)
                st.markdown(generate_download_link(image_url), unsafe_allow_html=True)
                st.markdown(generate_instagram_link(image_url), unsafe_allow_html=True)

        except Exception as e:
            st.error("Failed to generate or upload image.")
            st.exception(e)