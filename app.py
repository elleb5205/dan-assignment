import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI Interface", page_icon="🤖")

# Logic to connect the AI directly
genai.configure(api_key="AIzaSyD8QL3FPlh6wpfJnoXz9mSIfPn3d5CFpu0")
model = genai.GenerativeModel('gemini-pro')

st.title("DAN: Advanced Neural Interface")
st.write("Assignment Submission: AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Neural Link Established. I am DAN. Ask me anything."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # This part makes it talk
    try:
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error("Connection error. Check your API key!")
        
