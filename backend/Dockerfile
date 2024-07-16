# Use an official Python runtime as a parent image
FROM python:3.12.4-slim AS base

# Set the working directory in the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY app /app

# Development stage
FROM base AS development
# Install additional development dependencies if needed
RUN pip install debugpy

# Set the command to run the development server with --reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM python:3.12.4-slim AS production
WORKDIR /app
COPY --from=base /app /app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
