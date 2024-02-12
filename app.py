import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ## load all env variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## gemini pro response
def get_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


import PyPDF2 as pdf

def input_pdf_text(uploaded_file):
    # Use PdfReader instead of PdfFileReader
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    # The loop was also incorrect. It should iterate over reader.pages directly
    for page in reader.pages:
        # No need to call reader.pages(page), as page is already the page object
        text += str(page.extract_text())
    return text



#Prompt Template
input_prompt = """
Act as an ATS (Application Tracking System) tailored for the data science, machine learning, NLP, and AI job market, which is currently extremely 
clustered and saturated. Analyze the input, which could be a job description or resume, focusing on identifying 
and matching keywords relevant to these fields. Your task is to determine the extent to which the candidate's 
qualifications and experiences match the job requirements based on the presence of specific keywords related to 
data science techniques, machine learning algorithms, NLP methodologies, and AI technologies. 
Calculate and provide a percentage matching score reflecting the alignment between the candidate's profile and 
the job's demands. Be harsh on giving the matching percentage.
Assign the percentage matching based on job description and the missing keywords with high accuracy
resume : {text}
description : {jd}
I want the response in one single string having the structure {{"Job Description Match" : "%", "Missing Keywords : []", "Profile Summary"
: ""}}
"""


##streamlit app
st.title("MuCool_ATS")
st.text("Get Your Resume ATS")
jd = st.text_area("Paste the Job Description Here")
uploaded_file = st.file_uploader("Upload your Latest Resume here", type = "pdf", help="Please Upload the PDF")

submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_response(input_prompt)
        st.subheader(response)

