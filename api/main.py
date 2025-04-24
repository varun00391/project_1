from fastapi import FastAPI
from api.rag_chatbot.utils import router as rag_router
from api.summarization.utils import router as summarize_router

# app = FastAPI()

app = FastAPI(
    title="Multimodal Summarizer & RAG API",
    description="Summarize PDFs, YouTube videos, and interact with a RAG-based chatbot using FastAPI.",
    version="2.0.0"
)


app.include_router(rag_router, prefix="/rag-chatbot", tags=["RAG Chatbot"])
app.include_router(summarize_router, prefix="/summarize", tags=["Summarization"])