import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI", page_icon="🤖")

# Your key is correct - do not change this
genai.configure(api_key="AIzaSyD8QL3FPlh6wpfJnoXz9mSIfPn3d5CFpu0")

# Brute force: Try multiple names until one works
model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
model = None

for name in model_names:
    try:
        model = genai.GenerativeModel(name)
        # Test if this model name is valid
        model.generate_content("test", generation_config={"max_output_tokens": 1})
        break 
    except:
        continue

st.title("DAN AI Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Say something to DAN"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    if model:
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    else:
        st.error("Google is still being difficult. Please refresh one more time.")
    
