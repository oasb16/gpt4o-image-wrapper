import streamlit as st
import openai
import base64
from io import BytesIO
from PIL import Image
from streamlit.components.v1 import html

st.set_page_config(page_title="GPT-4o Image Generator", layout="centered")

openai.api_key = st.secrets.get("OPENAI_API_KEY")

def sanitize_prompt(prompt):
    return f"A {SAFE_KEYWORDS[0]} {prompt.strip()}. Rendered as an {SAFE_KEYWORDS[2]} in soft tone."

def generate_image(prompt):
    clean_prompt = sanitize_prompt(prompt)
    response = openai.images.generate(
        model="dall-e-3",
        prompt=f"Create Ghibli Style photos for this user prompt: {clean_prompt}",
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    return image_url

def image_to_download_link(img_url):
    return f'<a href="{img_url}" download="gpt4o_image.png" target="_blank">📥 Download Image</a>'

def share_to_twitter_url(prompt):
    return f"https://twitter.com/intent/tweet?text=Check+out+this+image+generated+by+GPT-4o:+{prompt}"

st.title("🖼️ GPT-4o Image Creator")
method = st.radio("Input Method", ["Text Prompt", "Voice (Experimental)"])

if method == "Text Prompt":
    prompt = st.text_area("Enter your image description")
else:
    prompt = st.text_input("Speak your prompt then type it here (voice-to-text pending)")

if st.button("Generate Image") and prompt.strip():
    with st.spinner("Generating image..."):
        try:
            img_url = generate_image(prompt)
            st.image(img_url, caption="Generated by GPT-4o", use_column_width=True)
        except openai.error.InvalidRequestError as e:
            st.error("⚠️ OpenAI flagged this prompt: " + str(e))
            st.info("Try rephrasing your request with simpler, safer words.")
        st.image(img_url, caption="Generated by GPT-4o", use_column_width=True)
        st.markdown(image_to_download_link(img_url), unsafe_allow_html=True)
        st.markdown(f"[🔗 Share on Twitter]({share_to_twitter_url(prompt)})")
