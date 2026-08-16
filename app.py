import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="MeroAI", page_icon="⚡")

# Hardcoded CSS to fix keyboard visibility once and for all
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatInput textarea { color: white !important; background: #1F2937 !important; }
</style>
""", unsafe_allow_html=True)

st.title("MeroAI Assistant ⚡")

# Get API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing hai! Manage App -> Secrets mein jao.")
else:
    genai.configure(api_key=api_key)
    
    # Using the standard model
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Model Error: {e}")

    # Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Poocho..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"Error: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
