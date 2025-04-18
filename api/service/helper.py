#helper.py file for helper functions

import fitz  # PyMuPDF
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Load Groq API key from env
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))



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
    
def split_text(text, max_words=3000):
    """Split text into chunks of max_words."""
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def summarize_chunk(chunk, model="meta-llama/llama-4-maverick-17b-128e-instruct", max_tokens=300): # meta-llama/llama-4-scout-17b-16e-instruct
    """Summarize a single chunk using Groq."""
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who summarizes documents."},
                {"role": "user", "content": f"Please summarize this:\n\n{chunk}"}
            ],
            max_tokens=max_tokens,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing chunk: {e}"