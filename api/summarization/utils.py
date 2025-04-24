# # #utils.py file for utility functions

# # #main.py file for final api

# # import fitz  # PyMuPDF
# # import os
# # from groq import Groq
# # from dotenv import load_dotenv
# # from api.summarization.helper import read_pdf,summarize_chunk,split_text

# # load_dotenv()

# # # # Load Groq API key from env
# # groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# # def summarization(text: str,model="meta-llama/llama-4-maverick-17b-128e-instruct") -> str:
# #     """Split text and summarize each chunk, then combine summaries."""
# #     try:
# #         chunks = split_text(text)
# #         summaries = []
# #         for i, chunk in enumerate(chunks):
# #             summary = summarize_chunk(chunk)
# #             summaries.append(f"Chunk {i+1} Summary:\n{summary}")
# #         combined_summaries = "\n\n".join(summaries)

# #         # More detailed prompt
# #         detailed_prompt = f"""
# #         You are an intelligent and concise summarizer.

# #         Your task is to read through the section summaries below, understand the overall content, and write a comprehensive summary of the document.
    
# #         The final summary should:
# #         - Capture the key concepts, arguments, or narrative from the text.
# #         - Avoid repetition.
# #         - Be clear, concise, and factually accurate.
# #         - Preserve technical or domain-specific language if needed.
# #         - Be written in a neutral and professional tone.
# #         - Do NOT include any analysis or assumptions.
# #         - Do NOT add introductory or closing phrases like "This document is about..."

# #         Here are the section summaries:

# #         {combined_summaries}

# #         Write the final summary below. Do not include any additional explanation or preamble.
# #         """

        
# #         # Final summary of all chunks
# #         response = groq_client.chat.completions.create(
# #             model=model,
# #             messages=[
# #                 {"role": "system", "content": "You are a helpful assistant who creates final summaries from section summaries."},
# #                 {"role": "user", "content": detailed_prompt.strip()}
# #             ],
# #             max_tokens=500,
# #             temperature=0.5
# #         )
# #         return response.choices[0].message.content.strip()
# #     except Exception as e:
# #         return f"Error generating final summary: {e}"    


# from fastapi import APIRouter, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# from api.summarization.helper import SummarizationPipeline
# import tempfile
# import os

# router = APIRouter()
# summarizer = SummarizationPipeline()

# @router.post("/")
# async def summarize_pdf(file: UploadFile = File(...)):
#     # Save uploaded file temporarily
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(await file.read())
#         tmp_path = tmp.name

#     try:
#         # Read and summarize the PDF
#         text = summarizer.read_pdf(tmp_path)
#         summary = summarizer.summarize_document(text)
#         return JSONResponse(content={"summary": summary})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         os.remove(tmp_path)  # Cleanup temp file


from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from api.summarization.helper import SummarizationPipeline
import tempfile
import os

router = APIRouter()
summarizer = SummarizationPipeline()

@router.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    """Endpoint to summarize uploaded PDF files."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        text = summarizer.read_pdf(tmp_path)
        summary = summarizer.summarize_document(text)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF summarization failed: {str(e)}")
    finally:
        os.remove(tmp_path)

@router.post("/summarize-youtube")
async def summarize_youtube(url: str = Form(...)):
    """Endpoint to summarize YouTube videos."""
    try:
        summary = summarizer.summarize_youtube(url)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YouTube summarization failed: {str(e)}")







