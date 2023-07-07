# import streamlit as st
from pathlib import Path
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
import openai
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS 
# from speech_to_text import * #edited by Sudip
import tempfile

# api = st.secrets["openai_api_key"]
# os.environ["OPENAI_API_KEY"] = api
# file_directory = os.path.join(Path.cwd(),"file_directory")
# # pdf_files = [f'sample{i}.pdf' for i in range(1, len(os.listdir(file_directory))+1)]
# pdf_files = sorted([file for file in os.listdir(file_directory)])

# extract text from multiple pdf files
def extract_text_multiple(pdfs_folder):
    # to be change according to ui
    raw_text = ""
    for pdf_file in os.listdir(pdfs_folder):
        doc_reader = PdfReader(os.path.join(pdfs_folder, pdf_file))
        for page in doc_reader.pages:
            raw_text += " " + page.extract_text()
    return raw_text

def user_question(query):
    return ''

def get_chunk_lst(pdf_text):
    splitter = CharacterTextSplitter(
                separator = ".",
                chunk_size = 200,
                chunk_overlap = 100,
                length_function = len
            )
    chunk_lst = splitter.split_text(pdf_text)
    return chunk_lst

def get_docsearch(pdf_text):
    # split text into multiple chunks
    chunk_lst = get_chunk_lst(pdf_text)
    
    # store hugging face embeddings
    embeddings = HuggingFaceEmbeddings()
    
    # embed all the chunks ans store in a vectordatabase
    doc_search = FAISS.from_texts(chunk_lst, embeddings)
    return doc_search

def get_answer(query, doc_search):
    # set api as environment variable
    load_dotenv()
    api = os.getenv("openai_api_key")
    os.environ["OPENAI_API_KEY"] = api
    
    # perform similarilty search with query
    docs = doc_search.similarity_search(query)
    
    # set a question answering chain
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    
    # get answer for the given query
    answer = chain.run(input_documents=docs, question=query)
    
    # if answer is not found
    if answer.strip()==" I don't know.".strip():
        answer = "Apologies! The information you have requested in not available at this point."
        
    return answer


# ----------------------------------------------------------------
# the flow 
# pdf_text = extract_text_multiple(pdf_folder='user_input_folder')
# query = user_question() 
# doc_search = get_docsearch(pdf_text)
# answer = get_answer(query=query, doc_search=doc_search)
