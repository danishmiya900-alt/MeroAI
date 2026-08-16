import streamlit as st
import requests
import replicate
import os

# Page Config
st.set_page_config(page_title="MeroAI Assistant", page_icon="⚡", layout="wide")

# Styling
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    input[type="text"], textarea, .stChatInput input {
        color: #FFFFFF !important; background-color: #1F2937 !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# API Keys
gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
replicate_key = st.secrets.get("REPLICATE_API_TOKEN", os.getenv("REPLICATE_API_TOKEN"))

if replicate_key:
    os.environ["REPLICATE_API_TOKEN"] = replicate_key

st.title("MeroAI Assistant ⚡")

# Direct API Call
def get_gemini_response(prompt_text, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt_text}]}]})
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return "Error: API Key check karo ya code error hai."

# Sidebar
mode = st.sidebar.radio("Mode:", ["Chat", "Image", "Video"])

if mode == "Chat":
    if prompt := st.chat_input("Poocho jo poochna hai..."):
        with st.chat_message("user"): st.markdown(prompt)
        with st.spinner("AI soch raha hai..."):
            reply = get_gemini_response(prompt, gemini_key)
            st.markdown(reply)

elif mode == "Image":
    img_prompt = st.text_input("Kya banana hai?")
    if st.button("Generate"):
        if replicate_key:
            output = replicate.run("stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b", input={"prompt": img_prompt})
            st.image(output[0])

elif mode == "Video":
    vid_prompt = st.text_input("Video ke liye prompt:")
    if st.button("Generate Video"):
        if replicate_key:
            output = replicate.run("anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e42d021f4d7496cdb3cdb001", input={"prompt": vid_prompt})
            st.video(output[0])
            
