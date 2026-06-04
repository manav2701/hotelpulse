# Stage 1: Build Next.js Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python backend
COPY . .

# Copy compiled Next.js frontend to /app/frontend/out
COPY --from=frontend-builder /app/frontend/out /app/frontend/out

RUN mkdir -p data/raw data/processed artifacts mlruns

EXPOSE 8501

# Run ML pipeline, then start FastAPI server
CMD ["sh", "-c", "python src/pipeline/run_pipeline.py && uvicorn src.api.main:app --host 0.0.0.0 --port 8501"]
