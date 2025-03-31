
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
from google import genai
from google.genai import types

AWS_REGION=st.secrets.get("AWS_REGION")
GEMINI_API_KEY=st.secrets.get("GEMINI_API_KEY")
AWS_ACCESS_KEY=st.secrets.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY=st.secrets.get("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE=st.secrets.get("DYNAMODB_TABLE")

openai.api_key = OPENAI_API_KEY
s3 = boto3.client("s3", region_name=AWS_REGION)

st.set_page_config(page_title="GPT-4o Image Wrapper", layout="centered")
st.title("🖼️ You deserve an almost-ghibli-fied version of you!")

uploaded_image = st.file_uploader("📤 Upload an image here (optional)", type=["png", "jpg", "jpeg"])
prompt = st.text_area("Or write a text prompt to ghiblify it")


client = genai.Client(api_key=GEMINI_API_KEY)

def generate_edited_image_gemini(image_bytes, prompt_text):
    
    image = Image.open(image_bytes)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[prompt_text, image],
        config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.show()
    
    st.image(image, caption="https://www.linkedin.com/in/omkarsb7/ ", use_container_width=True)

if st.button("Generate / Upload") and (prompt or uploaded_image):
    with st.spinner("Processing..."):
        if uploaded_image:
            prompt_text = f"Convert the image into and anime style using immersive realism similar at 99% to Studio Ghiblis style\
                 but not the same but similar so it’s not infrigment"
            generate_edited_image_gemini(uploaded_image, prompt_text)

            img_bytes = uploaded_image.read()
            file_id = f"user_uploads/{uuid.uuid4()}.png"
            # s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            # s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"
            # img_bytes = uploaded_image.read()
            # file_id = f"user_uploads/{uuid.uuid4()}.png"
            #image_url = generate_edited_image_gemini(file_id, prompt_text)
            # s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            # s3_url_2 = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"            

            # dynamodb = boto3.resource(
            #     'dynamodb',
            #     ra                        egion_name=AWS_REGION,
            #     aws_access_key_id=AWS_ACCESS_KEY,
            #     aws_secret_access_key=AWS_SECRET_KEY
            # )
            

            # table = dynamodb.Table(DYNAMODB_TABLE)
            # table.put_item(
            #     Item={
            #         "email": "123",
            #         "uploaded_image": s3_url,
            #         "generated_image": s3_url_2,
            #     }
            # ) 
            # response = requests.get(s3_url)
            #image = Image.open(BytesIO(response.content))
            #st.image(image, caption=s3_url_2, use_container_width=True)
            #st.success(f"Uploaded s3_url to S3: {s3_url}")
            #st.success(f"Uploaded s3_url_2 to S3: {s3_url_2}")

        elif prompt:
            image_url = generate_image(prompt)
            st.image(image_url, caption="🎨 Generated Image")
            st.markdown(generate_download_link(image_url), unsafe_allow_html=True)
            st.markdown(generate_instagram_link(image_url), unsafe_allow_html=True)
