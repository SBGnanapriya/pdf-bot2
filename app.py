import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="PDF Q&A Bot", layout="wide")
st.title("📄 PDF Question Answering Bot (Gemini)")

# ---------------- GEMINI SETUP ----------------
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("models/gemini-1.5-flash")
except Exception as e:
    st.error("❌ Gemini API key not configured")
    st.stop()

# ---------------- PDF UPLOAD ----------------
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

pdf_text = ""

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"
        st.success("✅ PDF loaded successfully")
    except Exception as e:
        st.error("❌ Failed to read PDF")
        st.stop()

# ---------------- QUESTION ----------------
question = st.text_input("Ask any question from the PDF")

def ask_gemini(context, question):
    prompt = f"""
You are an expert tutor.

Use ONLY the content from the PDF below to answer.
Explain clearly in at least 8–10 lines.
If the answer does NOT exist in the PDF, say:
"Answer not found in the provided document."

PDF CONTENT:
{context}

QUESTION:
{question}
"""
    response = model.generate_content(prompt)
    return response.text

# ---------------- ANSWER ----------------
if question and pdf_text:
    with st.spinner("Thinking..."):
        answer = ask_gemini(pdf_text, question)
        st.subheader("✅ Answer")
        st.write(answer)
