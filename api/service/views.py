#views.py file for viewing api

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from api.service.utils import read_pdf,summarization

app = FastAPI()


@app.post("/extract-pdf-text/")
async def extract_pdf_text(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed."})

    # Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read and extract text
    text = read_pdf(temp_path)

    # Delete temporary file
    os.remove(temp_path)

    summary = summarization(text)

    return {"filename": file.filename, 
            "summary": summary
            }