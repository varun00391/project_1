# import tempfile
# import sys
# import os

# # # Adjust Python path to find 'API' module
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from api.summarization.utils import SummarizationPipeline

# summarizer = SummarizationPipeline()

# def transcript_pdf_file(uploaded_file):
#     """Takes a Streamlit uploaded PDF and returns its summary."""
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(uploaded_file.read())
#         tmp_path = tmp.name

#     try:
#         text = summarizer.read_pdf(tmp_path)
#         # summary = summarizer.summarize_document(text)
#         return text   #summary
#     except Exception as e:
#         return f"PDF text extraction failed: {str(e)}"
#     finally:
#         os.remove(tmp_path)

import tempfile
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.summarization.utils import SummarizationPipeline

summarizer = SummarizationPipeline()

def transcript_pdf_file(uploaded_file):
    """Extracts text from PDF and optionally returns a summary."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        text = summarizer.read_pdf(tmp_path)
        # if return_summary:
        #     summary = summarizer.summarize_document(text)
        return text
    except Exception as e:
        return f"PDF processing failed: {str(e)}"
    finally:
        os.remove(tmp_path)
