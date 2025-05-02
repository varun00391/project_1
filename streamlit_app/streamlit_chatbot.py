import tempfile
import sys
import os

# Adjust Python path to find 'API' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.rag_chatbot.utils import RAGPipeline

chatbot = RAGPipeline()


def ask_question(uploaded_file,question):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        docs = chatbot.load_pdf(tmp_path)
        chunks = chatbot.split_documents(docs)
        vectorstore = chatbot.create_vectorstore(chunks)
        llm = chatbot.get_llm()
        response = chatbot.ask_question(vectorstore,question,llm)

        # Extract and return answer
        if isinstance(response, dict):
            return response.get("result") or response.get("output")
        return str(response)
    
    except Exception as e:
        return f"Chatbot Failed: {str(e)}"
    finally:
        os.remove(tmp_path)

