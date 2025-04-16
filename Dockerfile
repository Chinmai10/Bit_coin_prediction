# Use a smaller base image with build tools first
FROM python:3.10-slim AS builder

# Set environment variables to reduce size
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements and install dependencies to avoid rebuilds
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
FROM python:3.10-slim

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/include /usr/local/include

# Copy your source code
COPY . .

# Expose the app port
EXPOSE 8080

# Run the app
CMD ["uvicorn", "BITCOIN_PREDICTION:app", "--host", "0.0.0.0", "--port", "8080"]
