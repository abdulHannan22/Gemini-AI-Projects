from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-001")

chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question)
    return response.text

st.set_page_config(page_title="Q&A Chatbot")
st.header("Q&A Chatbot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Your question:", key="input")
submit = st.button("Submit", key="submit")

if submit and user_input:
    response = get_gemini_response(user_input)
    
    # Add to chat history
    st.session_state['chat_history'].append(("You", user_input))
    st.session_state['chat_history'].append(("Bot", response))
    
    # Display the response
    st.subheader("Response:")
    st.write(response)

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"**{role}:** {text}")
    st.write("---")