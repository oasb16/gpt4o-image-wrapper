import streamlit as st
import os
import uuid
import boto3
import requests
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
from streamtoolkit_omkar.config.env import AWS_REGION, S3_BUCKET
from modules.utils import generate_download_link, generate_instagram_link

# Credentials from Streamlit Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
AWS_ACCESS_KEY = st.secrets.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = st.secrets.get("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE = st.secrets.get("DYNAMODB_TABLE")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Boto3 S3
s3 = boto3.client("s3", region_name=AWS_REGION)

st.set_page_config(page_title="GPT-4o Image Wrapper", layout="centered")
st.title("🖼️ Upload to Anime (Gemini 2.0 Flash)")

uploaded_image = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])
prompt = st.text_area("Describe how to transform the image")

def generate_edited_image_gemini(image_bytes, prompt_text):
    # Save to local temp file
    temp_filename = f"temp_{uuid.uuid4()}.png"
    with open(temp_filename, "wb") as f:
        f.write(image_bytes)

    # Upload image to Gemini file store
    gemini_file = client.files.upload(file=temp_filename)

    # Construct contents for generation
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=gemini_file.uri,
                    mime_type=gemini_file.mime_type,
                ),
                types.Part.from_text(text=prompt_text),
            ],
        )
    ]

    config = types.GenerateContentConfig(response_mime_type="text/plain")
    result_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=contents,
        config=config,
    ):
        result_text += chunk.text

    return result_text

if st.button("Generate"):
    if uploaded_image and prompt:
        st.info("Generating Ghibli-style description via Gemini...")
        with st.spinner("Uploading to S3 and Gemini..."):
            # Upload original to S3
            img_bytes = uploaded_image.read()
            file_id = f"user_uploads/{uuid.uuid4()}.png"
            s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"

            st.image(img_bytes, caption="📤 Uploaded Image")

            try:
                # Gemini generation
                st.info("Generating Ghibli-style description via Gemini...")
                gemini_response = generate_edited_image_gemini(img_bytes, prompt)

                st.markdown(f"**Gemini Response:**\n\n{gemini_response}")
                st.markdown(generate_download_link(s3_url), unsafe_allow_html=True)
                st.markdown(generate_instagram_link(s3_url), unsafe_allow_html=True)

            except Exception as e:
                st.error("Gemini image editing failed.")
                st.exception(e)

    else:
        st.warning("Please upload an image and enter a prompt.")
