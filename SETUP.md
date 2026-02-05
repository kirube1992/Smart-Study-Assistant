# Smart Study Assistant - Complete Setup Guide

Welcome! This guide will help you get the Smart Study Assistant up and running on your local machine.

## Prerequisites

Make sure you have the following installed:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **Docker & Docker Compose** (optional, for containerized setup) - [Download](https://www.docker.com/)

## Quick Start (Local Development)

### Option 1: Manual Setup (Recommended for Development)

#### Step 1: Clone and Navigate to Project

```bash
cd Smart-Study-Assistant
```

#### Step 2: Setup Python Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirment.txt
```

#### Step 3: Prepare Data Directory

```bash
# Create data directory if it doesn't exist
mkdir -p data
```

#### Step 4: Start FastAPI Backend

```bash
# From the project root directory
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

The API is now running at `http://localhost:8000`

#### Step 5: In a New Terminal, Setup Frontend

```bash
# Navigate to project directory (with venv deactivated or in new terminal)

# Install Node dependencies
npm install
# or
pnpm install

# Start Next.js development server
npm run dev
# or
pnpm dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

#### Step 6: Access the Application

Open your browser and go to: `http://localhost:3000`

You should see the Smart Study Assistant homepage!

---

### Option 2: Docker Setup (One Command)

If you have Docker installed, you can run everything in containers:

```bash
# Navigate to project directory
cd Smart-Study-Assistant

# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

This will:
- Start the FastAPI backend on `http://localhost:8000`
- Start the Next.js frontend on `http://localhost:3000`
- Create a shared network between containers
- Mount volumes for live code changes

Access the application at: `http://localhost:3000`

To stop services:
```bash
docker-compose down
```

---

## Verifying Installation

### Check Backend Health

```bash
# Terminal 1 (API should be running)
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "api_version": "1.0.0",
  "service": "Smart Study Assistant API"
}
```

### Check Frontend

Open `http://localhost:3000` in your browser. You should see the landing page.

---

## First Steps with SSA

### 1. Upload a Document

1. Go to **Documents** → **Upload New**
2. Upload a `.txt` or `.md` file (or paste content directly)
3. Add a title and optional document type
4. Click "Upload Document"

### 2. Search Documents

1. Go to **Search**
2. Enter a search query (e.g., "machine learning")
3. View semantic search results with similarity scores

### 3. Ask Questions

1. Go to **Q&A**
2. Ask a question about your documents
3. Optionally enable "Use AI Agent" for more sophisticated reasoning
4. Get instant answers based on your study materials

### 4. View Analytics

1. Go to **Analytics**
2. See visualizations of:
   - Total documents and average length
   - Most common words
   - Document type distribution

---

## API Endpoints

### Core Endpoints

**Health Check**
```bash
GET /health
```

**List Documents**
```bash
GET /documents?skip=0&limit=10
```

**Upload Document**
```bash
POST /documents/ingest
Content-Type: application/json

{
  "title": "My Lecture Notes",
  "content": "...",
  "document_type": "lecture"
}
```

**Search Documents**
```bash
POST /documents/search
Content-Type: application/json

{
  "query": "search query",
  "top_k": 5,
  "threshold": 0.2
}
```

**Ask Question**
```bash
POST /qa/ask
Content-Type: application/json

{
  "question": "What is machine learning?",
  "use_agent": false
}
```

**Get Analytics**
```bash
GET /analytics/dashboard
```

### Full API Documentation

With the backend running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Troubleshooting

### Issue: "Connection refused" when accessing API

**Solution**: Make sure the FastAPI backend is running:
```bash
uvicorn api:app --reload --port 8000
```

### Issue: Port 8000 already in use

**Solution**: Use a different port:
```bash
uvicorn api:app --reload --port 8001
```

Then update the frontend API URL in `app/documents/page.tsx` and other components to use `http://localhost:8001`

### Issue: Port 3000 already in use

**Solution**: Use a different port:
```bash
npm run dev -- -p 3001
```

### Issue: Dependencies installation fails

**Solution**: Clear cache and reinstall:

For Python:
```bash
# Remove venv and reinstall
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirment.txt
```

For Node:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: Docker build fails

**Solution**: 
```bash
# Remove old containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

---

## Environment Variables

Create a `.env.local` file in the project root:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production deployment, set:
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

---

## Development Workflow

### Making Backend Changes

1. Edit Python files in `/src/` or `api.py`
2. FastAPI with `--reload` will automatically restart
3. Changes available immediately

### Making Frontend Changes

1. Edit files in `/app/`, `/components/`, or `/lib/`
2. Next.js with `npm run dev` will hot-reload
3. Changes visible instantly in browser

### Testing API Locally

Use the built-in Swagger UI at `http://localhost:8000/docs` to test endpoints interactively.

---

## Project Structure

```
Smart-Study-Assistant/
├── api.py                    # FastAPI backend
├── App.py                    # Legacy CLI (optional)
├── requirment.txt           # Python dependencies
├── package.json             # Node dependencies
│
├── src/ssa/                 # Python backend modules
│   ├── core/               # Document management
│   ├── ml/                 # Machine learning models
│   ├── qa/                 # Q&A system
│   └── agent/              # AI agent
│
├── app/                     # Next.js app directory
│   ├── page.tsx            # Home page
│   ├── documents/          # Documents page
│   ├── search/             # Search page
│   ├── qa/                 # Q&A page
│   ├── analytics/          # Analytics page
│   └── layout.tsx          # Root layout
│
├── components/             # Reusable React components
│   ├── ui/                 # shadcn/ui components
│   ├── documents/          # Document-related components
│   ├── navbar.tsx          # Navigation bar
│   └── theme-provider.tsx  # Dark mode provider
│
├── lib/                    # Utility functions
├── hooks/                  # Custom React hooks
├── public/                 # Static assets
│
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker build instructions
├── SETUP.md               # This file
└── README.md              # Project overview
```

---

## Next Steps

1. **Explore the UI** - Familiarize yourself with all features
2. **Upload Documents** - Start building your knowledge base
3. **Try Search** - Experience semantic search capabilities
4. **Ask Questions** - Get answers from your materials
5. **Check Analytics** - Understand your learning data

---

## Performance Tips

- **Large Datasets**: If you have many documents, increase `top_k` in search threshold for faster results
- **GPU Acceleration**: For better performance, install GPU support:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```
- **Caching**: The system automatically caches embeddings for faster searches on repeat queries

---

## Support & Contributing

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with:
   - Python version
   - Node version
   - Error message/logs
   - Steps to reproduce

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

Special thanks to:
- The transformers and sentence-transformers communities
- FastAPI and Next.js teams
- All contributors to this project

**Happy learning! 🚀**
