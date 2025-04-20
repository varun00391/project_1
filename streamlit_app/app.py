import streamlit as st
import requests

st.set_page_config(page_title="PDF Summarizer", layout="centered")

st.title("📄 PDF Summarizer using LLM")
st.write("Upload a PDF file and get a smart summary generated using Groq's LLM.")

uploaded_file = st.sidebar.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Uploading and summarizing..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        try:
            response = requests.post("http://summarization-api:8000/extract-pdf-text/", files=files)
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ Summary for: {result['filename']}")
                st.text_area("Summary", result['summary'], height=300)
            else:
                st.error(f"❌ Error: {response.json().get('error')}")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Could not connect to FastAPI server. Make sure it's running.")
