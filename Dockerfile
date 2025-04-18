# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire service folder into /app
COPY service/ .

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "service.views:app", "--host", "0.0.0.0", "--port", "8000"]

