from dotenv import load_dotenv
load_dotenv()

import base64
import PyPDF2
import spacy
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to convert PDF to imagesfrom dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import pdf2image
import google.generativeai as genai
from PIL import Image 


# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to convert PDF to images
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to convert PDF to images
def convert_pdf_to_images(uploaded_file):
    if uploaded_file is not None:
        try:
            images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r'C:\Program Files\poppler-24.02.0\Library\bin')
            return images
        except Exception as e:
            st.error(f"Error converting PDF to images: {e}")
    else:
        st.warning("Please upload a PDF file.")

# Function to get response from Generative AI model
def get_gemini_response(prompt, pdf_content, input_text):
    if pdf_content:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_text, pdf_content[0], prompt])
        return response.text
    else:
        st.error("Error: No PDF content available.")
        
# Function to parse resume
# def parse_resume(prompt, pdf_content, input_text):
#     resume_text = ""
#     if uploaded_file is not None:
#         try:
#             model = genai.GenerativeModel('gemini-pro-vision')
#             response = model.generate_content([input_text, pdf_content[0], prompt])
#             response_text = response.text
#             resume_text = response_text.split("Resume Text:")[1].strip()
#         except Exception as e:
#             st.error(f"Error parsing resume: {e}")
#     else:
#         st.warning("Please upload a PDF file.")
#     return resume_text




# Function to screen resumes
# def screen_resume(resume_text, job_description):
#     # Implement resume screening logic here
#     # Example: Check for keywords in resume text
#     if "Python" in resume_text and "Data Science" in resume_text:
#         return "Qualified"
#     else:
#         return "Not Qualified"

# Function to get match percentage
def get_match_percentage(prompt, pdf_content, input_text):
    if pdf_content:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_text, pdf_content[0], prompt])
        response_text = response.text
        try:
            match_percentage_str = response_text.split("Percentage")[0].strip()
            match_percentage = float(match_percentage_str)
            return match_percentage
        except (ValueError, IndexError):
            st.error("Error: Match percentage could not be extracted.")
            return None
    else:
        st.error("Error: No PDF content available.")

# Streamlit App
st.set_page_config(page_title="ATSResumeVision")
st.header("ATS Tracking System")

# Input fields
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons
submit1 = st.button("Evaluate Resume")
submit2 = st.button("Improve Skills")
submit3 = st.button("Match Percentage")
# submit4 = st.button("Parse Resume")


# Prompts
input_prompt1 = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
 in less than 100 words.
"""
input_prompt2 = """
You are a professional career coach with a background in data science, your task is to provide constructive feedback to the candidate
on how they can improve their resume to better align with the job description.
in bullets key point for the resume improvement.
and then further tell me where the candidate can improve their at what section in particlar.
"""

input_prompt3 = """
BE HARSH on this one.and display in bold the percentage of match and then the keywords missing and then final thoughts.
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# input_prompt4 = """
# You are a professional career coach with a background in data science, your task is to provide constructive feedback to the candidate
# on how they can improve their resume to better align with the job description.
# in bullets key point for the resume improvement.
# and then further tell me where the candidate can improve their at what section in particlar.
# """

# Button actions
if submit1:
    if uploaded_file is not None:
        pdf_content = convert_pdf_to_images(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("Evaluation Response")
            st.write(response)
        else:
            st.write("Error: PDF processing failed.")
    else:
        st.write("Please upload the resume.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = convert_pdf_to_images(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader("Skills Improvement Response")
            st.write(response)
        else:
            st.write("Error: PDF processing failed.")
    else:
        st.write("Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content=convert_pdf_to_images(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
# elif submit4:
#     if uploaded_file is not None:
#         pdf_content = convert_pdf_to_images(uploaded_file)

#         resume_text = parse_resume(input_prompt2, pdf_content, input_text)
#         # Display parsed resume text
#         st.subheader("Parsed Resume Text")
#         st.write(resume_text)
#     else:
#         st.write("Please upload the resume.")