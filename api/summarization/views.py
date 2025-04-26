from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from api.summarization.utils import SummarizationPipeline
import tempfile
import os

router = APIRouter()
summarizer = SummarizationPipeline()


# @router.post("/summarize")
# async def summarize(
#     file: Optional[UploadFile] = File(None),
#     url: Optional[str] = Form(None)
# ):
#     """Unified endpoint to summarize either a PDF file or a YouTube video."""
#     if not file and not url:
#         raise HTTPException(status_code=400, detail="Please upload a PDF file or provide a YouTube URL.")

#     if file:
#         if not file.filename.endswith(".pdf"):
#             raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")
        
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#             tmp.write(await file.read())
#             tmp_path = tmp.name

#         try:
#             text = summarizer.read_pdf(tmp_path)
#             summary = summarizer.summarize_document(text)
#             return JSONResponse(content={"summary": summary})
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"PDF summarization failed: {str(e)}")
#         finally:
#             os.remove(tmp_path)

#     elif url:
#         try:
#             summary = summarizer.summarize_youtube(url)
#             return JSONResponse(content={"summary": summary})
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"YouTube summarization failed: {str(e)}")

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







