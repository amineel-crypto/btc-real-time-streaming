# producer/Dockerfile
FROM python:3.10.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "-u", "app.py"]


