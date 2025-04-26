from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from api.summarization.utils import SummarizationPipeline
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







