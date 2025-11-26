# Stage 1: Build image to install dependencies
FROM python:3.10-slim AS builder

# Set working directory inside the container
WORKDIR /app

# Install dependencies required for building some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies to a temporary folder
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Stage 2: Final lightweight runtime image

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy your whole app folder (FastAPI + FAISS + PDF + index)
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Default environment variables
ENV PYTHONUNBUFFERED=1

# Command to run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
