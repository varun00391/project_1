import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.rag_chatbot.views import router as rag_router
from api.summarization.views import router as summarizer_router
from api.transcription.views import router as transcription_router


app = FastAPI(
    title="Multimodal Summarizer & RAG API",
    description="Summarize PDFs, YouTube videos, and interact with a RAG-based chatbot using FastAPI.",
    version="2.0.0"
)

# Add the list of routes we want to allow
origins = ["*"]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rag_router, prefix="/rag-chatbot", tags=["RAG Chatbot"])
# app.include_router(summarizer_router, prefix="/summarization and Transcription", tags=["Summarization"])
app.include_router(summarizer_router, prefix="/summarization", tags=["Summarization & Transcription"])
app.include_router(transcription_router,prefix="/Transcription",tags=["Transcription"])


if (__name__ == "__main__"):
    uvicorn.run("main:app", reload=True, port=8000)