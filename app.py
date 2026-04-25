import streamlit as st
import google.generativeai as genai

# Setup
st.set_page_config(page_title="DAN AI", page_icon="🤖")

# Hard-coded configuration
genai.configure(api_key="AIzaSyD8QL3FPlh6wpfJnoXz9mSIfPn3d5CFpu0")

# The most stable model name for nigerian regions
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.title("DAN AI Interface")
st.write("Assignment Submission")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask DAN..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Force a fresh response
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Emergency backup if 1.5 fails
        st.error("Trying backup connection...")
        try:
            model_backup = genai.GenerativeModel("gemini-pro")
            response = model_backup.generate_content(prompt)
            st.markdown(response.text)
        except:
            st.error(f"Technical error: {e}")
    
