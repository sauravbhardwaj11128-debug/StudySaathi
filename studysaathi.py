import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import streamlit as st


genai.configure(api_key=st.secrets["GEMINI_API"])
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_pdf_text(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def extract_docx_text(docx_file):
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def generate_summary(text):
    prompt = f"""
    Analyze the notes and provide:
    1. Detailed Summary
    2. Key Concepts
    3. Important Formulas
    4. Revision Notes

    Notes:
    {text}
    """
    return model.generate_content(prompt).text


def generate_questions(text):
    prompt = f"""
    Generate important exam questions from these notes:

    Notes:
    {text}
    """
    return model.generate_content(prompt).text


def generate_answers(text):
    prompt = f"""
    Generate detailed answers for important questions:

    Notes:
    {text}
    """
    return model.generate_content(prompt).text


def generate_mcqs(text):
    prompt = f"""
    Create 10 MCQs with:
    Question
    4 Options
    Correct Answer

    Notes:
    {text}
    """
    return model.generate_content(prompt).text


st.title("StudySaathi AI 📚")

uploaded_file = st.file_uploader("Upload Notes", type=["pdf", "docx", "txt"])

notes_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        notes_text = extract_pdf_text(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        notes_text = extract_docx_text(uploaded_file)

    else:
        notes_text = uploaded_file.read().decode()


if notes_text:

    if st.button("Generate Summary"):
        st.subheader("Summary")
        st.write(generate_summary(notes_text))

    if st.button("Generate Questions"):
        st.subheader("Questions")
        st.write(generate_questions(notes_text))

    if st.button("Generate Answers"):
        st.subheader("Answers")
        st.write(generate_answers(notes_text))

    if st.button("Generate MCQs"):
        st.subheader("MCQs")
        st.write(generate_mcqs(notes_text))
