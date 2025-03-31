
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_image(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=f"Convert this {prompt} into a modern anime style with Ghibli influence, clean line art, realistic shading, soft pastel tones, and expressive faces. Inspired by scenes from 'Your Name' and 'Whisper of the Heart'. Emphasize clarity, color harmony, and emotional warmth.",
        n=1,
        size="1024x1024"
    )
    return response.data[0].url
