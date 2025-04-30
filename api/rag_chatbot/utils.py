import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import subprocess
import whisper
import tempfile
import glob

load_dotenv()  # load variables from .env into environment

groq_api_key = os.getenv("GROQ_API_KEY")

class RAGPipeline:
    def __init__(self, embedding_model="BAAI/bge-small-en", device="cpu"):
        self.embedding_model = embedding_model
        self.device = device
        self.embeddings = self._load_embeddings()

        print("[0] Loading Whisper model once...")
        self.whisper_model = whisper.load_model("base")  # Load once here
    
    def _load_embeddings(self):
        model_kwargs = {"device": self.device}
        encode_kwargs = {"normalize_embeddings": True}
        return HuggingFaceBgeEmbeddings(
            model_name=self.embedding_model,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

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
            
    # def download_audio_with_ytdlp_temp(self, url):
    #     tmp_dir = tempfile.TemporaryDirectory()
    #     output_template = os.path.join(tmp_dir.name, "%(title)s.%(ext)s")

    #     command = [
    #         "yt-dlp",
    #         "-f", "bestaudio",
    #         "--extract-audio",
    #         "--audio-format", "mp3",
    #         "--output", output_template,
    #         url
    #     ]

    #     subprocess.run(command, check=True)

    #     mp3_files = glob.glob(os.path.join(tmp_dir.name, "*.mp3"))
    #     if not mp3_files:
    #         raise Exception("No MP3 file found after download.")
        
    #     return mp3_files[0], tmp_dir

    # def transcribe_youtube_video(self, url):
    #     print("[1] Downloading audio...")
    #     audio_file_path, tmp_dir = self.download_audio_with_ytdlp_temp(url)

    #     try:
    #         print(f"[2] Audio file downloaded: {audio_file_path}")
    #         print("[3] Transcribing...")
    #         result = self.whisper_model.transcribe(audio_file_path)
    #         print("[4] Transcription complete!")
    #         return result["text"]
    #     finally:
    #         tmp_dir.cleanup()
    #         print(f"[5] Temp folder {tmp_dir.name} deleted.")
    
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



# class RAGPipeline:
#     def __init__(self, embedding_model="BAAI/bge-small-en", device="cpu"):
#         self.embedding_model = embedding_model
#         self.device = device
#         self.embeddings = self._load_embeddings()

#         # Load Whisper model ONCE here
#         print("[0] Loading Whisper model once...")
#         self.whisper_model = whisper.load_model("base")  # or 'small', 'medium', etc.
    
#     def _load_embeddings(self):
#         model_kwargs = {"device": self.device}
#         encode_kwargs = {"normalize_embeddings": True}
#         return HuggingFaceBgeEmbeddings(
#             model_name=self.embedding_model,
#             model_kwargs=model_kwargs,
#             encode_kwargs=encode_kwargs,
#         )

#     def download_audio_with_ytdlp_temp(self, url):
#         """Download YouTube audio to a temp folder."""
#         tmp_dir = tempfile.TemporaryDirectory()
#         output_template = os.path.join(tmp_dir.name, "%(title)s.%(ext)s")

#         command = [
#             "yt-dlp",
#             "-f", "bestaudio",
#             "--extract-audio",
#             "--audio-format", "mp3",
#             "--output", output_template,
#             url
#         ]

#         subprocess.run(command, check=True)

#         # Find the downloaded .mp3 file
#         mp3_files = glob.glob(os.path.join(tmp_dir.name, "*.mp3"))
#         if not mp3_files:
#             raise Exception("No MP3 file found after download.")
        
#         return mp3_files[0], tmp_dir

#     def transcribe_youtube_video(self, url):
#         """Download and transcribe YouTube audio."""
#         print("[1] Downloading audio to temp folder...")
#         audio_file_path, tmp_dir = self.download_audio_with_ytdlp_temp(url)

#         try:
#             print(f"[2] Audio file downloaded: {audio_file_path}")

#             print("[3] Loading Whisper model...")
#             model = whisper.load_model(audio_file_path)  # or 'small', 'medium', etc.

#             print("[4] Transcribing...")
#             result = model.transcribe(audio_file_path)

#             print("[5] Transcription complete!\n")
#             return result["text"]

#         finally:
#             # Always clean up the temp folder
#             tmp_dir.cleanup()
#             print(f"[6] Temp folder {tmp_dir.name} deleted.")
    
#     def load_pdf(self, file_path):
#         loader = PyPDFLoader(file_path)
#         return loader.load()
    
#     def split_documents(self, documents, chunk_size=500, chunk_overlap=100):
#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size, chunk_overlap=chunk_overlap
#         )
#         return splitter.split_documents(documents)

#     def create_vectorstore(self, docs):
#         return FAISS.from_documents(docs, self.embeddings)
    
#     def get_llm(self, model="meta-llama/llama-4-maverick-17b-128e-instruct"): 
#         return ChatGroq(model=model)
    
#     def ask_question(self, vectorstore, question, llm):
#         retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
#         qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
#         return qa.invoke(question)
