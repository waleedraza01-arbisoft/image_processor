# Use a slim Python base
FROM python:3.9-slim-bullseye

WORKDIR /app

# Install system dependencies needed for OpenCV
# libgl1-mesa-glx and libglib2.0-0 are low-level graphics libraries required by cv2
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

# Install dependencies (Very fast!)
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]