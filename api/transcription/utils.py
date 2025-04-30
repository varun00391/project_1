import os
import glob
import whisper
import tempfile
import subprocess




class TranscriptionPipeline:
    def __init__(self,model='base'):
        self.model = model

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


    
        