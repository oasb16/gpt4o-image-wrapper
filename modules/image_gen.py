import openai
from streamtoolkit_omkar.config.env import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response["data"][0]["url"]
