# syntax = docker/dockerfile:1.4

# Base image
FROM tiangolo/uvicorn-gunicorn:python3.11 AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy application code
COPY ./app ./app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose the application port
EXPOSE 8000

# Set the entrypoint command for development with live reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
