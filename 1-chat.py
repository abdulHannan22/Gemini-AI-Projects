from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

st.set_page_config(page_title="Gemini LLM Chatbot")
st.header("Ask me anything!")

input = st.text_input("Your question:",key="input")
submit = st.button("Submit", key="submit")

# If the submit button is clicked and input is not empty, get the response from Gemini
if submit and input:
    response = get_gemini_response(input)
    st.write(response)