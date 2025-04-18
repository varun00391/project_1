#utils.py file for utility functions

#main.py file for final api

import fitz  # PyMuPDF
import os
from groq import Groq
from dotenv import load_dotenv
from api.service.helper import read_pdf,summarize_chunk,split_text

load_dotenv()

# # Load Groq API key from env
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarization(text: str,model="meta-llama/llama-4-maverick-17b-128e-instruct") -> str:
    """Split text and summarize each chunk, then combine summaries."""
    try:
        chunks = split_text(text)
        summaries = []
        for i, chunk in enumerate(chunks):
            summary = summarize_chunk(chunk)
            summaries.append(f"Chunk {i+1} Summary:\n{summary}")
        combined_summaries = "\n\n".join(summaries)

        # More detailed prompt
        detailed_prompt = f"""
        You are an intelligent and concise summarizer.

        Your task is to read through the section summaries below, understand the overall content, and write a comprehensive summary of the document.

        The final summary should:
        - Capture the key concepts, arguments, or narrative from the text.
        - Avoid repetition.
        - Be clear, concise, and factually accurate.
        - Preserve technical or domain-specific language if needed.
        - Be written in a neutral and professional tone.
        - Do NOT include any analysis or assumptions.
        - Do NOT add introductory or closing phrases like "This document is about..."

        Here are the section summaries:

        {combined_summaries}

        Write the final summary below. Do not include any additional explanation or preamble.
        """

        
        # Final summary of all chunks
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who creates final summaries from section summaries."},
                {"role": "user", "content": detailed_prompt.strip()}
            ],
            max_tokens=500,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating final summary: {e}"    

    





