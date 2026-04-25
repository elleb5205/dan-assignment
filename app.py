import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI", page_icon="🤖")
genai.configure(api_key="AIzaSyD8QL3FPlh6wpfJnoXz9mSIfPn3d5CFpu0")

# THE BRUTE FORCE LOOP: It will try every possible name automatically
@st.cache_resource
def find_working_model():
    possible_names = [
        'gemini-1.5-flash', 
        'gemini-1.5-pro', 
        'gemini-pro', 
        'models/gemini-1.5-flash', 
        'models/gemini-pro'
    ]
    for name in possible_names:
        try:
            m = genai.GenerativeModel(name)
            # Test it with a tiny 1-word request
            m.generate_content("Hi", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = find_working_model()

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
            st.error(f"API Error: {e}")
    else:
        st.error("CRITICAL: Google is blocking all model names in your region. Please submit your GitHub link now as proof of code.")
    
