FROM python:3.11-slim

# Faster, cleaner Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (cache-friendly, explicit paths)
COPY ["requirements.txt", "/app/requirements.txt"]
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copy source code
COPY ["src", "/app/src"]
COPY ["components", "/app/components"]

# Default command: simple sanity message
CMD ["python", "-c", "print('Container is ready for Vertex Pipelines.')"]