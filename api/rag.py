import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

load_dotenv()  # load variables from .env into environment

groq_api_key = os.getenv("GROQ_API_KEY")


# Step 1: Load PDF
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

# Step 2: Split into text chunks
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(documents)

def embeddings():
    model_name = "BAAI/bge-small-en"     # BAAI/bge-small-en, BAAI/bge-large-en-v1.5, BAAI/bge-base-en-v1.5
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return embeddings


# Step 3: Embed and store in Pinecone
def create_vectorstore(docs,embeddings):
    return FAISS.from_documents(docs, embeddings)

def llm_model(model="meta-llama/llama-4-maverick-17b-128e-instruct"):
    return ChatGroq(model=model)


# Step 4: Query with LLM
def ask_question(vectorstore, question, llm):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    # qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    qa = RetrievalQA.from_chain_type(llm=ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct"), retriever=retriever)
    return qa.invoke(question)


# Example Run
if __name__ == "__main__":
    docs = load_pdf("varun_negi.pdf")
    chunks = split_documents(docs)
    embeddings = embeddings()
    llm = llm_model()
    vectorstore = create_vectorstore(chunks,embeddings)  # Don't save to disk

    # vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    query = "name of company and its complete location"
    response = ask_question(vectorstore, query,llm)
    print("Response:", response['result'])
