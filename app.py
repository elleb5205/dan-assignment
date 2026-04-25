import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI Project", page_icon="🤖")

# Securely fetching the key from your Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# We specify the model directly to avoid the "v1beta" error
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("DAN AI Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Standard generation call
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Technical error: {e}")
        
