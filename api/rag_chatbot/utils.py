import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

load_dotenv()  # load variables from .env into environment

groq_api_key = os.getenv("GROQ_API_KEY")


class RAGPipeline:
    def __init__(self, embedding_model="BAAI/bge-small-en", device="cpu"):
        self.embedding_model = embedding_model
        self.device = device
        self.embeddings = self._load_embeddings()
    
    def _load_embeddings(self):
        model_kwargs = {"device": self.device}
        encode_kwargs = {"normalize_embeddings": True}
        return HuggingFaceBgeEmbeddings(
            model_name=self.embedding_model,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
    
    def load_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    def split_documents(self, documents, chunk_size=500, chunk_overlap=100):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        return splitter.split_documents(documents)

    def create_vectorstore(self, docs):
        return FAISS.from_documents(docs, self.embeddings)
    
    def get_llm(self, model="meta-llama/llama-4-maverick-17b-128e-instruct"): 
        return ChatGroq(model=model)
    
    def ask_question(self, vectorstore, question, llm):
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        return qa.invoke(question)
