from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import PyPDF2 as pdf
from langchain import PromptTemplate
from langchain_openai import OpenAI



def generate_text(upload_file):
    reader=pdf.PdfReader(upload_file)
    text=''
    for page in reader.pages:
        text+=page.extract_text()
    return text

def generate_response(text, jd):
    prompt = f'You are an expert human resource manager with expertise in data science, web development, cloud computing, and data analysis.\n\nCompare this resume:\n{text}\n\nBased on the job description:\n{jd}\n\nAnd tell the matching percentage of the resume, missing keywords in the resume, and further improvements that can be done in the resume according to the job description.'
    llm=OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    response=llm(prompt)
    return response



st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
jd=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=generate_text(uploaded_file)
        response=generate_response(text,jd)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")