#main.py file for final api


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import shutil
import os

app = FastAPI()

def read_pdf(file_path):
    """Extract text from a PDF using PyMuPDF."""
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

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

    return {"filename": file.filename, "extracted_text": text}

