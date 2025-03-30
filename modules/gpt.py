import openai
from modules.env import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_image(prompt):
    response = openai.images.generate(
        prompt=f"A cute {prompt}. Rendered as a cartoon in soft tone.",
        n=1,
        size="1024x1024"
    )
    return response.data[0].url
