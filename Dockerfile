FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install OS-level dependencies (e.g., ffmpeg for Whisper, yt-dlp)
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

# Copy all files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r api/requirements.txt

# Default command
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
