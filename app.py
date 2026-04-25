import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI Project", page_icon="🤖")

# Fetching the key SAFELY from Streamlit's hidden vault
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Setup incomplete: API Key not found in Streamlit Secrets.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("DAN AI Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Say something to DAN"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
        
