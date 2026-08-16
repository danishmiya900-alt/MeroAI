import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="MeroAI", page_icon="🤖", layout="centered")

st.title("MeroAI 🤖")
st.caption("Your Gemini-Powered AI Companion")

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Message MeroAI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if not api_key:
        bot_reply = "API Key error."
    else:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            bot_reply = response.text
        except Exception as e:
            bot_reply = str(e)

    with st.chat_message("assistant"):
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
  
