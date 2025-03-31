
import streamlit as st
from PIL import Image
from io import BytesIO
import uuid
import boto3
import openai
import os

# Config from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
AWS_REGION = st.secrets["AWS_REGION"]
S3_BUCKET = st.secrets["S3_BUCKET"]
AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]

# AWS client
s3 = boto3.client("s3", region_name=AWS_REGION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_to_s3(file_bytes, filename):
    s3.upload_fileobj(file_bytes, S3_BUCKET, filename)
    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"

def generate_image(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=f"Convert this {prompt} into a modern anime style with Ghibli influence, clean line art, realistic shading, soft pastel tones, and expressive faces. Inspired by scenes from 'Your Name' and 'Whisper of the Heart'. Emphasize clarity, color harmony, and emotional warmth.",
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

st.set_page_config(page_title="🎨 GPT-4o Ghibli Generator", layout="centered")
st.title("🎨 Upload or Prompt to Ghibli Image")

uploaded_file = st.file_uploader("📤 Upload an image (optional)", type=["png", "jpg", "jpeg"])
prompt = st.text_input("📝 Or enter a prompt for the image")

final_prompt = prompt.strip()

if uploaded_file:
    uploaded_bytes = uploaded_file.read()
    uploaded_image = Image.open(BytesIO(uploaded_bytes))
    st.image(uploaded_image, caption="📤 Uploaded Image", use_container_width=True)

if st.button("🚀 Generate / Upload"):
    if uploaded_file:
        filename = f"uploads/{uuid.uuid4()}.png"
        url = upload_to_s3(BytesIO(uploaded_bytes), filename)
        st.success(f"✅ Uploaded to S3: {url}")

    if final_prompt:
        with st.spinner("🎨 Generating..."):
            try:
                image_url = generate_image(final_prompt)
                st.image(image_url, caption="✨ Ghibli-style by GPT-4o", use_container_width=True)
                st.markdown(f"[📥 Download Image]({image_url})", unsafe_allow_html=True)
                st.markdown(f"[📸 Share on Instagram](https://instagram.com)", unsafe_allow_html=True)
            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)
