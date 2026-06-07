from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from PyPDF2 import PdfReader
import os
import google.generativeai as genai

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_embeddings():
    """Return a GoogleGenerativeAIEmbeddings instance.
    If `EMBEDDING_MODEL` env var is set, use it; otherwise let the library choose a default.
    """
    # Use explicit fallback to a supported embedding model to avoid validation errors
    # Use a known supported embedding model by default
    model = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-2")
    return GoogleGenerativeAIEmbeddings(model=model)

def get_pdf_text(pdf_file):
    text = ""
    for pdf in pdf_file:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("vector_store")
    return vector_store

def get_conversation_chain(vector_store):
    prompt_template = """
    Answer the following question based on the context provided. If the answer is not in the context, say "I don't know".
    Context:\n {context}\n

    Question:\n {question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    try:
        embeddings = get_embeddings()
        
        # Check if vector store exists
        if not os.path.exists("vector_store"):
            st.error("Please upload and process PDFs first!")
            return

        new_db = FAISS.load_local("vector_store", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversation_chain(new_db)

        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )

        print(response)
        st.write("Reply: ", response['output_text'])
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please make sure you have uploaded and processed PDFs first.")




def main():
    st.set_page_config(page_title="Multiple PDF Q&A Chatbot")
    st.header("Multiple PDF Q&A Chatbot")

    user_question = st.text_input("Ask a question about the PDFs:", key="user_question")
    if user_question:
        user_input(user_question)
    
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
        if st.button("Process PDFs"):
            if pdf_docs:
                with st.spinner("Processing PDFs..."):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        if raw_text.strip():
                            text_chunks = get_text_chunks(raw_text)
                            get_vector_store(text_chunks)
                            st.success("PDFs processed and vector store created.")
                        else:
                            st.error("No text found in the uploaded PDFs.")
                    except Exception as e:
                        st.error(f"Error processing PDFs: {str(e)}")
            else:
                st.error("Please upload PDF files first.")

main()