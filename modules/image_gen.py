# modules/image_gen.py
import openai
from streamtoolkit_omkar.config.env import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_image(prompt: str) -> str:
    """Generate Ghibli-style image from prompt using GPT-4o DALL·E."""
    response = openai.images.generate(
        prompt=f"Convert this {prompt} into a modern anime style with "
               f"Ghibli influence, clean line art, realistic shading, "
               f"soft pastel tones, and expressive faces. "
               f"Inspired by scenes from 'Your Name' and 'Whisper of the Heart'. "
               f"Emphasize clarity, color harmony, and emotional warmth.",
        n=1,
        size="1024x1024"
    )
    return response.data[0].url
