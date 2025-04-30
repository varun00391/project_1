import fitz  # PyMuPDF
import os
from groq import Groq
from dotenv import load_dotenv
import subprocess
import whisper
import tempfile
import glob

load_dotenv()

class SummarizationPipeline:
    def __init__(self, model="meta-llama/llama-4-maverick-17b-128e-instruct", max_tokens=300):
        self.model = model
        self.max_tokens = max_tokens
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def download_audio_with_ytdlp_temp(self, url):
        """Download YouTube audio to a temp folder."""
        tmp_dir = tempfile.TemporaryDirectory()
        output_template = os.path.join(tmp_dir.name, "%(title)s.%(ext)s")

        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", output_template,
            url
        ]

        subprocess.run(command, check=True)

        # Find the downloaded .mp3 file
        mp3_files = glob.glob(os.path.join(tmp_dir.name, "*.mp3"))
        if not mp3_files:
            raise Exception("No MP3 file found after download.")
        
        return mp3_files[0], tmp_dir

    def transcribe_youtube_video(self, url):
        """Download and transcribe YouTube audio."""
        print("[1] Downloading audio to temp folder...")
        audio_file_path, tmp_dir = self.download_audio_with_ytdlp_temp(url)

        try:
            print(f"[2] Audio file downloaded: {audio_file_path}")

            print("[3] Loading Whisper model...")
            model = whisper.load_model("base")  # or 'small', 'medium', etc.

            print("[4] Transcribing...")
            result = model.transcribe(audio_file_path)

            print("[5] Transcription complete!\n")
            return result["text"]

        finally:
            # Always clean up the temp folder
            tmp_dir.cleanup()
            print(f"[6] Temp folder {tmp_dir.name} deleted.")

    def read_pdf(self, file_path):
        """Extract text from a PDF using PyMuPDF."""
        text = ""
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        except Exception as e:
            return f"Error reading PDF: {e}"

    def split_text(self, text, max_words=3000):
        """Split text into chunks of max_words."""
        words = text.split()
        return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

    def summarize_chunk(self, chunk):
        """Summarize a single chunk using Groq."""
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who summarizes documents."},
                    {"role": "user", "content": f"Please summarize this:\n\n{chunk}"}
                ],
                max_tokens=self.max_tokens,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error summarizing chunk: {e}"
        
    def summarize_youtube(self, url):
        """Download, transcribe, and summarize a YouTube video."""
        try:
            transcript = self.transcribe_youtube_video(url)
            summary = self.summarize_document(transcript)
            return summary
        except Exception as e:
            return f"Error summarizing YouTube video: {e}"


    def summarize_document(self, text):
        """Split text and summarize each chunk, then create a final summary."""
        try:
            chunks = self.split_text(text)
            summaries = []
            for i, chunk in enumerate(chunks):
                summary = self.summarize_chunk(chunk)
                summaries.append(f"Chunk {i+1} Summary:\n{summary}")
            combined_summaries = "\n\n".join(summaries)

            final_prompt = f"""
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

            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who creates final summaries from section summaries."},
                    {"role": "user", "content": final_prompt.strip()}
                ],
                max_tokens=500,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating final summary: {e}"
