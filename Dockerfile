# Small, pinned base image reduces attack surface
FROM python:3.12-slim

# Patch known OS-level vulnerabilities in the base image
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Create a non-root user (containers should not run as root)
RUN useradd --create-home --uid 1000 appuser
WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
