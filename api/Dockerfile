# api/DockerFile

# Use official lightweight Python image

FROM python:3.10.11-slim

# Set the working directory inside the container

WORKDIR /app

# Copy and install Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code 
COPY main.py .

# Expose FastAPI default port 
EXPOSE 8000

# Run the FastAPI app using Uvicorn 
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]