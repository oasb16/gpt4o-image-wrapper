
import streamlit as st
import openai
import boto3
import uuid
from PIL import Image
from io import BytesIO
from streamtoolkit_omkar.config.env import OPENAI_API_KEY, AWS_REGION, S3_BUCKET
from modules.image_gen import generate_image
from modules.utils import generate_instagram_link, generate_download_link

openai.api_key = OPENAI_API_KEY
s3 = boto3.client("s3", region_name=AWS_REGION)

st.set_page_config(page_title="GPT-4o Image Wrapper", layout="centered")
st.title("🖼️ GPT-4o Prompt/Image to Anime")

uploaded_image = st.file_uploader("📤 Upload an image (optional)", type=["png", "jpg", "jpeg"])
prompt = st.text_area("Or enter a text prompt")

if st.button("Generate / Upload") and (prompt or uploaded_image):
    with st.spinner("Processing..."):
        if uploaded_image:
            img_bytes = uploaded_image.read()
            file_id = f"user_uploads/{uuid.uuid4()}.png"
            s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"
            st.image(img_bytes, caption="📤 Uploaded Image")
            st.success(f"Uploaded to S3: {s3_url}")

        if prompt:
            image_url = generate_image(prompt)
            st.image(image_url, caption="🎨 Generated Image")
            st.markdown(generate_download_link(image_url), unsafe_allow_html=True)
            st.markdown(generate_instagram_link(image_url), unsafe_allow_html=True)
