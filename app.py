import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI Project", page_icon="🤖")

# Fetching the key SAFELY from your Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# DYNAMIC DISCOVERY: This finds the working model automatically
@st.cache_resource
def get_model():
    try:
        # Ask Google for the list of models supported for your key
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except Exception as e:
        st.error(f"Discovery Error: {e}")
    return None

model = get_model()

st.title("DAN AI Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask DAN anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if model:
        try:
            response = model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Technical Error: {e}")
    else:
        st.error("Could not find a valid AI model. Please verify your API Key in Google AI Studio.")
            
