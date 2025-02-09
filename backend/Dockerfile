FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (including curl for downloading static files)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    krb5-user \
    libkrb5-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download static files from CDN into the ./static directory
RUN mkdir -p static && \
    curl -o static/swagger-ui-bundle.js https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js && \
    curl -o static/swagger-ui.css https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css && \
    curl -o static/redoc.standalone.js https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js

# Copy the FastAPI application code
COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
