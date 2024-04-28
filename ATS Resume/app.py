import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input_text)
    return response.text  # Return the raw text response

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

st.set_page_config(page_title="Smart ATS", layout="wide")  # Set page title and layout

st.title("Smart ATS")
st.header("Improve Your Resume with AI Guidance")

# Get job field/position and job description
job_field_position = st.text_input("Job Field/Position", "Enter the specific field or job title you're applying for")
jd = st.text_area("Paste the Job Description", height=200)

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"], help="Your resume in PDF format")

if uploaded_file is not None and jd and job_field_position:
    text = input_pdf_text(uploaded_file)
    input_prompt = """
    Hey! Acting as your experienced HR friend and resume screening pro, I'm here to help you land your dream job in {job_field_position}! 

    I'll analyze your resume and the job description, providing you with valuable insights:

    * Job Description Match: A clear percentage score on how well your resume aligns with the key requirements. 
    * Missing Keywords: Crucial skills or experiences mentioned in the job description that your resume seems to lack. 
    * Resume Improvement Tips: Actionable advice to optimize your resume for maximum impact.

    Ready to get started? Here's my expert analysis:

    Resume: {text}
    Job Description: {jd}
    """.format(text=text, jd=jd, job_field_position=job_field_position)

    response = get_gemini_response(input_prompt)

    with st.spinner("Analyzing your resume..."):
        # Simulate processing time for a better user experience
        pass

    st.success("Analysis Complete!")

    # Display the full text response directly
    st.write(response)

else:
    st.warning("Please provide the job field/position, job description, and resume to proceed.")
