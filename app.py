import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI Project")
genai.configure(api_key="AIzaSyD8QL3FPlh6wpfJnoXz9mSIfPn3d5CFpu0")

# AUTOMATIC DISCOVERY: This finds the "working" model for us
@st.cache_resource
def get_working_model():
    try:
        # Ask Google: "What models do you have for me?"
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Returns the first one that works (usually gemini-1.5-flash)
                return genai.GenerativeModel(m.name)
    except Exception as e:
        st.error(f"Discovery failed: {e}")
    return None

model = get_working_model()

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
            st.error(f"Processing error: {e}")
    else:
        st.error("Model discovery failed. Please check your API key.")
    
