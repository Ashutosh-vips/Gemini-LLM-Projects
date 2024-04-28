import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="Gemini Chatbot")

############## New Bard-like interface elements ##############
st.markdown("<h1 style='text-align: center;'>Gemini Chatbot</h1>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center;'>I'm Gemini Pro, a large language model from Google AI, ready to engage in conversation and assist you with your tasks. Ask me anything, or try a creative prompt!</p>
""", unsafe_allow_html=True)
################################################################

# Create a container for the chat interface
chat_container = st.container()

with chat_container:
    user_input = st.text_input("You:", key="input")
    submit_button = st.button("Send")

    if submit_button and user_input:
        response = get_gemini_response(user_input)

        # Update chat history
        st.session_state['chat_history'].extend([("You", user_input)] + [("Bard", chunk.text) for chunk in response])  # Add messages in desired order

    # Display chat history in a scrollable container
    st.session_state['chat_history'] = st.session_state.get('chat_history', [])  # Initialize if needed
    for role, text in st.session_state['chat_history']:
        st.write(f"**{role}:** {text}")  # No need to reverse for desired order
