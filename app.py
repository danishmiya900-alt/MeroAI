import streamlit as st
import google.generativeai as genai
import replicate
import os

# Page Setup
st.set_page_config(
    page_title="MeroAI - AI Assistant",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling (Professional Look)
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #9CA3AF;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# API Keys Setup
gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
replicate_key = st.secrets.get("REPLICATE_API_TOKEN", os.getenv("REPLICATE_API_TOKEN"))

if gemini_key:
    genai.configure(api_key=gemini_key)
if replicate_key:
    os.environ["REPLICATE_API_TOKEN"] = replicate_key

# Sidebar Configuration
st.sidebar.title("⚡ MeroAI Control")
mode = st.sidebar.radio("Mode Select Karo:", ["💬 Chat Assistant", "🎨 Image Generator", "🎬 Video Generator"])

st.markdown('<div class="main-header">MeroAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Powerful AI Companion</div>', unsafe_allow_html=True)

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
            bot_reply = "API Key setup nahi hai bhai!"
        else:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"Error: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# 2. Image Generator Mode
elif mode == "🎨 Image Generator":
    st.subheader("🎨 AI Image Generation")
    img_prompt = st.text_input("Kaisa image banana hai? Prompt type karo:")
    if st.button("Generate Image", type="primary"):
        if not replicate_key:
            st.error("Replicate API Token missing hai!")
        else:
            with st.spinner("Image ready ho rahi hai..."):
                try:
                    output = replicate.run(
                        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                        input={"prompt": img_prompt}
                    )
                    st.image(output[0], caption="Generated Image", use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# 3. Video Generator Mode
elif mode == "🎬 Video Generator":
    st.subheader("🎬 AI Video Generation")
    vid_prompt = st.text_input("Kaisa video banana hai? Prompt type karo:")
    if st.button("Generate Video", type="primary"):
        if not replicate_key:
            st.error("Replicate API Token missing hai!")
        else:
            with st.spinner("Video process ho raha hai (1-2 min lagenge)..."):
                try:
                    output = replicate.run(
                        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e42d021f4d7496cdb3cdb001",
                        input={"prompt": vid_prompt}
                    )
                    st.video(output[0])
                except Exception as e:
                    st.error(f"Error: {e}")
                    
