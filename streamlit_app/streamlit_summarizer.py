# streamlit_app/streamlit_summarizer.py

import tempfile
import sys
import os

# Adjust Python path to find 'API' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.summarization.utils import SummarizationPipeline

summarizer = SummarizationPipeline()

def summarize_pdf_file(uploaded_file):
    """Takes a Streamlit uploaded PDF and returns its summary."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        text = summarizer.read_pdf(tmp_path)
        summary = summarizer.summarize_document(text)
        return summary
    except Exception as e:
        return f"PDF summarization failed: {str(e)}"
    finally:
        os.remove(tmp_path)
