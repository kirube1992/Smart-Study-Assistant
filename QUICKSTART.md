# Smart Study Assistant - Quick Start Guide

Get up and running in 5 minutes!

## The Absolute Fastest Way

### Using Docker (Recommended - 1 Command)

```bash
docker-compose up --build
```

Done! Open `http://localhost:3000`

---

## Local Setup (5-10 minutes)

### Step 1: Clone & Navigate
```bash
git clone https://github.com/kirube1992/Smart-Study-Assistant.git
cd Smart-Study-Assistant
```

### Step 2: Backend Setup (Terminal 1)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirment.txt
uvicorn api:app --reload --port 8000
```

Wait for: `Application startup complete`

### Step 3: Frontend Setup (Terminal 2)
```bash
npm install
npm run dev
```

Wait for: `ready - started server on 0.0.0.0:3000`

### Step 4: Open Browser
Go to: `http://localhost:3000`

---

## First 5 Things to Try

1. **Upload a Document**
   - Click "Documents" → "Upload New"
   - Paste or upload text content
   - Give it a title and type
   - Click "Upload Document"

2. **Search Your Documents**
   - Click "Search"
   - Type a question or topic
   - See relevant documents ranked by similarity

3. **Ask a Question**
   - Click "Q&A"
   - Ask a question about your documents
   - Get AI-powered answers

4. **View Analytics**
   - Click "Analytics"
   - See visualizations of your knowledge base
   - Understand your study materials

5. **Explore API**
   - Visit `http://localhost:8000/docs`
   - See all available API endpoints
   - Try them interactively

---

## Troubleshooting

**"Connection refused" error?**
- Make sure both backend and frontend are running
- Backend should be on port 8000
- Frontend should be on port 3000

**Port already in use?**
```bash
# Use different port for backend
uvicorn api:app --reload --port 8001

# Use different port for frontend
npm run dev -- -p 3001
```

**Dependencies not installing?**
```bash
# Python
pip install --upgrade pip
pip install -r requirment.txt

# Node
npm cache clean --force
npm install
```

---

## What's Working

✅ Upload & organize documents  
✅ Semantic search across documents  
✅ AI-powered Q&A system  
✅ Learning analytics & insights  
✅ REST API for all features  
✅ Docker containerization  

---

## API Quick Reference

### Upload Document
```bash
curl -X POST "http://localhost:8000/documents/ingest" \
  -H "Content-Type: application/json" \
  -d '{"title":"Notes","content":"...","document_type":"lecture"}'
```

### Search
```bash
curl -X POST "http://localhost:8000/documents/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"machine learning","top_k":5}'
```

### Ask Question
```bash
curl -X POST "http://localhost:8000/qa/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is AI?","use_agent":true}'
```

### Get Analytics
```bash
curl "http://localhost:8000/analytics/dashboard"
```

---

## Need Help?

- See [SETUP.md](./SETUP.md) for detailed instructions
- Check [README.md](./README.md) for project overview
- Visit `http://localhost:8000/docs` for API documentation
- View `run.sh` for automated setup script

---

## Next Steps

1. Upload your actual study materials
2. Try different search queries
3. Ask complex questions to test the AI
4. Explore the analytics dashboard
5. Check out the API documentation

Happy learning! 🚀
