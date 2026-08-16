import streamlit as st
import google.generativeai as genaiimport streamlit as st
import google.generativeai as genai

st.title("MeroAI Assistant ⚡")
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing!")
else:
    genai.configure(api_key=api_key)
    # Using 'latest' suffix to avoid v1beta path issues
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    if prompt := st.chat_input("Poocho..."):
        st.chat_message("user").markdown(prompt)
        with st.spinner("AI soch raha hai..."):
            try:
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
                
