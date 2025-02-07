FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for Kerberos
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    krb5-user \
    libkrb5-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]