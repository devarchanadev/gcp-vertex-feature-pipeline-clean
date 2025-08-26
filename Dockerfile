FROM python:3.11-slim

# faster, cleaner Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# system dependencies (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install Python deps first (cache-friendly)
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy source (empty for now except our folders)
COPY src /app/src
COPY components /app/components

# default command: print a message so we can verify the image runs
CMD ["python", "-c", "print('Container is ready for Vertex Pipelines.')"]
