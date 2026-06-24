from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader

# Gemini API Setup
# Gemini API Setup
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("models/gemini-2.0-flash")

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Page Setup
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚"
)

st.title("📚 AI-Powered Study Buddy")
st.write("Your Personal AI Learning Assistant")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Concept Explainer",
        "Notes Summarizer",
        "Quiz Generator",
        "Study Planner"
    ]
)

# ====================================================
# TAB 1 - CONCEPT EXPLAINER
# ====================================================

with tab1:

    st.subheader("Concept Explainer")

    topic = st.text_input(
        "Enter Topic",
        placeholder="e.g. OSI Model"
    )

    if st.button("Explain Concept"):

        prompt = f"""
Explain the topic: {topic}

Give:
1. Simple Explanation
2. Exam Point of View
3. Interview Point of View
"""

        response = get_gemini_response(prompt)

        st.markdown(response)

# ====================================================
# TAB 2 - NOTES SUMMARIZER
# ====================================================

with tab2:

    st.subheader("Notes Summarizer")

    uploaded_file = st.file_uploader(
        "Upload PDF Notes",
        type=["pdf"]
    )

    if uploaded_file is not None:

        pdf_reader = PdfReader(uploaded_file)

        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        if st.button("Generate Summary"):

            prompt = f"""
Summarize the following notes.

Also provide:
- Important Points
- 2 Mark Questions
- 5 Mark Questions

Notes:
{text[:10000]}
"""

            response = get_gemini_response(prompt)

            st.markdown(response)

# ====================================================
# TAB 3 - QUIZ GENERATOR
# ====================================================

with tab3:

    st.subheader("Quiz Generator")

    quiz_topic = st.text_input(
        "Quiz Topic",
        placeholder="DBMS"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("Generate Quiz"):

        prompt = f"""
Generate 10 MCQs on {quiz_topic}

Difficulty: {difficulty}

Give answers at the end.
"""

        response = get_gemini_response(prompt)

        st.markdown(response)

# ====================================================
# TAB 4 - STUDY PLANNER
# ====================================================

with tab4:

    st.subheader("Study Planner")

    subject = st.text_input(
        "Subject Name"
    )

    days = st.number_input(
        "Days Left for Exam",
        min_value=1,
        max_value=365,
        value=7
    )

    if st.button("Generate Study Plan"):

        prompt = f"""
Create a {days}-day study plan for {subject}.

Make it suitable for a college student.

Include:
- Daily Targets
- Revision Plan
- Practice Questions
"""

        response = get_gemini_response(prompt)

        st.markdown(response)