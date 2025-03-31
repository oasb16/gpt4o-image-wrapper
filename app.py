
import streamlit as st
import requests
import openai
import boto3
import uuid
from PIL import Image
from io import BytesIO
from streamtoolkit_omkar.config.env import OPENAI_API_KEY, AWS_REGION, S3_BUCKET
from modules.image_gen import generate_image
from modules.utils import generate_instagram_link, generate_download_link

AWS_ACCESS_KEY=st.secrets.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY=st.secrets.get("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE=st.secrets.get("DYNAMODB_TABLE")

openai.api_key = OPENAI_API_KEY
s3 = boto3.client("s3", region_name=AWS_REGION)

st.set_page_config(page_title="GPT-4o Image Wrapper", layout="centered")
st.title("🖼️ GPT-4o Prompt/Image to Anime")

uploaded_image = st.file_uploader("📤 Upload an image (optional)", type=["png", "jpg", "jpeg"])
prompt = st.text_area("Or enter a text prompt")

def generate_image_from_image(uploaded_image):
    print(f"generating image from s3_url : {uploaded_image}")
    response = openai.images.edit(
        model="dall-e-2",
        image=open(uploaded_image, "rb"),
        mask=open(uploaded_image, "rb"),
        prompt=f"Convert this image into a modern anime style with Ghibli influence, clean line art, realistic shading, soft pastel tones, and expressive faces. Inspired by scenes from 'Your Name' and 'Whisper of the Heart'. Emphasize clarity, color harmony, and emotional warmth.",
        n=1,
        size="1024x1024",
    )
    print("generated {response.data[0].url}")
    return response.data[0].url

if st.button("Generate / Upload") and (prompt or uploaded_image):
    with st.spinner("Processing..."):
        if uploaded_image:
            img_bytes = uploaded_image.read()
            print(f"img_bytes : {img_bytes}")
            file_id = f"user_uploads/{uuid.uuid4()}.png"
            print(f"file_id : {file_id}")
            s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"
            


            img_bytes = uploaded_image.read()
            print(f"img_bytes : {img_bytes}")
            file_id = f"user_uploads/{uuid.uuid4()}.png"
            print(f"file_id : {file_id}")
            image_url = generate_image_from_image
            s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            s3_url_2 = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"            

            dynamodb = boto3.resource(
                'dynamodb',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )
            

            table = dynamodb.Table(DYNAMODB_TABLE)
            table.put_item(
                Item={
                    "email": "123",
                    "uploaded_image": s3_url,
                    "generated_image": s3_url_2,
                }
            ) 
            response = requests.get(s3_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=s3_url_2, use_container_width=True)
            st.success(f"Uploaded to S3: {s3_url_2}")

        if prompt:
            image_url = generate_image(prompt)
            st.image(image_url, caption="🎨 Generated Image")
            st.markdown(generate_download_link(image_url), unsafe_allow_html=True)
            st.markdown(generate_instagram_link(image_url), unsafe_allow_html=True)
