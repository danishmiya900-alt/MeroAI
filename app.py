import streamlit as st
import requests
import replicate
import os
from gTTS import gTTS
import io

# Page Config
st.set_page_config(page_title="MeroAI Assistant", page_icon="⚡", layout="wide")

# Custom Styling (Fixes Typing Visibility + Themes)
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    input[type="text"], textarea, .stChatInput input {
        color: #FFFFFF !important;
        background-color: #1F2937 !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    input::placeholder, textarea::placeholder {
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
    }
</style>
""", unsafe_allow_html=True)

# Secrets Retrieval
gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
replicate_key = st.secrets.get("REPLICATE_API_TOKEN", os.getenv("REPLICATE_API_TOKEN"))

if replicate_key:
    os.environ["REPLICATE_API_TOKEN"] = replicate_key

st.title("MeroAI Assistant ⚡")

# Sidebar
st.sidebar.title("⚡ Control Panel")
mode = st.sidebar.radio("Select Mode:", ["💬 Chat Assistant", "🎨 Image Generator", "🎬 Video Generator"])

# Direct HTTP Call Function for Gemini
def get_gemini_response(prompt_text, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        try:
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return "AI Response Parsing Error."
    else:
        return f"Error ({response.status_code}): {response.text}"

# 1. Chat Assistant Mode
if mode == "💬 Chat Assistant":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Poocho jo poochna hai..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not gemini_key:
            bot_reply = "API Key missing hai! Secrets me GEMINI_API_KEY check karo."
        else:
            bot_reply = get_gemini_response(prompt, gemini_key)

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
            try:
                tts = gTTS(text=bot_reply[:250], lang='hi')
                sound_file = io.BytesIO()
                tts.write_to_fp(sound_file)
                st.audio(sound_file, format='audio/mp3')
            except Exception:
                pass

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# 2. Image Generator Mode
elif mode == "🎨 Image Generator":
    st.subheader("🎨 AI Image Generation")
    img_prompt = st.text_input("Kaisa image banana hai?")
    if st.button("Generate Image"):
        if not replicate_key:
            st.error("Replicate API Key missing hai!")
        else:
            with st.spinner("Creating image..."):
                try:
                    output = replicate.run(
                        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                        input={"prompt": img_prompt}
                    )
                    st.image(output[0], use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# 3. Video Generator Mode
elif mode == "🎬 Video Generator":
    st.subheader("🎬 AI Video Generation")
    vid_prompt = st.text_input("Kaisa video banana hai?")
    if st.button("Generate Video"):
        if not replicate_key:
            st.error("Replicate API Key missing hai!")
        else:
            with st.spinner("Processing video..."):
                try:
                    output = replicate.run(
                        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e42d021f4d7496cdb3cdb001",
                        input={"prompt": vid_prompt}
                    )
                    st.video(output[0])
                except Exception as e:
                    st.error(f"Error: {e}")
    
