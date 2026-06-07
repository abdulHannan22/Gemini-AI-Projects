from dotenv import load_dotenv
load_dotenv()

from PIL import Image
import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-3.5-flash')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        image_parts =[
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Multilanguage Invoice Extractor")

input = st.text_input("Input Prompt : ",key=input)
upload_file = st.file_uploader("Choose an image of the invoice..",type=["jpg","jpeg","png"])
image=""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="uploaded file",use_column_width=True)

submit = st.button("tell me about the invoice")

input_prompt ="""
You are an expert in understanding invoices in any language.
You will be given an image of an invoice and a prompt in English.
Your task is to extract the relevant information from the invoice based on the prompt.
You will return the information in English.
"""

if submit:
    image_data = input_image_details(upload_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("Response:")
    st.write(response)