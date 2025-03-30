import streamlit as st
import openai
from streamtoolkit_omkar.auth.streamlit_guard import token_input_box, get_user_from_token_ui
from streamtoolkit_omkar.config.env import OPENAI_API_KEY, AWS_REGION

st.title("🧠 GPT-4o Wrapper")

token = token_input_box()
user = get_user_from_token_ui(token)
if user:
    st.write("Ready to generate images...")