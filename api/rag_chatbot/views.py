# from fastapi import UploadFile, File, Form, APIRouter
# from fastapi.responses import JSONResponse
# from api.rag_chatbot.utils import RAGPipeline
# import tempfile
# import os

# router = APIRouter()
# pipeline = RAGPipeline()

# @router.post("")
# async def ask_question_from_pdf(file: UploadFile = File(...), question: str = Form(...)):
#     # Save the uploaded PDF temporarily
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(await file.read())
#         tmp_path = tmp.name

#     try:
#         # Process PDF with the RAG pipeline
#         docs = pipeline.load_pdf(tmp_path)
#         chunks = pipeline.split_documents(docs)
#         vectorstore = pipeline.create_vectorstore(chunks)
#         llm = pipeline.get_llm()
#         response = pipeline.ask_question(vectorstore, question, llm)
#         return JSONResponse(content={"response": response['result']})
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
#     finally:
#         os.remove(tmp_path)  # Always clean up temp file

from fastapi import UploadFile, File, Form, APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Optional
from api.rag_chatbot.utils import RAGPipeline
import tempfile
import os

router = APIRouter()
pipeline = RAGPipeline()

@router.post("/ask")
async def ask_question(
    request: Request,
    question: str = Form(...),
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
):
    """Ask a question from either a PDF file or a YouTube video."""
    try:
        if file and file.filename:
            # Process PDF file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            try:
                docs = pipeline.load_pdf(tmp_path)
            finally:
                os.remove(tmp_path)

        elif url:
            # Process YouTube URL
            docs = [{"page_content": pipeline.transcribe_youtube_video(url)}]

        else:
            return JSONResponse(content={"error": "Please upload a PDF file or provide a YouTube URL."}, status_code=400)

        # Common RAG logic
        chunks = pipeline.split_documents(docs)
        vectorstore = pipeline.create_vectorstore(chunks)
        llm = pipeline.get_llm()
        response = pipeline.ask_question(vectorstore, question, llm)

        return JSONResponse(content={"response": response['result']})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

