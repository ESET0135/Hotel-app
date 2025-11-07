# Use an official lightweight Python image
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose Render's dynamic port (optional but good practice)
EXPOSE 10000

# Use Render's dynamic port environment variable
CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]
