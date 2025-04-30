import streamlit as st
import requests
import os

# Load backend URLs from environment variables or defaults
SUMMARIZATION_API = os.getenv("SUMMARIZATION_API_URL", "http://localhost:8000/summarization")
RAG_API = os.getenv("RAG_API_URL", "http://localhost:8000/rag-chatbot")

st.set_page_config(page_title="Multimodal AI Assistant", layout="wide")
st.title("📚 Multimodal AI Assistant")

# Sidebar Navigation
option = st.sidebar.radio("Choose a Feature", ["📄 PDF Summarization", "📺 YouTube Transcription", "🤖 RAG Chatbot"])

# ----------------- PDF Summarization -----------------
if option == "📄 PDF Summarization":
    st.subheader("📄 Upload a PDF to Summarize")
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    
    if uploaded_file:
        with st.spinner("Summarizing PDF..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            try:
                response = requests.post(f"{SUMMARIZATION_API}/summarize-pdf", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Summary Generated")
                    st.text_area("Summary", result["summary"], height=300)
                else:
                    st.error(f"❌ Error: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Could not connect to the Summarization API.")

# ----------------- YouTube Transcription -----------------
elif option == "📺 YouTube Transcription":
    st.subheader("🎙️ Transcribe or Summarize a YouTube Video")
    youtube_url = st.text_input("Enter YouTube Video URL")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Transcribe"):
            if youtube_url:
                with st.spinner("Transcribing video..."):
                    try:
                        res = requests.post(f"{SUMMARIZATION_API}/video-transcription", data={"url": youtube_url})
                        if res.status_code == 200:
                            transcription = res.json()["transcription"]
                            st.text_area("📄 Transcription", transcription, height=300)
                        else:
                            st.error(f"Error: {res.json().get('detail')}")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Could not connect to the API.")

    with col2:
        if st.button("Summarize"):
            if youtube_url:
                with st.spinner("Summarizing video..."):
                    try:
                        res = requests.post(f"{SUMMARIZATION_API}/summarize-youtube", data={"url": youtube_url})
                        if res.status_code == 200:
                            summary = res.json()["summary"]
                            st.text_area("📄 Summary", summary, height=300)
                        else:
                            st.error(f"Error: {res.json().get('detail')}")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Could not connect to the API.")
elif option == "🤖 RAG Chatbot":
    st.subheader("💬 Chat with a PDF or YouTube Video (RAG Chatbot)")

    source_type = st.radio("Choose your source", ["PDF File", "YouTube Video"], horizontal=True)
    query = st.text_input("Enter your question")

    if source_type == "PDF File":
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    else:
        youtube_url = st.text_input("Enter YouTube Video URL")

    if st.button("Ask"):
        if not query:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating response..."):
                try:
                    if source_type == "PDF File" and uploaded_file:
                        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                        data = {"question": query}
                        res = requests.post(f"{RAG_API}/ask", data=data, files=files)

                    elif source_type == "YouTube Video" and youtube_url:
                        data = {"question": query, "url": youtube_url}
                        res = requests.post(f"{RAG_API}/ask", data=data)

                    else:
                        st.error("Please upload a PDF or enter a YouTube URL.")
                        res = None

                    if res and res.status_code == 200:
                        answer = res.json()["response"]
                        st.markdown(f"**🧠 Answer:**\n\n{answer}")
                    elif res:
                        st.error(f"Error: {res.json().get('detail', res.text)}")

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to the RAG API.")
