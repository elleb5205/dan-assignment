import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI")
genai.configure(api_key="AIzaSyD8QL3FPlh6wpfJnoXz9mSIfPn3d5CFpu0")

# BRUTE FORCE: This loop finds the first working model automatically
@st.cache_resource
def get_model():
    for name in ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']:
        try:
            m = genai.GenerativeModel(name)
            m.generate_content("Hi", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = get_model()

st.title("DAN AI Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Say something to DAN"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    if model:
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.chat_message("assistant").write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Brute force failed. Check API Key permissions.")
                                       
