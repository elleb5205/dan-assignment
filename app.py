import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DAN AI Interface", page_icon="🤖")

# Logic to connect the AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.warning("Please add your GOOGLE_API_KEY to Streamlit Secrets.")

st.title("DAN: Advanced Neural Interface")
st.write("Assignment Submission: AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Neural Link Established. I am DAN. Ask me anything."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # This part makes it talk like ChatGPT
    try:
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error("Connection error. Check your API key!")
