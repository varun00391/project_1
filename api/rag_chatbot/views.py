from fastapi import UploadFile, File, Form, APIRouter
from fastapi.responses import JSONResponse
from typing import Optional,Union
from api.rag_chatbot.utils import RAGPipeline
import tempfile
import os
from langchain.schema import Document

router = APIRouter()
pipeline = RAGPipeline()


@router.post("/ask")
async def ask_question(
    question: str = Form(...),
    file: Optional[Union[UploadFile, str]] = File(None),
    url: Optional[str] = Form(default=None)
):
    # Normalize file parameter: if file is an empty string, treat it as None.
    if file and isinstance(file, str):
        if file.strip() == "":
            file = None
        else:
            return JSONResponse(content={"error": "Invalid file provided."}, status_code=400)
    try:
        # if file and file.filename:
        if file:  # is not None and file.filename:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            try:
                docs = pipeline.load_pdf(tmp_path)
            finally:
                os.remove(tmp_path)

        elif url:
            transcription = pipeline.transcribe_youtube_video(url)
            print("Transcription:", transcription[:200])  # Debug only
            docs = [Document(page_content=transcription, metadata={"source": url})]

        else:
            return JSONResponse(
                content={"error": "Please upload a PDF file or provide a YouTube URL."},
                status_code=400
            )

        chunks = pipeline.split_documents(docs)
        vectorstore = pipeline.create_vectorstore(chunks)
        llm = pipeline.get_llm()
        response = pipeline.ask_question(vectorstore, question, llm)

        # response from RetrievalQA.invoke is usually a dict with "result" key
        if isinstance(response, dict):
            result_text = response.get("result") or response.get("output")
        else:
            result_text = str(response)

        return JSONResponse(content={"response": result_text})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)