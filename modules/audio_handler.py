# modules/audio_handler.py
from st_audiorec import st_audiorec
import streamlit as st

def record_audio():
    """
    Renders a browser-native audio recorder in Streamlit
    and returns WAV audio bytes if recorded.
    """
    st.markdown("🎙️ **Voice Recorder** (works best on Chrome desktop or Android mobile)")
    st.markdown("*Click the microphone below to start/stop recording*")

    audio_bytes = st_audiorec()

    if audio_bytes:
        st.success("✅ Voice recorded!")
        return audio_bytes

    return None
