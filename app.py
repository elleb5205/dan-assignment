import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="DAN AI Project", page_icon="🤖")

# Fetch API Key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Setup incomplete: Add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# THIS IS THE FIX: Explicitly calling the model without the 'models/' prefix
# if 'models/' didn't work, we try the simple name
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("DAN AI Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Say something to DAN"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # We add a safety check here to force the correct API version
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Final emergency fallback if Flash is truly blocked in your region
        st.info("Switching to standard model...")
        try:
            backup_model = genai.GenerativeModel('gemini-pro')
            response = backup_model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as last_e:
            st.error(f"Final Technical Error: {last_e}")
        
