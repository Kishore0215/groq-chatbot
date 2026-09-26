import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Create the Groq client
client = Groq(api_key=api_key)

st.title("My Groq AI Chatbot")

# Set up memory (only create it once)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages so far
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input box at the bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # 1. Save and show the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 2. Build the full message list (system + history)
    messages_to_send = [
        {"role": "system", "content": "You are a friendly and helpful AI assistant."}
    ] + st.session_state.messages

    # 3. Send to Groq and get the reply
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages_to_send
    )
    reply = response.choices[0].message.content

    # 4. Save and show the AI's reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)