import whisper
import subprocess

def download_audio_with_ytdlp(url, output_filename="yt_audio.mp3"):
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_filename,
        url
    ]
    subprocess.run(command, check=True)
    return output_filename

def transcribe_youtube_video(url):
    print("[1] Downloading audio with yt-dlp...")
    audio_file = download_audio_with_ytdlp(url)

    print("[2] Loading Whisper model...")
    model = whisper.load_model("base")

    print("[3] Transcribing...")
    result = model.transcribe(audio_file)

    print("[4] Transcription complete!\n")
    print(result["text"])

# Example usage
video_url = "https://www.youtube.com/watch?v=gywke3XiNC0&list=PLdpzxOOAlwvJdsW6A0jCz_3VaANuFMLpc&index=3"  # Replace with your video link
transcribe_youtube_video(video_url)
