from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(input,image):
    if input !="":
        response = model.generate_content([input,image])
        return response.text
    else:
        response = model.generate_content(image)
    return response.text
    
st.set_page_config(page_title="Gemini LLM Chatbot with Vision")
st.header("Gemini LLM Chatbot with Vision")

input = st.text_input("Input text:", key="input")
uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"], key="image")
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    
submit = st.button("Submit", key="submit")

# If the submit button is clicked and input is not empty, get the response from Gemini
if submit:
    response = get_gemini_response(input, image)
    st.write(response)