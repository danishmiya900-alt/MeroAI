import streamlit as st
import google.generativeai as genai
import replicate
import os
from gtts import gTTS
import io

# Page Setup
st.set_page_config(page_title="MeroAI", page_icon="⚡", layout="wide")

# Styling
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    input { color: #FFFFFF !important; background-color: #1F2937 !important; }
</style>
""", unsafe_allow_html=True)

# API Setup
gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
if gemini_key:
    genai.configure(api_key=gemini_key)

st.title("MeroAI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Logic
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Poocho jo poochna hai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # SABSE STABLE MODEL: 1.5-flash
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error aaya: {str(e)}. (Bhai, API Key ya Model access check karo)"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
        try:
            tts = gTTS(text=bot_reply[:200], lang='hi')
            sound_file = io.BytesIO()
            tts.write_to_fp(sound_file)
            st.audio(sound_file, format='audio/mp3')
        except:
            pass
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    
