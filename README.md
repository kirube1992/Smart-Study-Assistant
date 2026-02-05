

# Smart Study Assistant

Your Personal AI-Powered Learning Companion

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)
![Node 18+](https://img.shields.io/badge/Node-18%2B-green)
![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Phase 5](https://img.shields.io/badge/Phase-5-blueviolet)

1. Project Overview

Welcome to the Smart Study Assistant (SSA)! This project is an ambitious, end-to-end AI engineering journey to create an intelligent learning companion. The SSA aims to revolutionize how students interact with their study materials by providing organization, intelligent search, personalized explanations, and generative Q&A capabilities.

This README will evolve alongside the project, reflecting its growing complexity and features.

2. Vision & Goals

The core vision for the SSA is to build an AI that acts as:

Your Digital Librarian: Smartly ingesting, organizing, and categorizing all your study materials.

Your Intelligent Search Engine: Moving beyond keywords to understand the meaning of your queries and documents.

Your Personalized Tutor: Offering contextual Q&A, explanations tailored to your needs, and potentially adaptive learning paths.

Your AI Study Buddy: An autonomous agent capable of orchestrating various AI tools to assist your learning journey.

Each phase of this project integrates new AI/engineering concepts directly into the SSA, making it progressively smarter and more functional.

## Features

### Phase 1: Data Management & Foundation ✅
- Document Ingestion: Add study materials via CLI or web UI
- Structured Storage: Documents with metadata (title, type, difficulty, date)
- Basic Analytics: Document count, word count, statistics

### Phase 2: Machine Learning Fundamentals ✅
- Automatic Document Classification: Tag documents by type
- Content Clustering: Group semantically similar materials
- Difficulty Scoring: Assess content complexity

### Phase 3: Deep Learning Capabilities ✅
- Semantic Embeddings: Transformer-based document vectors
- Semantic Search: Find documents by meaning, not keywords
- Extractive Summarization: Generate concise summaries

### Phase 4: LLMs & AI Agents ✅
- Generative Q&A: Answer questions from your documents
- Smart Agent: Automatically selects the best tool for your query
- Multi-tool Orchestration: Search, summarize, classify in one query

### Phase 5: MLOps & Deployment ✅
- FastAPI Backend: Production-ready REST API
- Next.js Frontend: Modern, responsive web interface
- Docker Support: Single-command deployment
- Local Development Setup: Complete development environment

## Technologies Used

### Backend
- **Python 3.9+** - Core language
- **FastAPI** - REST API framework
- **PyTorch** - Deep learning
- **Hugging Face Transformers** - NLP models
- **Sentence Transformers** - Semantic embeddings
- **Scikit-learn** - Traditional ML
- **NumPy & Pandas** - Data processing
- **LangChain** - LLM orchestration

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type-safe development
- **React 19** - UI library
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Uvicorn** - ASGI server
- **Git & GitHub** - Version control

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (optional)

### Installation

#### Option 1: Local Development (Recommended)

```bash
# Clone repository
git clone https://github.com/kirube1992/Smart-Study-Assistant.git
cd Smart-Study-Assistant

# Run setup script
chmod +x run.sh
./run.sh

# In Terminal 1 - Start Backend
source venv/bin/activate
uvicorn api:app --reload --port 8000

# In Terminal 2 - Start Frontend
npm run dev
```

Then open `http://localhost:3000`

#### Option 2: Docker (All-in-One)

```bash
# Build and run everything
docker-compose up --build

# Services will be available at:
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

For detailed setup instructions, see [SETUP.md](./SETUP.md)

## Usage

### Web Interface

1. **Upload Documents** - Go to Documents tab and upload study materials
2. **Search** - Use semantic search to find relevant documents
3. **Ask Questions** - Get answers from your materials with AI
4. **View Analytics** - See insights about your knowledge base

### API Usage

**Upload Document**
```bash
curl -X POST "http://localhost:8000/documents/ingest" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Notes","content":"...","document_type":"lecture"}'
```

**Search Documents**
```bash
curl -X POST "http://localhost:8000/documents/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"machine learning","top_k":5}'
```

**Ask a Question**
```bash
curl -X POST "http://localhost:8000/qa/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is neural networks?","use_agent":true}'
```

See [Full API Documentation](http://localhost:8000/docs) when running the backend


## Development

### Project Structure
```
Smart-Study-Assistant/
├── api.py                 # FastAPI application
├── src/ssa/              # Python backend modules
│   ├── core/             # Document management
│   ├── ml/               # ML models & analysis
│   ├── qa/               # Q&A system
│   └── agent/            # AI agent
├── app/                  # Next.js application
├── components/           # React components
├── docker-compose.yml    # Container orchestration
└── SETUP.md             # Setup guide
```

### Contributing
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes following PEP 8 (Python) and ESLint (JavaScript) guidelines
3. Test your changes locally
4. Commit with clear messages
5. Push and create a pull request

### Code Style
- **Python**: PEP 8, type hints recommended
- **JavaScript/TypeScript**: ESLint config provided
- **Git**: Clear, descriptive commit messages 

## Roadmap & Milestones

This project follows a 120-day AI Engineering learning path:

- ✅ **Phase 1**: Data Management & Foundation
- ✅ **Phase 2**: ML Fundamentals & Intelligence
- ✅ **Phase 3**: Deep Learning & Semantic Understanding
- ✅ **Phase 4**: LLMs & AI Agents
- ✅ **Phase 5**: MLOps & Deployment (Current - 70% Complete)
- 🚀 **Phase 6**: Portfolio & Future Trends

### Current Status: 70-75% Complete

**Completed:**
- All core Python backend (Phases 1-4)
- FastAPI REST API implementation
- Next.js web frontend with dashboard
- Docker containerization
- Local development setup

**In Progress:**
- Advanced error handling and logging
- Comprehensive testing suite
- Performance optimization

**Next Steps:**
- CI/CD pipeline setup
- Advanced personalization features
- Multi-modal input support
- Cloud deployment guides

## Future Enhancements

- **Multi-modal Support**: Images, PDFs, audio, and video materials
- **Flashcard Generation**: Automatic quiz generation from documents
- **External Integrations**: Notion, Anki, Google Classroom sync
- **Advanced Personalization**: Adaptive learning based on performance
- **Voice Interface**: Voice-based queries and interactions
- **Mobile App**: Native iOS/Android applications
- **Collaborative Learning**: Share materials and notes with study groups
- **Advanced Analytics**: Learning patterns and recommendations
- **Offline Mode**: Work without internet connection
- **Real-time Collaboration**: Live study sessions

12. License

This project is licensed under the MIT License - see the LICENSE file for details.

13. Contact & Acknowledgments

Developers:

[Kirubel Aynalem] - [(https://github.com/kirube1992)]

Acknowledgments:

Special thanks to God Jesus and the holy sprit 
