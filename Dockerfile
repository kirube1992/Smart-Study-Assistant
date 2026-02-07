# Smart Study Assistant - Multi-stage Docker Build
# Stage 1: Backend (FastAPI)
FROM python:3.11-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY src/ ./src/
COPY api.py .
COPY App.py .
COPY data/ ./data/

# Expose API port
EXPOSE 8000

# Health check

# Start FastAPI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 2: Frontend (Next.js)
FROM node:20-alpine as frontend-builder

WORKDIR /app

# Copy frontend files
COPY package.json pnpm-lock.yaml ./

# Install dependencies using pnpm
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Copy frontend code
COPY app/ ./app/
COPY components/ ./components/
COPY next.config.ts tsconfig.json tailwind.config.ts postcss.config.js ./

# Build Next.js
RUN pnpm build

# Stage 3: Frontend Runtime
FROM node:20-alpine as frontend

WORKDIR /app

# Copy built app from builder
COPY --from=frontend-builder /app/node_modules ./node_modules
COPY --from=frontend-builder /app/.next ./.next
COPY --from=frontend-builder /app/public ./public
COPY --from=frontend-builder /app/package.json ./

# Expose frontend port
EXPOSE 3000

# Start Next.js
CMD ["npm", "start"]
