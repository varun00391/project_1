from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from api.transcription.utils import TranscriptionPipeline
import tempfile
import os

router = APIRouter()
summarizer = TranscriptionPipeline()

@router.post("/video-transcription")
async def transcription(url: str = Form(...)):
    """Endpoint to transcribe YouTube videos."""

    try:
        transcription = summarizer.transcribe_youtube_video(url)
        return JSONResponse(content={"transcription": transcription})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

