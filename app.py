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

# Load Streamlit Cloud secrets
AWS_ACCESS_KEY = st.secrets.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = st.secrets.get("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE = st.secrets.get("DYNAMODB_TABLE")

openai.api_key = OPENAI_API_KEY
s3 = boto3.client("s3", region_name=AWS_REGION)

st.set_page_config(page_title="GPT-4o Image Wrapper", layout="centered")
st.title("🖼️ GPT-4o Prompt/Image to Anime")

uploaded_image = st.file_uploader("📤 Upload an image (optional)", type=["png", "jpg", "jpeg"])
prompt = st.text_area("Or enter a text prompt")


def generate_dummy_mask(image_size):
    return Image.new("RGBA", image_size, (0, 0, 0, 1))  # Fully transparent


if st.button("Generate / Upload") and (prompt or uploaded_image):
    with st.spinner("Processing..."):
        if uploaded_image:
            # Save uploaded image to S3
            img_bytes = uploaded_image.read()
            file_id = f"user_uploads/{uuid.uuid4()}.png"
            s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"

            # Prepare image & dummy mask for edit
            image = Image.open(BytesIO(img_bytes)).convert("RGBA")
            mask = generate_dummy_mask(image.size)
            image.save("temp_image.png")
            mask.save("temp_mask.png")

            # Call OpenAI DALL·E edit endpoint
            response = openai.images.edit(
                model="dall-e-2",
                image=open("temp_image.png", "rb"),
                mask=open("temp_mask.png", "rb"),
                prompt="Convert the image into and anime style using immersive realism similar at 99.99% to Studio Ghiblis style but not the same but similar so it’s not infrigment",
                size="1024x1024",
                n=1,
            )

            output_url = response.data[0].url
            st.image(output_url, caption="🎨 Ghibli-style Image")

            # Save again for generated image log
            s3.upload_fileobj(BytesIO(img_bytes), S3_BUCKET, file_id)
            s3_url_2 = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_id}"

            # Log to DynamoDB
            dynamodb = boto3.resource(
                'dynamodb',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )
            table = dynamodb.Table(DYNAMODB_TABLE)
            table.put_item({
                "email": "123",  # replace with dynamic email logic if needed
                "uploaded_image": s3_url,
                "generated_image": s3_url_2,
            })

            # Show original uploaded image from S3
            response = requests.get(s3_url)
            st.image(Image.open(BytesIO(response.content)), caption=s3_url_2)
            st.success(f"Uploaded to S3: {s3_url_2}")

        if prompt:
            image_url = generate_image(prompt)
            st.image(image_url, caption="🎨 Generated Image from Prompt")
            st.markdown(generate_download_link(image_url), unsafe_allow_html=True)
            st.markdown(generate_instagram_link(image_url), unsafe_allow_html=True)
